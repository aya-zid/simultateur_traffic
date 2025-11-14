# simulateur_trafic/core/numba_helpers.py
import numpy as np
from numba import njit, prange

@njit
def update_positions_numba(positions, speeds, limits, lengths, densities, variations, rand_flags, delta_t):
    """
    In-place update of positions and speeds (Numba JIT).
    All arguments are numpy arrays of dtype float64, except rand_flags which is int8/uint8 (0 or 1).
    """
    n = positions.shape[0]
    for i in range(n):
        v = speeds[i]
        if v == 0.0:
            v = limits[i] * 0.8
        vitesse_ms = v / 3.6
        distance = vitesse_ms * delta_t
        # apply supplied variation factor
        distance *= variations[i]

        # slow down logic
        if densities[i] > 20.0:
            distance *= 0.8
        elif positions[i] > lengths[i] * 0.8:
            distance *= 0.6

        # ensure not overshoot
        distance_max = lengths[i] - positions[i]
        if distance > distance_max:
            distance = distance_max

        positions[i] = positions[i] + distance

        # occasional speed adjustment, controlled by rand_flags array
        if rand_flags[i] == 1:
            if densities[i] < 10.0:
                speeds[i] = min(limits[i], speeds[i] * 1.05)
            elif densities[i] > 25.0:
                # ensure a minimum speed of 20
                speeds[i] = max(20.0, speeds[i] * 0.9)
    return positions, speeds
