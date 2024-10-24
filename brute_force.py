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

def findClosestPair(points):
    points = sorted(points, key=lambda point: point[0])
    points = np.array(points)
    print("Array: ", points)
    return closestPair(points)

def closestPair(points):
    if(len(points) == 2): # If there are 2 points in the set of points
        distance = np.linalg.norm(points[1] - points[0]) # Calculate d directly

        if(points[0][1] < points[1][1]): # Arrange the two points into a list Y sorted on y coordinate
            return distance, points
        else:
            Y = points
            return distance, Y[::-1]
    else:
        P_L = points[0 : len(points) // 2] # Divide the set into two equal-sized parts PL and PR
        P_R = points[len(points) // 2 : ]
        d1, YL = closestPair(P_L)
        d2, YR = closestPair(P_R)
        Y = np.concatenate((YL, YR), axis=0) # Merge the two sorted lists YL and YR into one sorted list Y
        Y = Y[Y[:, 1].argsort()]
        distance = np.min(np.array([d1, d2]))
        vert_line = (P_L[len(P_L) - 1][0] + P_R[0][0]) / 2
        S = list()
        for i in range(len(Y)):
            if(abs(Y[i][0] - vert_line) < distance): # Let S be the points in Y which are in the strip
                S.append(Y[i]) 
        S = np.array(S)
        for i in range(len(S) - 1):
            j = 1
            while(i+j < len(S) and j <= 7):
                if(np.linalg.norm(S[i] - S[i + j]) < distance):
                    distance = np.linalg.norm(S[i] - S[i + j])
                j += 1
        print(f"S: {S}")

        return distance, Y

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

#save(test_algorithm(), "brute_force")

n = sys.argv[1]
array = generator(int(n))
print(f"Closest Pair: {findClosestPair(array)}")