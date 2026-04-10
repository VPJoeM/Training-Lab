#!/bin/bash
MARKER="/tmp/.training_lab_driver_mismatch"
[ -f "$MARKER" ] && echo "Lab active - driver 550 vs FM 535 mismatch" && exit 0
echo "Lab marker not found" && exit 1
