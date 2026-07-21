# ResearchEngine

**Systemic Cycle Detection & Validation Pipeline**

This engine is a rigorous analytical framework designed to detect, validate, and map recurring periodicities (cycles) across complex human and natural datasets.

## Features
- **Data Ingestion Framework**: Standardizes heterogeneous historical data (JSON, CSV) with automatic interpolation and detrending.
- **Robust Analysis Engine**: Implements the Lomb–Scargle periodogram, ideal for finite, unevenly sampled time-series data.
- **Statistical Validation Suite**:
    - **AR(1) Red Noise Benchmarking**: Differentiates genuine cycles from inherent autocorrelation.
    - **Sliding-Window Stability Analysis**: Tests the persistence of cycles over time.
    - **Bootstrap Confidence Intervals**.
- **Systemic Mapping**:
    - **Phase Coherence Analysis**: Maps synchronization between disparate domains.
    - **Granger Causality Testing**: Quantifies directional influence between indicators.
- **Real-time Streaming**: Asynchronous ingestion and incremental spectral analysis framework.

## Project Structure
```
ResearchEngine/
├── ingestion.py          # Data standardization
├── analysis_engine.py    # Lomb-Scargle implementation
├── validation_suite.py   # Red-noise & AR(1) logic
├── causality_engine.py   # Coherence & Granger tests
├── run_pipeline.py       # Pipeline orchestrator
├── run_causality.py      # Systemic coupling analysis
└── realtime_pipeline.py  # Streaming architecture
```

## Quick Start
1. Place datasets in `PlanetIQ/data/raw/`.
2. Run the main batch pipeline:
   ```bash
   python3 run_pipeline.py
   ```
3. Run the systemic coupling analysis:
   ```bash
   python3 run_causality.py
   ```

---
*Developed for complex systemic research.*
