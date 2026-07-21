import random
import math

class SystemAgent:
    """Agent representing a system domain with non-linear threshold activation."""
    def __init__(self, name, state, coupling_coeffs):
        self.name = name
        self.state = state
        self.coupling_coeffs = coupling_coeffs

    def update(self, neighbor_states):
        # Linear sum of influences
        raw_influence = sum(self.coupling_coeffs.get(name, 0) * state 
                            for name, state in neighbor_states.items())
        
        # Apply Sigmoid activation to constraint systemic feedback
        # Prevents the runaway instability observed in linear models
        influence = 1.0 / (1.0 + math.exp(-raw_influence)) - 0.5
        
        # Internal autoregressive component + non-linear coupling
        self.state = 0.8 * self.state + influence + random.gauss(0, 0.05)
        return self.state

class SystemDynamicsModel:
    def __init__(self):
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
