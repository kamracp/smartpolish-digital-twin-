import numpy as np

def generate_alerts(amps, result, speed, base_speed, pressure):

    alerts = []
    avg = np.mean(amps)

    for i, val in enumerate(amps):
        if val < avg * 0.75:
            alerts.append(f"Head {i+1}: Abrasive worn")
        elif val > avg * 1.3:
            alerts.append(f"Head {i+1}: Overload")

    if speed > base_speed * 1.2:
        alerts.append("High speed → quality risk")

    if speed < base_speed * 0.8:
        alerts.append("Low speed → energy increase")

    if pressure < 3.5:
        alerts.append("Low pressure → poor finish")

    if pressure > 5:
        alerts.append("High pressure → wear risk")

    if result["energy"] > 1.2:
        alerts.append("High energy consumption")

    return alerts