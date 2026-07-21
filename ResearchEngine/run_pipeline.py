import math
import random
from ingestion import DataIngestor
from analysis_engine import lomb_scargle

def estimate_ar1(values):
    if len(values) < 2: return 0
    y_t = values[1:]
    y_prev = values[:-1]
    n = len(y_prev)
    mean_y = sum(y_prev) / n
    mean_yt = sum(y_t) / n
    num = sum((y_t[i] - mean_yt) * (y_prev[i] - mean_y) for i in range(n))
    den = math.sqrt(sum((y_t[i] - mean_yt)**2 for i in range(n)) * 
                    sum((y_prev[i] - mean_y)**2 for i in range(n)))
    return num / den if den != 0 else 0

def generate_ar1_series(n, phi, sigma=1.0):
    series = [random.gauss(0, sigma)]
    for _ in range(1, n):
        series.append(phi * series[-1] + random.gauss(0, sigma))
    return series

def get_power_at_period(times, values, target_period):
    """Computes power at a specific period using Lomb-Scargle."""
    freq = 1 / target_period
    # We re-run Lomb-Scargle for the single frequency
    res = lomb_scargle(times, values, [freq])
    return res[0][1]

def run_ar1_significance_test(times, values, target_period, iterations=1000):
    phi = estimate_ar1(values)
    observed_power = get_power_at_period(times, values, target_period)
    
    count = 0
    for _ in range(iterations):
        synthetic = generate_ar1_series(len(values), phi)
        # Synthetic data needs the same detrending
        # Simplified: assume same times/trend
        synthetic_power = get_power_at_period(times, synthetic, target_period)
        if synthetic_power >= observed_power:
            count += 1
            
    return (count + 1) / (iterations + 1)

def analyze_dataset(ingestor, filepath):
    print(f"\nAnalyzing: {filepath}")
    
    # 1. Ingest
    if filepath.endswith('.json'): raw = ingestor.load_from_json(filepath)
    elif filepath.endswith('.csv'): raw = ingestor.load_from_csv(filepath)
    else: return
    processed = ingestor.preprocess_series(raw)
    
    times = list(processed.keys())
    values = list(processed.values())
    
    # 2. Period Analysis
    freqs = [1/p for p in range(2, 61)]
    results = lomb_scargle(times, values, freqs)
    best_freq, best_power = max(results, key=lambda x: x[1])
    target_period = 1/best_freq
    print(f"  Strongest Period: {target_period:.2f} years (Power: {best_power:.4f})")
    
    # 3. Statistical Validation (AR1 Red Noise)
    print("  Running Red Noise Significance Test...")
    p_val = run_ar1_significance_test(times, values, target_period, iterations=500)
    print(f"  Significance (p-value vs red noise): {p_val:.4f}")
    if p_val < 0.05:
        print("  Result: Statistically significant cycle.")
    else:
        print("  Result: Not significant (consistent with red noise).")

if __name__ == "__main__":
    ingestor = DataIngestor()
    import os
    if os.path.exists('cache_worldbank.json'):
        analyze_dataset(ingestor, 'cache_worldbank.json')
    data_dir = 'PlanetIQ/data/raw'
    for filename in os.listdir(data_dir):
        if filename.endswith(('.csv', '.json')):
            analyze_dataset(ingestor, os.path.join(data_dir, filename))
