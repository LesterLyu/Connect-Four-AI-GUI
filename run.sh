#!/bin/bash

if [ $# -eq 1 ] && [ $1 = "-t" ];
then
    python3.5 connect_four.py
else
    python3.5 gui.py
fi