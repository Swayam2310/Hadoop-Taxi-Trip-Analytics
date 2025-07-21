#!/bin/bash

hadoop fs -mkdir -p /Input
hadoop fs -put -f Trips.txt /Input/
hadoop fs -put -f Taxis.txt /Input/
# Clean up previous output
hadoop fs -rm -r /Output/Task1

# Run the Hadoop streaming job
hadoop jar ./hadoop-streaming-3.1.4.jar \
    -D stream.num.map.output.key.fields=2 \
    -D mapreduce.job.reduces=3 \
    -file ./Task1-mapper.py \
    -mapper ./Task1-mapper.py \
    -file ./Task1-reducer.py \
    -reducer ./Task1-reducer.py \
    -input /Input/Trips.txt \
    -output /Output/Task1

# Ensure that the output directory exists
hadoop fs -test -d /Output/Task1
if [ $? -eq 0 ]; then
    # Merge all part files into a single local file
    hadoop fs -getmerge /Output/Task1/part-* ./Task1_output.txt
    echo "Output has been merged and saved to Task1_output.txt"
else
    echo "Output directory /Output/Task1 does not exist."
fi
