# simulateur_trafic/core/fast_numba.py
import numpy as np

try:
    from .numba_helpers import update_positions_numba
    NUMBA_AVAILABLE = True
except Exception:
    update_positions_numba = None
    NUMBA_AVAILABLE = False

import random

def update_positions_py(positions, speeds, limits, lengths, densities, delta_t):
    """Pure-Python fallback (same semantics)."""
    n = len(positions)
    new_positions = positions[:]  # lists
    new_speeds = speeds[:]
    for i in range(n):
        v = new_speeds[i]
        if v == 0:
            v = limits[i] * 0.8
        vitesse_ms = v / 3.6
        distance = vitesse_ms * delta_t
        variation = random.uniform(0.7, 1.1)
        distance *= variation

        if densities[i] > 20:
            distance *= 0.8
        elif positions[i] > lengths[i] * 0.8:
            distance *= 0.6

        distance_max = lengths[i] - positions[i]
        if distance > distance_max:
            distance = distance_max

        new_positions[i] = positions[i] + distance

        if random.random() < 0.1:
            if densities[i] < 10:
                new_speeds[i] = min(limits[i], new_speeds[i] * 1.05)
            elif densities[i] > 25:
                new_speeds[i] = max(20, new_speeds[i] * 0.9)
    return new_positions, new_speeds

def update_positions(positions, speeds, limits, lengths, densities, delta_t):
    """
    Wrapper: tries to use Numba JIT; otherwise calls Python fallback.
    Input may be Python lists or numpy arrays.
    Returns (positions_array, speeds_array) as numpy arrays or lists (same types returned by underlying impl).
    """
    # ensure numpy arrays
    pos = np.ascontiguousarray(np.array(positions, dtype=np.float64))
    spd = np.ascontiguousarray(np.array(speeds, dtype=np.float64))
    lim = np.ascontiguousarray(np.array(limits, dtype=np.float64))
    lng = np.ascontiguousarray(np.array(lengths, dtype=np.float64))
    den = np.ascontiguousarray(np.array(densities, dtype=np.float64))

    if NUMBA_AVAILABLE:
        # generate variation factors and random flags in Python and pass to numba function
        variations = np.random.uniform(0.7, 1.1, size=pos.shape[0]).astype(np.float64)
        rand_flags = (np.random.random(size=pos.shape[0]) < 0.1).astype(np.int8)
        # call numba function (it modifies arrays in-place)
        update_positions_numba(pos, spd, lim, lng, den, variations, rand_flags, float(delta_t))
        return pos, spd
    else:
        new_positions, new_speeds = update_positions_py(list(pos), list(spd), list(lim), list(lng), list(den), delta_t)
        return np.array(new_positions, dtype=np.float64), np.array(new_speeds, dtype=np.float64)
