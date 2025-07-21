#!/usr/bin/env python3
import sys
from collections import defaultdict

# Initialize dictionaries to hold data for in-mapper combining
trip_counts = defaultdict(lambda: defaultdict(int))
total_fares = defaultdict(lambda: defaultdict(float))
max_fares = defaultdict(lambda: defaultdict(lambda: -float('inf')))
min_fares = defaultdict(lambda: defaultdict(lambda: float('inf')))

def classify_trip(distance):
    if distance >= 200:
        return 'long trips'
    elif 100 <= distance < 200:
        return 'medium trips'
    else:
        return 'short trips'

# Read input from standard input
for line in sys.stdin:
    line = line.strip()
    parts = line.split(',')

    if len(parts) == 8:  # Ensure the line has the expected number of fields
        trip_id, taxi_id, fare, distance, pickup_x, pickup_y, dropoff_x, dropoff_y = parts
        
        try:
            distance = float(distance)
            fare = float(fare)
            trip_type = classify_trip(distance)

            # Update counts and fares in the mapper
            trip_counts[taxi_id][trip_type] += 1
            total_fares[taxi_id][trip_type] += fare
            max_fares[taxi_id][trip_type] = max(max_fares[taxi_id][trip_type], fare)
            min_fares[taxi_id][trip_type] = min(min_fares[taxi_id][trip_type], fare)
            
        except ValueError:
            continue  # Skip lines where conversion fails

# Emit the combined data
for taxi_id in trip_counts:
    for trip_type in trip_counts[taxi_id]:
        avg_fare = total_fares[taxi_id][trip_type] / trip_counts[taxi_id][trip_type]
        print(f"{taxi_id}\t{trip_type}\t{trip_counts[taxi_id][trip_type]}\t{total_fares[taxi_id][trip_type]:.2f}\t{max_fares[taxi_id][trip_type]:.2f}\t{min_fares[taxi_id][trip_type]:.2f}")
