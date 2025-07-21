#!/usr/bin/env python3
import sys

current_taxi_id = None
current_trip_type = None
trip_count = 0
total_fare = 0.0
max_fare = -float('inf')
min_fare = float('inf')

def output_result(taxi_id, trip_type, trip_count, total_fare, max_fare, min_fare):
    if trip_count > 0:
        average_fare = total_fare / trip_count
        print(f"{taxi_id}\t{trip_type}\t{trip_count}\t{max_fare:.2f}\t{min_fare:.2f}\t{average_fare:.2f}")

# Read input from standard input
for line in sys.stdin:
    line = line.strip()
    parts = line.split('\t')

    if len(parts) == 6:
        taxi_id, trip_type, count, fare_sum, max_f, min_f = parts
        
        try:
            count = int(count)
            fare_sum = float(fare_sum)
            max_f = float(max_f)
            min_f = float(min_f)

            if current_taxi_id == taxi_id and current_trip_type == trip_type:
                trip_count += count
                total_fare += fare_sum
                max_fare = max(max_fare, max_f)
                min_fare = min(min_fare, min_f)
            else:
                if current_taxi_id is not None:
                    output_result(current_taxi_id, current_trip_type, trip_count, total_fare, max_fare, min_fare)
                
                current_taxi_id = taxi_id
                current_trip_type = trip_type
                trip_count = count
                total_fare = fare_sum
                max_fare = max_f
                min_fare = min_f

        except ValueError:
            continue  # Skip lines where conversion fails

# Output the last taxi_id and trip_type's results
if current_taxi_id and current_trip_type:
    output_result(current_taxi_id, current_trip_type, trip_count, total_fare, max_fare, min_fare)
