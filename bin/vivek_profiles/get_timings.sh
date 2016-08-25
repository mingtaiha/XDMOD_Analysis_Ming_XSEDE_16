#!/usr/bin/env bash

for file in `ls *.json`;
do
    echo $file >> time_results
    { time radical-synapse-emulate -i $file ; } 2>> time_results; 
done
