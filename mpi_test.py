import sys 
from master_worker_mpi import MasterWorkerMPI

""" Script to test function MasterWorkerMPI"""

def test_func(x, m, b):
    return m * x[0] + b

number_of_jobs = int(sys.argv[1])

m, b = -2., 10.
x0, xf = 0., 10.
dx = (xf - x0) / (number_of_jobs - 1)

jobs = [(x0 + i * dx,) for i in range(number_of_jobs)]

# Run jobs in parallel
results = MasterWorkerMPI(jobs, test_func, m, b)

keys = sorted(results.keys())
for key in keys:
    print '',key, results[key]




