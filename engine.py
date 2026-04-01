import numpy as np

def calculate(amps, production):
    total_kw = np.sum(amps) * 1.1
    energy = (total_kw * 24) / production
    efficiency = total_kw / 500 * 100

    return {
        "power": total_kw,
        "energy": energy,
        "efficiency": efficiency
    }