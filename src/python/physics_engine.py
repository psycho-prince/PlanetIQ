import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def pipeline_dynamics(state, t, pump_speed, pipe_resistance=0.1, max_pressure=1000.0):
    pressure, flow_rate = state
    d_flow = pump_speed * 0.001 - pipe_resistance * flow_rate
    d_pressure = flow_rate - 0.05 * pressure
    
    if pressure > max_pressure:
        print(f"WARNING: Pressure exceeded limit! {pressure:.2f} > {max_pressure}")
    
    return [d_pressure, d_flow]

def simulate_command(pump_speed_rpm, duration=10.0, max_safe_pressure=800.0):
    t = np.linspace(0, duration, 100)
    initial_state = [100.0, 10.0]
    
    sol = odeint(pipeline_dynamics, initial_state, t, args=(pump_speed_rpm,))
    pressures = sol[:, 0]
    max_p = np.max(pressures)
    
    print(f"Simulated pump speed: {pump_speed_rpm} RPM")
    print(f"Max pressure: {max_p:.2f} (Safe limit: {max_safe_pressure})")
    
    is_safe = max_p <= max_safe_pressure
    if not is_safe:
        print("CATASTROPHIC FAILURE PREDICTED - Packet should be DROPPED")
    else:
        print("Command is SAFE")
    
    plt.figure(figsize=(10, 6))
    plt.plot(t, pressures, label='Pressure')
    plt.axhline(max_safe_pressure, color='r', linestyle='--', label='Safety Limit')
    plt.xlabel('Time (s)')
    plt.ylabel('Pressure')
    plt.title(f'Physics Simulation for Pump Speed {pump_speed_rpm} RPM')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'sim_pump_{pump_speed_rpm}.png')
    plt.show()
    
    return is_safe, max_p

if __name__ == "__main__":
    print("=== VoltGuard: Physics Simulation ===\n")
    print("Normal operation:")
    simulate_command(1200)
    
    print("\nMalicious command:")
    simulate_command(50000)
