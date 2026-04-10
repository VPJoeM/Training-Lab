#!/bin/bash
[ -f "/tmp/.training_lab_fm_status" ] && echo "Lab active" && exit 0
exit 1
