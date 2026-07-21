import os
import numpy as np
from ingestion import DataIngestor
from causality_engine import check_phase_coherence, granger_causality

def run_systemic_analysis():
    ingestor = DataIngestor()
    
    # Load processed datasets
    datasets = {}
    data_dir = 'PlanetIQ/data/raw'
    if os.path.exists('cache_worldbank.json'):
        raw = ingestor.load_from_json('cache_worldbank.json')
        datasets['GDP'] = ingestor.preprocess_series(raw)
        
    for filename in os.listdir(data_dir):
        if filename.endswith(('.csv')):
            name = filename.split('.')[0]
            raw = ingestor.load_from_csv(os.path.join(data_dir, filename))
            datasets[name] = ingestor.preprocess_series(raw)
            
    keys = list(datasets.keys())
    n = len(keys)
    coherence_matrix = np.zeros((n, n))
    causality_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i == j: continue
            k1, k2 = keys[i], keys[j]
            # Coherence
            coherence_matrix[i, j] = check_phase_coherence(datasets[k1], datasets[k2], 9.0)
            # Causality: Does j cause i?
            causality_matrix[i, j] = granger_causality(np.array(list(datasets[k1].values())), 
                                                       np.array(list(datasets[k2].values())))
            
    print("\n--- Coupling Matrix (Phase Coherence, Lower = More Coupled) ---")
    print(f"{'':>20} " + " ".join(f"{k:>12}" for k in keys))
    for i in range(n):
        print(f"{keys[i]:>20} " + " ".join(f"{coherence_matrix[i,j]:>12.4f}" for j in range(n)))
        
    print("\n--- Causality Matrix (Granger, Higher = Stronger Influence) ---")
    print(f"{'':>20} " + " ".join(f"{k:>12}" for k in keys))
    for i in range(n):
        print(f"{keys[i]:>20} " + " ".join(f"{causality_matrix[i,j]:>12.4f}" for j in range(n)))

if __name__ == "__main__":
    run_systemic_analysis()
