#!/bin/bash

# Create and upload input files
hadoop fs -mkdir -p /Input
hadoop fs -put -f Trips.txt /Input/
hadoop fs -put -f Taxis.txt /Input/
hadoop fs -put -f initialization.txt /Input/

# Remove any existing output directory
hadoop fs -rm -r /Output/Task2

# Variable to control iteration count
iteration=1
max_iterations=$(head -n 1 initialization.txt) # Number of iterations from initialization.txt

# Run multiple iterations
while [ $iteration -le $max_iterations ]
do
  echo "Iteration: $iteration"
  
  # Hadoop Streaming Job with corrected options
  hadoop jar ./hadoop-streaming-3.1.4.jar \
    -D mapreduce.job.reduces=3 \
    -files Task2-mapper.py,Task2-reducer.py,initialization.txt \
    -input /Input/Trips.txt \
    -output /Output/Task2 \
    -mapper Task2-mapper.py \
    -reducer Task2-reducer.py \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

  # Check if the job was successful
  if [ $? -eq 0 ]; then
    echo "Hadoop job completed successfully for iteration $iteration."
  else
    echo "Hadoop job failed during iteration $iteration."
    exit 1
  fi
  
  # Increment the iteration count
  iteration=$((iteration + 1))

  # Remove the output directory for the next iteration, if not the last iteration
  if [ $iteration -le $max_iterations ]; then
    hadoop fs -rm -r /Output/Task2
  fi
done

# Merge part files from the final successful iteration into Task2_output.txt
hadoop fs -getmerge /Output/Task2/part-* Task2_output.txt
echo "Final output saved in Task2_output.txt. Use 'cat Task2_output.txt' to see the results."
