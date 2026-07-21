import random

class SystemAgent:
    """Agent representing a system domain (Climate, Agri, etc.)"""
    def __init__(self, name, state, coupling_coeffs):
        self.name = name
        self.state = state
        self.coupling_coeffs = coupling_coeffs # {other_name: coefficient}

    def update(self, neighbor_states):
        # State update = Internal dynamics (autoregressive) + Coupling influences
        # Simplified: s_t = phi * s_{t-1} + sum(coeff * neighbor_s) + noise
        
        influence = sum(self.coupling_coeffs.get(name, 0) * state 
                        for name, state in neighbor_states.items())
        
        # Internal autoregressive component (e.g., 0.8)
        self.state = 0.8 * self.state + influence + random.gauss(0, 0.1)
        return self.state

class SystemDynamicsModel:
    def __init__(self):
        # Define causal influence matrix
        # Climate -> Agri, Conflict -> Biodiversity, etc.
        self.agents = {
            'Climate': SystemAgent('Climate', 0.5, {'Agri': 0.1}),
            'Agri': SystemAgent('Agri', 0.5, {'Climate': 0.2, 'Biodiversity': 0.1}),
            'Biodiversity': SystemAgent('Biodiversity', 0.5, {'Climate': 0.1, 'Conflict': -0.2}),
            'Economy': SystemAgent('Economy', 0.5, {'Agri': 0.2, 'Conflict': -0.3}),
            'Conflict': SystemAgent('Conflict', 0.2, {'Economy': -0.1, 'Disease': 0.1}),
            'Disease': SystemAgent('Disease', 0.2, {'Conflict': 0.1, 'Biodiversity': -0.1})
        }

    def step(self):
        current_states = {name: agent.state for name, agent in self.agents.items()}
        new_states = {}
        for name, agent in self.agents.items():
            new_states[name] = agent.update(current_states)
        return new_states

# Test the ABM simulation
if __name__ == "__main__":
    model = SystemDynamicsModel()
    history = []
    
    print("Running ABM simulation...")
    for _ in range(60): # 60 years
        history.append(model.step())
        
    # Print sample of the simulated oscillations
    for i, step in enumerate(history[::10]):
        print(f"Year {i*10}: Climate={step['Climate']:.2f}, Conflict={step['Conflict']:.2f}")
