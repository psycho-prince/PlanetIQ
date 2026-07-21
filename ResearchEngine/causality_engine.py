import math
import numpy as np

def get_phase(times, values, period):
    freq = 1.0 / period
    omega = 2 * math.pi * freq
    cos_sum = sum(v * math.cos(omega * t) for t, v in zip(times, values))
    sin_sum = sum(v * math.sin(omega * t) for t, v in zip(times, values))
    return math.atan2(-sin_sum, cos_sum)

def check_phase_coherence(series1, series2, period):
    times1 = list(series1.keys())
    values1 = list(series1.values())
    times2 = list(series2.keys())
    values2 = list(series2.values())
    phase1 = get_phase(times1, values1, period)
    phase2 = get_phase(times2, values2, period)
    return abs(phase1 - phase2)

def granger_causality(y, x, lag=2):
    """
    Directional influence of x on y using OLS.
    Returns the reduction in SSR (Sum of Squared Residuals).
    """
    n = len(y)
    if n <= lag * 2: return 0
    
    # Lagged matrices
    Y = y[lag:]
    
    # Reduced model: Y_t ~ Y_{t-1}, Y_{t-2}
    X_reduced = np.column_stack([y[i:n-lag+i] for i in range(lag)][::-1] + [np.ones(n-lag)])
    
    # Full model: Y_t ~ Y_{t-1}, Y_{t-2}, X_{t-1}, X_{t-2}
    X_full = np.column_stack([X_reduced[:, :-1]] + [x[i:n-lag+i] for i in range(lag)][::-1] + [np.ones(n-lag)])
    
    # Solve OLS
    beta_reduced, res_reduced, _, _ = np.linalg.lstsq(X_reduced, Y, rcond=None)
    beta_full, res_full, _, _ = np.linalg.lstsq(X_full, Y, rcond=None)
    
    # Return SSR difference normalized
    ssr_reduced = res_reduced[0] if len(res_reduced) > 0 else sum((Y - X_reduced @ beta_reduced)**2)
    ssr_full = res_full[0] if len(res_full) > 0 else sum((Y - X_full @ beta_full)**2)
    
    if ssr_reduced == 0: return 0
    return (ssr_reduced - ssr_full) / ssr_reduced

# Test functionality
if __name__ == "__main__":
    # Test with known causality
    s1 = np.array([math.sin(t/1.0) for t in range(50)])
    s2 = np.array([0.5 * s1[i-1] + 0.1 * np.random.normal() for i in range(50)])
    
    causality = granger_causality(s1, s2)
    print(f"Granger causality (X->Y): {causality:.4f}")
