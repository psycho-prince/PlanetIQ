import csv
import math
import random

def generate_data(filename, period, amplitude, trend, noise_level=0.5):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Year', 'Value'])
        for year in range(1960, 2026):
            t = year - 1960
            # Shared 9-year cycle + unique trend + noise
            val = amplitude * math.sin(2 * math.pi * t / 9.0) + trend * t + random.gauss(0, noise_level)
            writer.writerow([year, val])

# New datasets for further stress testing
generate_data('PlanetIQ/data/raw/stock_volatility.csv', period=9.0, amplitude=10, trend=0.2)
generate_data('PlanetIQ/data/raw/agriculture_yield.csv', period=9.0, amplitude=2, trend=-0.1)
generate_data('PlanetIQ/data/raw/disease_outbreaks.csv', period=9.0, amplitude=6, trend=0.3)
