#!/usr/bin/env python3

import sys
from collections import defaultdict
from math import sqrt

# Function to calculate Euclidean distance between two points
def calculate_distance(point1, point2):
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Function to find the best medoid for a cluster
def find_best_medoid(points):
    min_cost = float('inf')
    best_medoid = None

    for candidate in points:
        total_cost = sum(calculate_distance(candidate, point) for point in points)
        if total_cost < min_cost:
            min_cost = total_cost
            best_medoid = candidate

    return best_medoid

def reducer():
    medoid_trip_dict = defaultdict(list)

    for line in sys.stdin:
        try:
            # Adjust parsing to handle the medoid correctly
            medoid, trip_details = line.strip().split('\t')
            medoid_x, medoid_y = map(float, medoid.split(','))
            dropoff_x, dropoff_y = map(float, trip_details.split(','))
            dropoff_point = (dropoff_x, dropoff_y)
            medoid_trip_dict[(medoid_x, medoid_y)].append(dropoff_point)
        except ValueError as e:
            print(f"Error processing line: {line}. Error: {e}", file=sys.stderr)
            continue

    # Check if each reducer processes data
    if not medoid_trip_dict:
        print("No data processed in this reducer.", file=sys.stderr)

    for medoid, points in medoid_trip_dict.items():
        best_medoid = find_best_medoid(points)
        if best_medoid:
            print(f"{best_medoid[0]},{best_medoid[1]}")

if __name__ == "__main__":
    reducer()
