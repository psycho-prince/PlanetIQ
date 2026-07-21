import math
import random
import os
from ingestion import DataIngestor
from analysis_engine import lomb_scargle
from run_pipeline import estimate_ar1, generate_ar1_series, get_power_at_period, run_ar1_significance_test

def analyze_sliding_window(ingestor, filepath, window_size=30, step=5):
    """Performs sliding window analysis to test cycle stability."""
    print(f"\n--- Sliding Window Analysis: {filepath} ---")
    
    # 1. Ingest
    if filepath.endswith('.json'): raw = ingestor.load_from_json(filepath)
    elif filepath.endswith('.csv'): raw = ingestor.load_from_csv(filepath)
    else: return
    processed = ingestor.preprocess_series(raw)
    
    # Extract years and values
    years = sorted(processed.keys())
    
    # 2. Iterate through windows
    for start_year in range(years[0], years[-1] - window_size + 1, step):
        end_year = start_year + window_size
        window_data = {y: processed[y] for y in years if start_year <= y < end_year}
        
        times = list(window_data.keys())
        values = list(window_data.values())
        
        # Spectral analysis
        freqs = [1/p for p in range(2, window_size // 2)]
        results = lomb_scargle(times, values, freqs)
        best_freq, best_power = max(results, key=lambda x: x[1])
        
        print(f"Window {start_year}-{end_year}: Best Period {1/best_freq:.2f}y (Power: {best_power:.4f})")

if __name__ == "__main__":
    ingestor = DataIngestor()
    # Test on GDP data
    if os.path.exists('cache_worldbank.json'):
        analyze_sliding_window(ingestor, 'cache_worldbank.json')
