import numpy as np
cimport numpy as np
from libcpp.vector cimport vector

# Cython wrapper for index.cpp functions

cdef extern from "index.h":
    int c2(int i, int j, int n)
    int c3(int i, int j, int k, int n)
    int c4(int i, int j, int k, int l, int n)
    int cinf(vector[int] index, int n)

def py_c2(int i, int j, int n):
    return c2(i, j, n)

def py_c3(int i, int j, int k, int n):
    return c3(i, j, k, n)

def py_c4(int i, int j, int k, int l, int n):
    return c4(i, j, k, l, n)

def py_cinf(np.ndarray[int, ndim=1] index, int n):
    return cinf(index, n)
