#!/bin/bash
# verify the lab is set up correctly

MARKER="/tmp/.training_lab_ib_down"

if [ -f "$MARKER" ]; then
    DOWN_HCA=$(grep "down_hca" "$MARKER" | cut -d= -f2)
    echo "Lab active - $DOWN_HCA port 1 is marked as down"
    exit 0
else
    echo "Lab marker not found"
    exit 1
fi
