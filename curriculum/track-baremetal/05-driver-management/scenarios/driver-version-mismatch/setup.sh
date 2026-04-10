#!/bin/bash
# Driver Version Mismatch Lab

MARKER="/tmp/.training_lab_driver_mismatch"
FAKE_NVIDIA_SMI="/tmp/fake_nvidia_smi_driver.sh"
FAKE_DPKG="/tmp/fake_dpkg_driver.sh"

# simulate a mismatch - driver 550, FM 535
echo "driver_version=550.54.15" > "$MARKER"
echo "fm_version=535.129.03" >> "$MARKER"

cat > "$FAKE_NVIDIA_SMI" << 'WRAPPER'
#!/bin/bash
if [[ "$*" == *"--query-gpu=driver_version"* ]]; then
    echo "550.54.15"
else
    cat << 'EOF'
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 550.54.15              Driver Version: 550.54.15    CUDA Version: 12.4     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
|=========================================+========================+======================|
|   0  NVIDIA H100 80GB HBM3          On  | 00000000:18:00.0   Off |                    0 |
|   1  NVIDIA H100 80GB HBM3          On  | 00000000:2A:00.0   Off |                    0 |
|   2  NVIDIA H100 80GB HBM3          On  | 00000000:3B:00.0   Off |                    0 |
|   3  NVIDIA H100 80GB HBM3          On  | 00000000:86:00.0   Off |                    0 |
+-----------------------------------------+------------------------+----------------------+
EOF
fi
WRAPPER

cat > "$FAKE_DPKG" << 'WRAPPER'
#!/bin/bash
if [[ "$*" == *"fabricmanager"* ]]; then
    echo "ii  nvidia-fabricmanager-535  535.129.03-1  amd64  Fabric Manager for NVSwitch"
else
    /usr/bin/dpkg "$@"
fi
WRAPPER

chmod +x "$FAKE_NVIDIA_SMI" "$FAKE_DPKG"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  DRIVER VERSION MISMATCH LAB"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  Multi-GPU training is failing on this node."
echo "  Check for a driver/Fabric Manager version mismatch."
echo ""
echo "  Commands to use:"
echo "    $FAKE_NVIDIA_SMI --query-gpu=driver_version --format=csv,noheader"
echo "    $FAKE_DPKG -l | grep fabricmanager"
echo ""
echo "  Compare the major version numbers."
echo ""
echo "  When done, click 'Mark Complete' in the web UI."
echo "═══════════════════════════════════════════════════════"
echo ""
