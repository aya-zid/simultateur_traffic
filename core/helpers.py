# simulateur_trafic/core/helpers.py
from typing import List

def compute_mean_density_py(vehicle_counts: List[int], lengths_m: List[float]) -> float:
    """
    Pure-Python reference: compute mean density (vehicles per km)
    vehicle_counts: list of ints (# vehicles on each route)
    lengths_m: list of floats (lengths in meters)
    """
    if not vehicle_counts:
        return 0.0
    total_density = 0.0
    valid_routes = 0
    for cnt, length in zip(vehicle_counts, lengths_m):
        if length <= 0:
            continue
        length_km = length / 1000.0
        density = cnt / length_km if length_km != 0 else 0.0
        total_density += density
        valid_routes += 1
    return (total_density / valid_routes) if valid_routes > 0 else 0.0
