import numpy as np
from h2_exogenous_forcing import H2Model
from analysis_engine import lomb_scargle

def get_best_period(states_history):
    climate_values = [s['Climate'] for s in states_history]
    times = list(range(len(climate_values)))
    freqs = [1/p for p in range(2, 30)]
    results = lomb_scargle(times, climate_values, freqs)
    best_freq, best_power = max(results, key=lambda x: x[1])
    return 1/best_freq, best_power

def stress_test_h2():
    print("--- H2 Stress Test: Stability (±25% variation) ---")
    # Base coupling is implicitly 0.1 to 0.4
    variations = [0.75, 1.0, 1.25]
    
    for var in variations:
        model = H2Model()
        for agent in model.agents.values():
            for other in agent.coupling_coeffs:
                agent.coupling_coeffs[other] *= var
        
        history = []
        for t in range(100):
            history.append(model.step(t))
        
        period, power = get_best_period(history)
        print(f"Coupling Multiplier {var}x: Period {period:.2f}y (Power: {power:.4f})")

if __name__ == "__main__":
    stress_test_h2()
