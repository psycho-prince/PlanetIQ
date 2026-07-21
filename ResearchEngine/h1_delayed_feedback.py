import random
import math
from collections import deque

class SystemAgent:
    """Agent with delayed feedback."""
    def __init__(self, name, state, coupling_coeffs, delay=2):
        self.name = name
        self.state = state
        self.coupling_coeffs = coupling_coeffs
        self.history = deque([state] * delay, maxlen=delay)

    def update(self, neighbor_states):
        # Use delayed state (history[0])
        delayed_state = self.history[0]
        
        raw_influence = sum(self.coupling_coeffs.get(name, 0) * neighbor_states.get(name, 0) 
                            for name in self.coupling_coeffs)
        
        # Apply non-linear threshold (Sigmoid)
        influence = 1.0 / (1.0 + math.exp(-raw_influence)) - 0.5
        
        # New state depends on delayed feedback
        new_state = 0.7 * delayed_state + influence + random.gauss(0, 0.05)
        self.history.append(new_state)
        self.state = new_state
        return self.state

class H1Model:
    def __init__(self):
        # Increased coupling for H1 test
        self.agents = {
            'Climate': SystemAgent('Climate', 0.5, {'Agri': 0.2}),
            'Agri': SystemAgent('Agri', 0.5, {'Climate': 0.3, 'Biodiversity': 0.2}),
            'Biodiversity': SystemAgent('Biodiversity', 0.5, {'Climate': 0.2, 'Conflict': -0.3}),
            'Economy': SystemAgent('Economy', 0.5, {'Agri': 0.3, 'Conflict': -0.4}),
            'Conflict': SystemAgent('Conflict', 0.2, {'Economy': -0.2, 'Disease': 0.2}),
            'Disease': SystemAgent('Disease', 0.2, {'Conflict': 0.2, 'Biodiversity': -0.2})
        }

    def step(self):
        current_states = {name: agent.state for name, agent in self.agents.items()}
        new_states = {}
        for name, agent in self.agents.items():
            new_states[name] = agent.update(current_states)
        return new_states

if __name__ == "__main__":
    model = H1Model()
    history = []
    for _ in range(100):
        history.append(model.step())
    
    # Analyze Climate state
    climate_values = [s['Climate'] for s in history]
    times = list(range(len(climate_values)))
    from analysis_engine import lomb_scargle
    freqs = [1/p for p in range(2, 30)]
    results = lomb_scargle(times, climate_values, freqs)
    best_freq, best_power = max(results, key=lambda x: x[1])
    print(f"H1 (Delayed Feedback) Period: {1/best_freq:.2f}y (Power: {best_power:.4f})")
