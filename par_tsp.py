import numpy as np
import sys
import copy
import time
from mpi4py import MPI

def tsp_req(current, unvisited, sum, traveled_path, bound):
    if sum >= bound:
        return (10000000, [])
    if len(unvisited) == 0:
        return (sum, traveled_path)
    else:
        best = 1000000
        best_path = []
        for elem in unvisited:
            tmp = copy.deepcopy(unvisited)
            tmp.remove(elem)
            (res, final_path) = tsp_req(elem, tmp, sum+cities[current,elem], traveled_path+[elem], bound)
            if res < bound and (res < best):
                best = res
                best_path = final_path
        return (best, best_path)

def create_tsp(current, unvisited, sum, traveled_path, level):
    if level == 0:
        return [(current, unvisited, sum, traveled_path)]
    else:
        all_paths = []
        for elem in unvisited:
            tmp = copy.deepcopy(unvisited)
            tmp.remove(elem)
            paths = create_tsp(elem, tmp, sum+cities[current,elem], traveled_path+[elem], level-1)
            all_paths = all_paths + paths
        return all_paths

def main(level, n, number_of_cores, comm):
    start = time.time()
    paths = create_tsp(0, list(range(1,n)), 0, [], level)
    bound = 1000000
    best_path = []
    for i in range(1,number_of_cores):
        path = paths.pop()
        comm.send([(path[0], path[1], path[2], path[3], bound), False], dest = i)
    #until scheduler has tasks to assign
    while len(paths) != 0:
        result = comm.recv()
        if result[0] < bound:
            bound = result[0]
            best_path = result[1]
        next_path = paths.pop()
        comm.send([(next_path[0], next_path[1], next_path[2], next_path[3], bound), False], dest = result[2])
    for i in range(1,number_of_cores):
        result = comm.recv(source = i)
        if result[0] < bound:
            bound = result[0]
            best_path = result[1]
        comm.send((None, True), dest=i)
    print(best_path)
    print(bound)
    measure = time.time() - start
    print("Time [s]: " + str(measure))



def secondary(comm, rank):
    msg = comm.recv(source=0)
    done = msg[1]
    while not done:
        (current, unvisited, sum, traveled_path, bound) = msg[0]
        res, path = tsp_req(current, unvisited, sum, traveled_path, bound)
        comm.send((res,path, rank), dest=0)
        msg = comm.recv(source=0)
        done = msg[1]


if __name__ == '__main__':
    start = time.time()

    cities = np.load("cities_data.npy")
    n = int(sys.argv[1])
    level = int(sys.argv[2])
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    number_of_cores = comm.Get_size()

    if rank == 0:
        main(level, n, number_of_cores, comm)
    else:
        secondary(comm, rank)
