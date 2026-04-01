import numpy as np

def generate_data(base_speed, speed, removal, surface, pressure):

    np.random.seed(42)

    base_load = 30 + removal
    speed_factor = base_speed / speed
    surface_factor = 1.2 if surface == "DG" else 1.0
    pressure_factor = pressure / 4

    profile = np.linspace(1.3, 0.7, 24)

    amps = base_load * speed_factor * surface_factor * pressure_factor * profile
    amps += np.random.normal(0, 2, 24)

    return np.clip(amps, 20, 70)