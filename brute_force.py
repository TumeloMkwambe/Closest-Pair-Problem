import sys
import math
import time
import random
import numpy as np


def generator(n):
    List = list()
    i = 0
    while len(List) != n:
        x = random.randint(0, n**2)
        y = random.randint(0, n**2)
        entry = (x, y)
        if entry not in List:
            List.append(entry)
            i = i + 1
    return List

def brute_force(points):
    points = np.array(points)
    distance = np.linalg.norm(points[1] - points[0])
    for i in range(1, len(points) - 1, 1):
        for j in range(1 + 1, len(points), 1):
            curr = np.linalg.norm(points[i] - points[j])
            if curr < distance:
                distance = curr
    return curr

def timer(function, points):
    start = time.time()
    function(points)
    stop = time.time() - start
    return stop

def test_algorithm():
    runtimes = list()
    p = 2
    while p <= 13:
        points = generator(2**p)
        runtimes.append([p, timer(brute_force, points)])
        print(p)
        p += 1
    return runtimes

def save(array, sort):
    np.savetxt(sort, array, delimiter=',', header="input,time")

save(test_algorithm(), "brute_force")