# simulateur_trafic/core/fast_helpers.py
import numpy as np

try:
    from .cython_helpers import compute_mean_density_cy
    CYTHON_AVAILABLE = True
except Exception:
    compute_mean_density_cy = None
    CYTHON_AVAILABLE = False

from .helpers import compute_mean_density_py

def compute_mean_density(vehicle_counts, lengths_m):
    """
    Wrapper: use Cython if available, else Python.
    Accepts Python lists or numpy arrays.
    """
    if CYTHON_AVAILABLE:
        # ensure numpy arrays of type float64
        vc = np.ascontiguousarray(np.array(vehicle_counts, dtype=np.float64))
        lm = np.ascontiguousarray(np.array(lengths_m, dtype=np.float64))
        return float(compute_mean_density_cy(vc, lm))
    else:
        return compute_mean_density_py(vehicle_counts, lengths_m)
