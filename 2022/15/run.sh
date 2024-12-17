#!/bin/bash
START="$(date +%s)"
python3 solution.py
DURATION=$[ $(date +%s) - ${START} ]
echo ${DURATION}
