#!/bin/bash
hadoop fs -mkdir -p /Input
hadoop fs -put -f Trips.txt /Input/
hadoop fs -put -f Taxis.txt /Input/
# Remove existing output directories
hdfs dfs -rm -r /Output/Task3/IntermediateOutput
hdfs dfs -rm -r /Output/Task3/FinalSortedOutput

# Step 1: Run the main MapReduce job with multiple reducers (3 reducers)
hadoop jar ./hadoop-streaming-3.1.4.jar \
  -D mapreduce.job.reduces=3 \
  -files ./Task3-mapper.py,./Task3-reducer.py \
  -mapper "./Task3-mapper.py" \
  -reducer "./Task3-reducer.py" \
  -input /Input/Taxis.txt \
  -input /Input/Trips.txt \
  -output /Output/Task3/IntermediateOutput

# Final sorting with a single reducer to ensure global sorting
hadoop jar ./hadoop-streaming-3.1.4.jar \
  -D mapreduce.job.reduces=1 \
  -mapper "cat" \
  -reducer "sort -t ',' -k2,2n" \
  -input /Output/Task3/IntermediateOutput/part-* \
  -output /Output/Task3/FinalSortedOutput

# Fetch the final output
hdfs dfs -cat /Output/Task3/FinalSortedOutput/part-* > Task3_output.txt

