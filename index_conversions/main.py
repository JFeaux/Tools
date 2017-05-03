import sys
import numpy as np
import index_wrap
 
""" 
Script to illustrate usage of index conversion functions from index.cpp
See index.cpp for description
"""


i = int(sys.argv[1])
j = int(sys.argv[2])
size = int(sys.argv[3])

idx1 = index_wrap.py_c2(i, j, size)
idx2 = index_wrap.py_cinf(np.array([i, j], dtype=np.int32), size)

print '{} {} : {} {}'.format(i, j, idx1, idx2)




