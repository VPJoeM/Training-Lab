#!/bin/bash
# XID 79 Diagnosis Lab

MARKER="/tmp/.training_lab_xid79"

# check for existing XID 79
EXISTING=$(sudo dmesg | grep -i "xid.*79" | tail -1 || true)

if [ -n "$EXISTING" ]; then
    GPU=$(echo "$EXISTING" | grep -oP 'PCI:[0-9a-f:.]+' | head -1 || echo "unknown")
    echo "existing=true" > "$MARKER"
    echo "gpu=$GPU" >> "$MARKER"
else
    # inject fake XID 79
    GPUS=("0000:18:00.0" "0000:2a:00.0" "0000:3b:00.0" "0000:86:00.0")
    GPU="${GPUS[$((RANDOM % 4))]}"
    TS=$(awk '{print $1}' /proc/uptime)
    
    sudo sh -c "echo '<3>[$TS] NVRM: Xid (PCI:$GPU): 79, GPU has fallen off the bus.' > /dev/kmsg" 2>/dev/null
    echo "injected=true" > "$MARKER"
    echo "gpu=$GPU" >> "$MARKER"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  XID 79 DIAGNOSIS LAB"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  A GPU has fallen off the bus. Find it."
echo ""
echo "  1. Check dmesg for XID errors:"
echo "     sudo dmesg | grep -i xid"
echo ""
echo "  2. Note the PCI address and timestamp"
echo ""
echo "  When done, click 'Mark Complete' in the web UI."
echo "═══════════════════════════════════════════════════════"
echo ""
