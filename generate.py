import sys
import numpy as np
import random

n = int(sys.argv[1])

arr = np.empty((n,n), dtype='i')

for i in range(n):
    for j in range(i):
        value = random.randint(1,100)
        arr[i,j] = value
        arr[j,i] = value
    arr[i,i] = 1000000

np.save("cities_data", arr)
