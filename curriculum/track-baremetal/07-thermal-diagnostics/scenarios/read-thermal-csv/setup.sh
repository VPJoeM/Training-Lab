#!/bin/bash
MARKER="/tmp/.training_lab_thermal_csv"
FAKE_CSV="/tmp/thermal_results_lab.csv"

# pick a random GPU to be the hot one
HOT_GPU=$((RANDOM % 8))

echo "hot_gpu=$HOT_GPU" > "$MARKER"

# create fake thermal CSV
cat > "$FAKE_CSV" << EOF
timestamp,gpu_id,gpu_temp,mem_temp,power_draw,gpu_util
EOF

for i in {0..7}; do
    if [ $i -eq $HOT_GPU ]; then
        TEMP=$((83 + RANDOM % 5))
        MEM_TEMP=$((TEMP - 4))
        POWER=$((670 + RANDOM % 20))
    else
        TEMP=$((70 + RANDOM % 8))
        MEM_TEMP=$((TEMP - 4))
        POWER=$((690 + RANDOM % 15))
    fi
    echo "2024-01-15 10:30:00,$i,$TEMP,$MEM_TEMP,$POWER,100" >> "$FAKE_CSV"
done

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  THERMAL CSV ANALYSIS LAB"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  A thermal test was run on this node."
echo "  Review the results and find any issues."
echo ""
echo "  View the CSV:"
echo "    cat $FAKE_CSV"
echo "    column -t -s',' $FAKE_CSV"
echo ""
echo "  Look for:"
echo "    - gpu_temp > 83°C"
echo "    - Abnormal power draw"
echo "    - Outliers vs other GPUs"
echo ""
echo "  When done, click 'Mark Complete' in the web UI."
echo "═══════════════════════════════════════════════════════"
echo ""
