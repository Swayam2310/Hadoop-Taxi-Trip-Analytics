#!/usr/bin/env python3

import sys
import math

# Function to calculate Euclidean distance between two points
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Function to read the initialization file
def read_initialization():
    with open('initialization.txt', 'r') as f:
        lines = f.readlines()
    v = int(lines[0].strip())  # Number of iterations
    medoids = [tuple(map(float, line.strip().split())) for line in lines[1:]]
    return v, medoids

# Initialize medoids
v, medoids = read_initialization()

# Mapper Function
for line in sys.stdin:
    fields = line.strip().split(',')

    # Skip lines that do not have the expected number of fields
    if len(fields) < 8:
        continue

    # Extracting necessary fields
    trip_id = fields[0]
    dropoff_x, dropoff_y = float(fields[6]), float(fields[7])
    dropoff_location = (dropoff_x, dropoff_y)

    # Finding the closest medoid
    min_distance = float('inf')
    closest_medoid = None

    # Loop through each medoid to find the closest one
    for medoid in medoids:
        distance = euclidean_distance(dropoff_location, medoid)
        if distance < min_distance:
            min_distance = distance
            closest_medoid = medoid

    # Output format: <medoid_x>,<medoid_y>\t<trip_id>,<dropoff_x>,<dropoff_y>
    if closest_medoid:
        medoid_x, medoid_y = closest_medoid
        print(f"{medoid_x},{medoid_y}\t{dropoff_x},{dropoff_y}")
