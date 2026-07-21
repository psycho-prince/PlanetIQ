import os
import numpy as np
import random
from ingestion import DataIngestor
from analysis_engine import lomb_scargle

def get_peak(times, values, period_min, period_max):
    freqs = np.linspace(1/period_max, 1/period_min, 100)
    results = lomb_scargle(times, values, freqs)
    best_freq, best_power = max(results, key=lambda x: x[1])
    return 1/best_freq, best_power

def falsification_suite(filepath):
    print(f"\n--- Falsification Testing: {filepath} ---")
    ingestor = DataIngestor()
    raw = ingestor.load_from_csv(filepath) if filepath.endswith('.csv') else ingestor.load_from_json(filepath)
    processed = ingestor.preprocess_series(raw)
    times = list(processed.keys())
    values = list(processed.values())
    
    # Baseline
    best_p, best_pow = get_peak(times, values, 5, 20)
    print(f"Baseline: Period {best_p:.2f}y (Power: {best_pow:.4f})")
    
    # 1. Parameter Sensitivity (Varying Lomb-Scargle resolution)
    # If the peak vanishes with different grid density, it's an artifact.
    freqs_coarse = np.linspace(1/20, 1/5, 20)
    res_c = lomb_scargle(times, values, freqs_coarse)
    best_p_c, best_pow_c = max(res_c, key=lambda x: x[1])
    print(f"Sensitivity (Coarse grid): Period {best_p_c:.2f}y (Power: {best_pow_c:.4f})")
    
    # 2. Randomized Window Validation
    # If the peak depends on contiguous time, it's not a true cycle.
    indices = random.sample(range(len(values)), int(len(values)*0.7))
    times_r = [times[i] for i in indices]
    vals_r = [values[i] for i in indices]
    best_p_r, best_pow_r = get_peak(times_r, vals_r, 5, 20)
    print(f"Randomized Sampling: Period {best_p_r:.2f}y (Power: {best_pow_r:.4f})")

if __name__ == "__main__":
    data_dir = '../data/raw'
    # Test on GDP (WorldBank)
    falsification_suite('cache_worldbank.json')
    # Test on one representative dataset
    falsification_suite(os.path.join(data_dir, 'conflict.csv'))
