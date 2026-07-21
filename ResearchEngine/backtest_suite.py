import os
from ingestion import DataIngestor

def backtest_dataset(ingestor, filepath):
    raw = ingestor.load_from_csv(filepath) if filepath.endswith('.csv') else ingestor.load_from_json(filepath)
    processed = ingestor.preprocess_series(raw)
    
    # Sort years
    years = sorted(processed.keys())
    train_years = [y for y in years if y <= 2000]
    test_years = [y for y in years if y > 2000]
    
    if not test_years:
        return None
        
    train_vals = [processed[y] for y in train_years]
    test_vals = [processed[y] for y in test_years]
    
    # Persistence Model (Naive Forecast)
    last_val = train_vals[-1]
    persistence_forecast = [last_val] * len(test_vals)
    
    # Simple Persistence MSE
    mse_persistence = sum((p - a)**2 for p, a in zip(persistence_forecast, test_vals)) / len(test_vals)
    
    return mse_persistence

def main():
    ingestor = DataIngestor()
    results = {}
    
    # 1. Existing Data
    if os.path.exists('cache_worldbank.json'):
        results['GDP'] = backtest_dataset(ingestor, 'cache_worldbank.json')
    
    # 2. PlanetIQ Data
    data_dir = 'PlanetIQ/data/raw'
    for filename in os.listdir(data_dir):
        if filename.endswith(('.csv')):
            path = os.path.join(data_dir, filename)
            results[filename.split('.')[0]] = backtest_dataset(ingestor, path)
            
    print("\n--- Out-of-Sample Backtesting (MSE of Persistence Baseline) ---")
    for dataset, mse in results.items():
        print(f"{dataset:>20}: {mse:.4f}")

if __name__ == "__main__":
    main()
