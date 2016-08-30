#!/usr/bin/env bash

for i in `seq 25`;
do
    { time radical-synapse-emulate -i 84.json ; } 2>> time_results; 
done

sed -n '/cannot/!p' time_results | sed -n '/open/!p' | grep . > time_results_cleaned
