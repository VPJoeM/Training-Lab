#!/bin/bash
echo ""
if command -v dcgmi &>/dev/null; then
    echo "✓ DCGM is installed"
    echo ""
    echo "Key points:"
    echo "  • L1 = quick health check (~1 min)"
    echo "  • L2 = hardware diagnostics (~2 min)"  
    echo "  • L3 = stress test (~12 min)"
    echo "  • Pass = healthy, Fail = investigate"
else
    echo "⚠ DCGM not found - did you install it?"
fi
echo ""
