# simulateur_trafic/core/cython_helpers.pyx
# cython: boundscheck=False
# cython: wraparound=False

from cpython cimport bool
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def compute_mean_density_cy(double[:] vehicle_counts, double[:] lengths_m) -> double:
    """
    Cython fast computation of mean density (vehicles per km).
    Accepts memoryviews of doubles. vehicle_counts should be floats or ints cast to double.
    """
    cdef Py_ssize_t n = vehicle_counts.shape[0]
    if n == 0:
        return 0.0

    cdef double total_density = 0.0
    cdef Py_ssize_t valid_routes = 0
    cdef Py_ssize_t i
    cdef double cnt, length_km, length

    for i in range(n):
        cnt = vehicle_counts[i]
        length = lengths_m[i]
        if length <= 0.0:
            continue
        length_km = length / 1000.0
        if length_km == 0.0:
            continue
        total_density += (cnt / length_km)
        valid_routes += 1

    if valid_routes == 0:
        return 0.0
    return total_density / valid_routes
