#!/bin/bash
[ -f "/tmp/.training_lab_thermal_csv" ] && echo "Lab active" && exit 0
exit 1
