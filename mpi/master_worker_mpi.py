from mpi4py import MPI

def MasterWorkerMPI(jobs, runJob, *args):
    """ Runs a series of jobs in master / worker parallel mode

    Thanks to Misha Salim github/masalim2 for input

    Args:
        jobs: iterable of hashable items which specify job to be run
        runJob: function which runs a job 
        *args: optional arguments to runJob. 
               useful for parameters which 
               are constant across all jobs
    Returns:
        results: dictionary of results key = job
    """

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nprocs = comm.Get_size()
    stat = MPI.Status()

    RUN = 1
    STOP = 0

    # Dictionary for results
    results = {}

    if nprocs == 1:
        # Only 1 processor / Run jobs in serial
        for job in jobs:
            results[job] = runJob(job, *args)
    elif rank == 0:
        # Master thread / distribute work to workers
        if rank == 0:
            # Send out initial job to each processor
            num_jobs = len(jobs)
            for job_index in range(nprocs - 1):
                comm.send(job_index, dest=job_index + 1, tag=RUN)
                
            # Give out rest of work as workers become available
            job_index = nprocs
            while job_index < num_jobs:
                (job, result) = comm.recv(source=MPI.ANY_SOURCE,
                                   tag=MPI.ANY_TAG, status=stat)
                results[job] = result
                
                comm.send(job_index, dest=stat.Get_source(),tag=RUN)
                job_index += 1

            # Pick Up Final Results / Tell workers to stop
            for i in range(1, nprocs):
                (job, result) = comm.recv(source=MPI.ANY_SOURCE,
                                   tag=MPI.ANY_TAG, status=stat)
                results[job] = result
                comm.send("", dest=stat.Get_source(), tag=STOP)
    else:
        # Worker thread
        job_index = comm.recv(source=0, tag=MPI.ANY_TAG, status=stat)
        while stat.Get_tag():
            job = jobs[job_index]
            result = runJob(job, *args)
            comm.send((job, result), dest=0)
            job_index = comm.recv(source=0, tag=MPI.ANY_TAG, status=stat)

    return results




