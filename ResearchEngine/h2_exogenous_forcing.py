import random
import math
from collections import deque

class SystemAgent:
    """Agent with exogenous driving force."""
    def __init__(self, name, state, coupling_coeffs):
        self.name = name
        self.state = state
        self.coupling_coeffs = coupling_coeffs

    def update(self, neighbor_states, exogenous_driver):
        raw_influence = sum(self.coupling_coeffs.get(name, 0) * neighbor_states.get(name, 0) 
                            for name in self.coupling_coeffs)
        
        # Influence + Exogenous Driver
        influence = raw_influence + exogenous_driver
        
        # Apply sigmoid
        activation = 1.0 / (1.0 + math.exp(-influence)) - 0.5
        
        self.state = 0.8 * self.state + activation + random.gauss(0, 0.05)
        return self.state

class H2Model:
    def __init__(self):
        self.agents = {
            'Climate': SystemAgent('Climate', 0.5, {'Agri': 0.1}),
            'Agri': SystemAgent('Agri', 0.5, {'Climate': 0.2, 'Biodiversity': 0.1}),
            'Biodiversity': SystemAgent('Biodiversity', 0.5, {'Climate': 0.1, 'Conflict': -0.2}),
            'Economy': SystemAgent('Economy', 0.5, {'Agri': 0.2, 'Conflict': -0.3}),
            'Conflict': SystemAgent('Conflict', 0.2, {'Economy': -0.1, 'Disease': 0.1}),
            'Disease': SystemAgent('Disease', 0.2, {'Conflict': 0.1, 'Biodiversity': -0.1})
        }

    def step(self, t):
        # 9-year exogenous driver
        exogenous_driver = 0.5 * math.sin(2 * math.pi * t / 9.0)
        
        current_states = {name: agent.state for name, agent in self.agents.items()}
        new_states = {}
        for name, agent in self.agents.items():
            new_states[name] = agent.update(current_states, exogenous_driver)
        return new_states

if __name__ == "__main__":
    model = H2Model()
    history = []
    for t in range(100):
        history.append(model.step(t))
    
    climate_values = [s['Climate'] for s in history]
    times = list(range(len(climate_values)))
    from analysis_engine import lomb_scargle
    freqs = [1/p for p in range(2, 30)]
    results = lomb_scargle(times, climate_values, freqs)
    best_freq, best_power = max(results, key=lambda x: x[1])
    print(f"H2 (Exogenous Forcing) Period: {1/best_freq:.2f}y (Power: {best_power:.4f})")
