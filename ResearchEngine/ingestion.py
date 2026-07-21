import csv
import json
import math
import statistics
from collections import defaultdict

class DataIngestor:
    """Standardizes heterogeneous historical data sources without external dependencies."""
    
    def load_from_json(self, filepath, date_key='date', val_key='value'):
        """Loads WorldBank-style JSON files."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Expecting WorldBank format: [meta, data_list]
        records = data[1]
        
        series = {}
        for record in records:
            if record[val_key] is not None:
                series[int(record[date_key])] = float(record[val_key])
        return series

    def load_from_csv(self, filepath, date_col='Year', val_col='Value'):
        """Loads standardized CSV files."""
        series = {}
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    year = int(row[date_col])
                    val = float(row[val_col])
                    series[year] = val
                except (ValueError, KeyError):
                    continue
        return series

    def preprocess_series(self, series):
        """Standardizes: interpolates missing years and removes linear trend."""
        sorted_years = sorted(series.keys())
        min_year = sorted_years[0]
        max_year = sorted_years[-1]
        
        # Interpolation
        processed = {}
        for year in range(min_year, max_year + 1):
            if year in series:
                processed[year] = series[year]
            else:
                # Simple linear interpolation
                prev_year = max([y for y in series if y < year], default=min_year)
                next_year = min([y for y in series if y > year], default=max_year)
                
                if prev_year == next_year:
                    processed[year] = series[prev_year]
                else:
                    v1 = series[prev_year]
                    v2 = series[next_year]
                    processed[year] = v1 + (v2 - v1) * (year - prev_year) / (next_year - prev_year)
        
        # Detrending (Linear)
        years = sorted(processed.keys())
        values = [processed[y] for y in years]
        n = len(years)
        
        # Calculate regression slope/intercept
        x_mean = sum(range(n)) / n
        y_mean = sum(values) / n
        
        num = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
        den = sum((i - x_mean) ** 2 for i in range(n))
        
        slope = num / den
        intercept = y_mean - slope * x_mean
        
        detrended = {}
        for i, year in enumerate(years):
            trend = slope * i + intercept
            detrended[year] = values[i] - trend
            
        return detrended

# Test
if __name__ == "__main__":
    ingestor = DataIngestor()
    try:
        raw_series = ingestor.load_from_json('cache_worldbank.json')
        processed = ingestor.preprocess_series(raw_series)
        
        print(f"Processed GDP data ({len(processed)} years).")
        print(f"Range: {min(processed.keys())}-{max(processed.keys())}")
        
        # Verify first few values
        sorted_keys = sorted(processed.keys())
        for y in sorted_keys[:5]:
            print(f"{y}: {processed[y]:.4f}")
            
    except Exception as e:
        print(f"Error: {e}")
