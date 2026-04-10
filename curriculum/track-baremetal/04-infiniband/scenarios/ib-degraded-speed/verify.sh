#!/bin/bash
MARKER="/tmp/.training_lab_ib_degraded"

if [ -f "$MARKER" ]; then
    DEGRADED_HCA=$(grep "degraded_hca" "$MARKER" | cut -d= -f2)
    echo "Lab active - $DEGRADED_HCA is running at HDR (200) instead of NDR (400)"
    exit 0
else
    echo "Lab marker not found"
    exit 1
fi
