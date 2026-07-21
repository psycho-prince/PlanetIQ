import numpy as np
import random
from mechanistic_abm import SystemDynamicsModel, SystemAgent
from analysis_engine import lomb_scargle

def get_best_period(states_history):
    # Analyze Climate state over time
    climate_values = [s['Climate'] for s in states_history]
    times = list(range(len(climate_values)))
    
    freqs = [1/p for p in range(2, 30)]
    results = lomb_scargle(times, climate_values, freqs)
    best_freq, best_power = max(results, key=lambda x: x[1])
    return 1/best_freq, best_power

def run_sensitivity_test():
    base_model = SystemDynamicsModel()
    
    # Define coupling modifications (±50%)
    variations = [0.5, 1.0, 1.5]
    
    print("--- Mechanistic Sensitivity Analysis (±50% Coupling) ---")
    
    for var in variations:
        model = SystemDynamicsModel()
        # Scale all coupling coefficients
        for agent in model.agents.values():
            for other in agent.coupling_coeffs:
                agent.coupling_coeffs[other] *= var
                
        # Simulate
        history = []
        for _ in range(100):
            history.append(model.step())
            
        period, power = get_best_period(history)
        print(f"Coupling Multiplier {var}x: Detected Period {period:.2f}y (Power: {power:.4f})")

if __name__ == "__main__":
    run_sensitivity_test()
