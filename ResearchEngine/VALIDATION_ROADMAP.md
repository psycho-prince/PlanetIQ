# Mechanistic Validation Roadmap

Following the identification of a systemic ~9–10 year periodicity, we transition from statistical observation to mechanistic validation.

## Phase 1: Reproducibility
- [ ] Freeze datasets (Archive `PlanetIQ/data/raw/` in a dedicated version).
- [ ] Document processing parameters (Sliding window sizes, AR(1) estimation methods).
- [ ] Implement automated regression tests for the entire pipeline to ensure findings hold under code changes.

## Phase 2: Causal Modeling (System Dynamics)
- [ ] Build a structural system dynamics model incorporating:
    - Climate, Agricultural Production, Food Prices, Political Instability, GDP/Investment.
- [ ] Simulate the model to determine if the 9-year oscillation emerges endogenously (without exogenous drivers).

## Phase 3: Out-of-Sample Testing
- [ ] Perform a "Backtesting" challenge:
    - Train mechanistic model on 1960–2000.
    - Forecast 2001–2025.
    - Evaluate against observed data.

## Phase 4: Independent Replication
- [ ] Re-run pipeline on regional/individual country data.
- [ ] Compare results from independent historical data providers.
