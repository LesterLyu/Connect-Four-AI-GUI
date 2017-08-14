#!/bin/bash

for difficulty in 1 2 3 4 5 6
do
    echo difficulty = $difficulty enable_prune=False
    /usr/bin/time -f "Memory used: %M bytes" python3.5 test_helper.py $difficulty
    echo ===================================
    echo difficulty = $difficulty enable_prune=True
    /usr/bin/time -f "Memory used: %M bytes" python3.5 test_helper.py $difficulty -p
    echo ===================================
done
