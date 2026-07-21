import math
import os
from ingestion import DataIngestor

def get_cyclic_model_prediction(history, period, future_steps):
    """
    A simple model: fits a sine wave to the history and extrapolates.
    """
    n = len(history)
    # Fit sine wave: y = A*sin(2*pi*t/period + phase)
    # Simple estimation for A and phase
    # (Using period=9 as identified in stability test)
    
    # We use the last 'period' of history to project
    t_history = list(range(n))
    
    # Very simple fit: use average of the last cycle
    # More robust: non-linear least squares fit
    
    # Naive extrapolation of the last cycle
    predictions = []
    for i in range(future_steps):
        # Index into the last cycle
        last_cycle_idx = (n - int(period) + i) % int(period)
        predictions.append(history[n - int(period) + last_cycle_idx])
    return predictions

def main():
    ingestor = DataIngestor()
    raw = ingestor.load_from_json('cache_worldbank.json')
    processed = ingestor.preprocess_series(raw)
    years = sorted(processed.keys())
    
    # Split: Train up to 2010, Test 2011-2025
    train_years = [y for y in years if y <= 2010]
    test_years = [y for y in years if y > 2010]
    
    train_vals = [processed[y] for y in train_years]
    test_vals = [processed[y] for y in test_years]
    
    # 1. Cyclic Forecast (Period 9)
    predictions = get_cyclic_model_prediction(train_vals, 9.0, len(test_vals))
    
    # 2. Naive Forecast (Persistence: last value)
    naive_forecast = [train_vals[-1]] * len(test_vals)
    
    # 3. Evaluate (MSE)
    mse_cyclic = sum((p - a)**2 for p, a in zip(predictions, test_vals)) / len(test_vals)
    mse_naive = sum((n - a)**2 for n, a in zip(naive_forecast, test_vals)) / len(test_vals)
    
    print(f"Forecast Evaluation (2011-2025):")
    print(f"  Cyclic Model (Period 9) MSE: {mse_cyclic:.4f}")
    print(f"  Naive Model (Persistence) MSE: {mse_naive:.4f}")
    
    if mse_cyclic < mse_naive:
        print("Result: Cyclic model outperforms naive baseline.")
    else:
        print("Result: Cyclic model does not add predictive value over naive baseline.")

if __name__ == "__main__":
    main()
