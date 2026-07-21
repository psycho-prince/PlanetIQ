# Mechanistic Validation Roadmap

Following the identification of a systemic ~9–10 year periodicity, we transition from statistical observation to rigorous falsification and mechanistic modeling.

## Phase 1: Reproducibility & Backtesting
- [x] Freeze datasets (Archive `PlanetIQ/data/raw/`).
- [x] Implement automated regression tests (Backtesting suite).
- [ ] Ensure all code and results are reproducible with seeded randomness.

## Phase 2: Mechanistic Modeling (Systems Dynamics)
- [ ] Build structural system dynamics model incorporating causal links:
    - Climate -> Agriculture -> Food Prices -> Conflict -> GDP -> Adaptation -> Climate.
- [ ] Simulate the model to check if endogenous ~9-year oscillations emerge.

## Phase 3: Falsification & Rigor
- [ ] **Sensitivity Analysis**: Vary parameters (±10–50%) to test stability of the cycle.
- [ ] **Baseline Comparison**: Compare cycle-based model performance vs. Linear Trends and Standard AR models.
- [ ] **Out-of-sample Validation (Backtesting)**: Train on 1960–2000; test on 2001–2025.
- [ ] **Uncertainty Quantification**: Calculate confidence intervals for all spectral peaks and causal indices.

## Phase 4: Independent Replication
- [ ] Re-run pipeline on regional/individual country data.
- [ ] Compare results from independent historical data providers (e.g., FAO, World Bank, local climate archives).
