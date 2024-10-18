import random
import math
import time
import matplotlib.pyplot as plt
import numpy as np

# Function to generate random points in a 2D plane
def generate_points(n):
    points = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(n)]
    return points

# Brute force closest pair algorithm
def brute_force_closest_pair(points):
    min_distance = float('inf')
    closest_pair = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = euclidean_distance(points[i], points[j])
            if distance < min_distance:
                min_distance = distance
                closest_pair = (points[i], points[j])
    return min_distance, closest_pair

# Euclidean distance function
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Optimized closest pair algorithm using divide and conquer
def closest_pair(points):
    points.sort(key=lambda x: x[0])  # Sort points by x-coordinate
    return closest_pair_recursive(points)

def closest_pair_recursive(points):
    if len(points) <= 3:
        return brute_force_closest_pair(points)
    
    mid = len(points) // 2
    mid_point = points[mid]

    left_closest = closest_pair_recursive(points[:mid])
    right_closest = closest_pair_recursive(points[mid:])

    min_closest = min(left_closest, right_closest, key=lambda x: x[0])

    # Consider points near the middle strip
    strip = [point for point in points if abs(point[0] - mid_point[0]) < min_closest[0]]
    strip.sort(key=lambda x: x[1])  # Sort by y-coordinate

    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if strip[j][1] - strip[i][1] > min_closest[0]:
                break
            distance = euclidean_distance(strip[i], strip[j])
            if distance < min_closest[0]:
                min_closest = (distance, (strip[i], strip[j]))

    return min_closest

# Function to time an algorithm
def time_algorithm(algorithm, points):
    start_time = time.time()
    result = algorithm(points)
    end_time = time.time()
    return end_time - start_time, result

# Function to run experiments and plot graphs
def run_experiments():
    sizes = [2**p for p in range(2, 12)]  # n = 2^p where p ranges from 2 to 11
    brute_force_times = []
    optimized_times = []

    for n in sizes:
        points = generate_points(n)
        
        # Time brute force approach
        bf_time, _ = time_algorithm(brute_force_closest_pair, points)
        brute_force_times.append(bf_time)
        
        # Time optimized divide and conquer approach
        opt_time, _ = time_algorithm(closest_pair, points)
        optimized_times.append(opt_time)

        print(f"n = {n}: Brute force time = {bf_time:.5f}s, Optimized time = {opt_time:.5f}s")

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, brute_force_times, label="Brute Force", marker='o')
    plt.plot(sizes, optimized_times, label="Divide and Conquer", marker='o')
    plt.title('Runtime Comparison: Brute Force vs Optimized Closest Pair Algorithm')
    plt.xlabel('Number of Points (n)')
    plt.ylabel('Time (seconds)')
    plt.xscale('log', base=2)
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.show()

# Run the experiment and plot the graph
if __name__ == "__main__":
    run_experiments()