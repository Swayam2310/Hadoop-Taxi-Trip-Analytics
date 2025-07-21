#!/usr/bin/env python3
import sys

# Mapper script that handles both join and count operations

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue  # Skip empty lines
    
    # Split the line by comma to identify its source
    values = line.split(',')

    # Check if line is from Taxis.txt (4 columns)
    if len(values) == 4:
        taxi_id, company, model, year = values
        print(f'{taxi_id}\tTAXI\t{company}')
        print(f'DEBUG: Taxis.txt -> taxi_id: {taxi_id}, company: {company}', file=sys.stderr)

    # Check if line is from Trips.txt (8 columns)
    elif len(values) == 8:
        trip_id, taxi_id, fare, distance, pickup_x, pickup_y, dropoff_x, dropoff_y = values
        print(f'{taxi_id}\tTRIP\t1')
        print(f'DEBUG: Trips.txt -> taxi_id: {taxi_id}, trip_id: {trip_id}', file=sys.stderr)

    # Handle unrecognized formats
    else:
        print(f'DEBUG: Unrecognized line format -> {line}', file=sys.stderr)
