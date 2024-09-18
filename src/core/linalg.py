from numba import njit as jit
import numpy as np


@jit
def norm(arr):
    return np.sqrt(arr @ arr)

@jit
def VecDiff(vec_i,vec_j):
    return vec_j - vec_i

@jit 
def VecMul1D(vec1,vec2):
    return np.transpose(vec1) @ vec2