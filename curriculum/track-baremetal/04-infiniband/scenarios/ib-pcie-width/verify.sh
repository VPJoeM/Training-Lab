#!/bin/bash
MARKER="/tmp/.training_lab_pcie_width"

if [ -f "$MARKER" ]; then
    DEGRADED_ADDR=$(grep "degraded_addr" "$MARKER" | cut -d= -f2)
    echo "Lab active - $DEGRADED_ADDR is running at x8 instead of x16"
    exit 0
else
    echo "Lab marker not found"
    exit 1
fi
