import math
import random

def estimate_ar1(values):
    """Estimates the AR(1) coefficient (phi) from the data."""
    if len(values) < 2:
        return 0
    # y_t = phi * y_{t-1} + epsilon
    # phi = correlation(y_t, y_{t-1})
    y_t = values[1:]
    y_prev = values[:-1]
    
    n = len(y_prev)
    mean_y = sum(y_prev) / n
    mean_yt = sum(y_t) / n
    
    num = sum((y_t[i] - mean_yt) * (y_prev[i] - mean_y) for i in range(n))
    den = math.sqrt(sum((y_t[i] - mean_yt)**2 for i in range(n)) * 
                    sum((y_prev[i] - mean_y)**2 for i in range(n)))
    
    if den == 0:
        return 0
    return num / den

def generate_ar1_series(n, phi, sigma=1.0):
    """Generates a synthetic AR(1) series."""
    series = [random.gauss(0, sigma)]
    for _ in range(1, n):
        series.append(phi * series[-1] + random.gauss(0, sigma))
    return series

def get_peak_power(values, target_period):
    """Simplified period power check."""
    # This is a placeholder; in the real pipeline, we'd reuse analysis_engine.py logic
    # For now, let's just find the power at the target frequency
    freq = 1 / target_period
    # Simplified Lomb-Scargle power estimate at specific frequency
    # (Matches analysis_engine.py logic)
    # ...
    # Placeholder: return random value for testing
    return random.random()

def run_ar1_significance_test(values, target_period, iterations=1000):
    phi = estimate_ar1(values)
    observed_power = get_peak_power(values, target_period)
    
    count = 0
    for _ in range(iterations):
        synthetic = generate_ar1_series(len(values), phi)
        # Process synthetic similarly to real data (detrend)
        # ...
        synthetic_power = get_peak_power(synthetic, target_period)
        if synthetic_power >= observed_power:
            count += 1
            
    return (count + 1) / (iterations + 1)

# Test
if __name__ == "__main__":
    # Test values
    test_vals = [i + random.gauss(0, 1) for i in range(50)]
    phi = estimate_ar1(test_vals)
    print(f"Estimated AR(1) phi: {phi:.4f}")
    
    # Run test
    p_val = run_ar1_significance_test(test_vals, 10.0)
    print(f"Red noise significance p-value: {p_val:.4f}")
