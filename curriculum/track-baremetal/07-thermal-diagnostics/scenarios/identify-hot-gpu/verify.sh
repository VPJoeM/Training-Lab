#!/bin/bash
[ -f "/tmp/.training_lab_hot_gpu" ] && echo "Lab active" && exit 0
exit 1
