#!/bin/bash
MARKER="/tmp/.training_lab_hot_gpu"
FAKE_NVIDIA_SMI="/tmp/fake_nvidia_smi_thermal.sh"

# pick a random GPU to be hot
HOT_GPU=$((RANDOM % 8))
HOT_TEMP=$((84 + RANDOM % 6))

echo "hot_gpu=$HOT_GPU" > "$MARKER"
echo "hot_temp=$HOT_TEMP" >> "$MARKER"

cat > "$FAKE_NVIDIA_SMI" << WRAPPER
#!/bin/bash
HOT_GPU=\$(grep "hot_gpu" /tmp/.training_lab_hot_gpu | cut -d= -f2)
HOT_TEMP=\$(grep "hot_temp" /tmp/.training_lab_hot_gpu | cut -d= -f2)

echo "index, temperature.gpu, power.draw [W]"
for i in {0..7}; do
    if [ \$i -eq \$HOT_GPU ]; then
        TEMP=\$HOT_TEMP
        POWER=\$((670 + RANDOM % 15))
    else
        TEMP=\$((70 + RANDOM % 8))
        POWER=\$((690 + RANDOM % 15))
    fi
    printf "%d, %d, %d.00\n" \$i \$TEMP \$POWER
done
WRAPPER

chmod +x "$FAKE_NVIDIA_SMI"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  HOT GPU IDENTIFICATION LAB"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  One of the GPUs on this node is running hot."
echo "  Find which one."
echo ""
echo "  Command:"
echo "    $FAKE_NVIDIA_SMI"
echo ""
echo "  Look for:"
echo "    - Temperature > 83°C"
echo "    - Lower power draw than siblings"
echo ""
echo "  When done, click 'Mark Complete' in the web UI."
echo "═══════════════════════════════════════════════════════"
echo ""
