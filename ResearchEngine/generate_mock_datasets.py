import csv
import math
import random

def generate_data(filename, period, amplitude, trend):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Year', 'Value'])
        for year in range(1960, 2026):
            # t = year - 1960
            t = year - 1960
            # cyclic component + trend + noise
            val = amplitude * math.sin(2 * math.pi * t / period) + trend * t + random.gauss(0, 0.5)
            writer.writerow([year, val])

# Generate representative human/nature datasets
# Human
generate_data('PlanetIQ/data/raw/conflict.csv', period=9.0, amplitude=5, trend=0.1)
generate_data('PlanetIQ/data/raw/population.csv', period=20.0, amplitude=2, trend=0.5)
generate_data('PlanetIQ/data/raw/energy.csv', period=10.0, amplitude=3, trend=0.8)

# Nature
generate_data('PlanetIQ/data/raw/biodiversity.csv', period=9.0, amplitude=4, trend=-0.05)
