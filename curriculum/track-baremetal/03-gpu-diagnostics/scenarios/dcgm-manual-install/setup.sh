#!/bin/bash
# Manual DCGM Install Lab

DCGM=$(command -v dcgmi &>/dev/null && echo "yes" || echo "no")

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  MANUAL DCGM INSTALL & L1 TEST"
echo "  DCGM currently installed: $DCGM"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  1. Check if DCGM is installed:"
echo "     which dcgmi"
echo ""
if [ "$DCGM" = "no" ]; then
echo "  2. Install DCGM (not installed - you'll need to do this):"
echo "     # Get CUDA version"
echo "     CUDA_VERSION=\$(nvidia-smi | grep -oP 'CUDA Version: \\K[0-9]+')"
echo "     # Install keyring if needed"
echo "     sudo apt-get install -y cuda-keyring"
echo "     # Install DCGM"
echo "     sudo apt-get install -y datacenter-gpu-manager"
echo ""
else
echo "  2. DCGM is already installed - skip to step 3"
echo ""
fi
echo "  3. Run L1 health check:"
echo "     sudo dcgmi diag -r 1"
echo ""
echo "  When done, click 'Mark Complete' in the web UI."
echo "═══════════════════════════════════════════════════════"
echo ""
