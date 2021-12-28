import numpy as np
import sys
import copy
import time

n = int(sys.argv[1])

cities = np.load("cities_data.npy")

print(cities)

def tsp_req(current, unvisited, sum, traveled_path):
    if len(unvisited) == 0:
        return (sum, traveled_path)
    else:
        best = 1000000
        best_path = []
        for elem in unvisited:
            tmp = copy.deepcopy(unvisited)
            tmp.remove(elem)
            (res, final_path) = tsp_req(elem, tmp, sum+cities[current,elem], traveled_path+[elem])
            if res < best:
                best = res
                best_path = final_path
        return (best, best_path)

start = time.time()
result, path = tsp_req(0, list(range(1,n)), 0, [])
measure = time.time() - start

print("Time [s]: " + str(measure))
print(result)
print(path)
