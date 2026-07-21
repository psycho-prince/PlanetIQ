import math

def lomb_scargle(times, values, frequencies):
    """
    Computes the Lomb-Scargle periodogram for a given set of frequencies.
    
    times: list of time points (e.g., years)
    values: list of signal values
    frequencies: list of frequencies to test
    """
    n = len(times)
    mean_val = sum(values) / n
    centered_values = [v - mean_val for v in values]
    
    periodogram = []
    
    for freq in frequencies:
        omega = 2 * math.pi * freq
        
        # Calculate tau
        # tan(2 * omega * tau) = sum(sin(2 * omega * t_i)) / sum(cos(2 * omega * t_i))
        sin_2ot = sum(math.sin(2 * omega * t) for t in times)
        cos_2ot = sum(math.cos(2 * omega * t) for t in times)
        tau = math.atan2(sin_2ot, cos_2ot) / (2 * omega)
        
        # Calculate power
        cos_ot_tau = [math.cos(omega * (t - tau)) for t in times]
        sin_ot_tau = [math.sin(omega * (t - tau)) for t in times]
        
        num_cos = sum(v * c for v, c in zip(centered_values, cos_ot_tau)) ** 2
        den_cos = sum(c * c for c in cos_ot_tau)
        
        num_sin = sum(v * s for v, s in zip(centered_values, sin_ot_tau)) ** 2
        den_sin = sum(s * s for s in sin_ot_tau)
        
        power = (num_cos / den_cos + num_sin / den_sin) / 2
        periodogram.append((freq, power))
        
    return periodogram

# Simple Test
if __name__ == "__main__":
    # Test with a known 10-year cycle
    times = list(range(50))
    values = [math.sin(2 * math.pi * t / 10) for t in times]
    
    # Test frequencies from 0.01 to 0.5 (periods from 100 to 2 years)
    freqs = [f * 0.005 for f in range(1, 100)]
    
    results = lomb_scargle(times, values, freqs)
    
    best_freq, best_power = max(results, key=lambda x: x[1])
    
    print(f"Detected strongest frequency: {best_freq:.4f} (Period: {1/best_freq:.2f})")
    print(f"Peak Power: {best_power:.4f}")
