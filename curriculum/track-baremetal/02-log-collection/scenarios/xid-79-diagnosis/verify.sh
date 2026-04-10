#!/bin/bash
# XID 79 - Verification

MARKER="/tmp/.training_lab_xid79"

if [ -f "$MARKER" ]; then
    source "$MARKER"
    echo ""
    echo "✓ Lab complete!"
    echo "  XID 79 was at: $gpu"
    echo ""
    echo "  Key points:"
    echo "  • XID 79 = GPU lost PCIe link"
    echo "  • Check timestamp (fresh vs stale)"
    echo "  • Next: power cycle via iDRAC"
    echo ""
else
    echo "XID 79 found in dmesg:"
    sudo dmesg | grep -i "xid.*79" | tail -3 || echo "(none)"
    echo ""
fi
