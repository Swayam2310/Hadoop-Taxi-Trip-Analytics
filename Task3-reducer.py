#!/usr/bin/env python3
import sys
from collections import defaultdict

# Initialize tracking variables
company_trip_count = defaultdict(int)

# Read each line from the mapper output
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue  # Skip empty lines

    # Split line into components
    try:
        taxi_id, record_type, value = line.split('\t')
    except ValueError:
        print(f'DEBUG: Skipping malformed line -> {line}', file=sys.stderr)
        continue

    # Handle TAXI records
    if record_type == 'TAXI':
        current_company = value
        current_taxi_id = taxi_id

    # Handle TRIP records
    elif record_type == 'TRIP':
        trip_count = int(value)
        # Add trip count to the corresponding company
        if current_company:
            company_trip_count[current_company] += trip_count

# Sort the companies by trip count in ascending order
sorted_trip_counts = sorted(company_trip_count.items(), key=lambda x: (x[1], int(x[0])))

# Emit sorted results
for company_id, total_trips in sorted_trip_counts:
    print(f"{company_id},{total_trips}")
    print(f"DEBUG: Emitting sorted result -> {company_id},{total_trips}", file=sys.stderr)
