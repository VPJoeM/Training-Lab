#!/bin/bash
# PCIe Width Lab - simulate lspci output with degraded width

MARKER="/tmp/.training_lab_pcie_width"
FAKE_LSPCI="/tmp/fake_lspci_pcie.sh"

# pick a random HCA to have degraded width
ADDRESSES=("3b:00.0" "86:00.0" "af:00.0" "d8:00.0")
DEGRADED_ADDR="${ADDRESSES[$((RANDOM % 4))]}"

echo "degraded_addr=$DEGRADED_ADDR" > "$MARKER"

# create wrapper for lspci
cat > "$FAKE_LSPCI" << 'WRAPPER'
#!/bin/bash
# wrapper that shows degraded PCIe width on one HCA

DEGRADED_ADDR=$(grep "degraded_addr" /tmp/.training_lab_pcie_width 2>/dev/null | cut -d= -f2)

if [ "$1" = "-vv" ] && [ "$2" = "-s" ]; then
    ADDR="$3"
    # simulate detailed output for this address
    if [ "$ADDR" = "$DEGRADED_ADDR" ]; then
        WIDTH="x8"
        SPEED="16GT/s"
    else
        WIDTH="x16"
        SPEED="16GT/s"
    fi
    
    cat << EOF
$ADDR Infiniband controller: Mellanox Technologies MT2910 Family [ConnectX-7]
        Subsystem: Mellanox Technologies Device 0023
        Control: I/O- Mem+ BusMaster+ SpecCycle- MemWINV- VGASnoop- ParErr+ Stepping- SERR+ FastB2B- DisINTx+
        Status: Cap+ 66MHz- UDF- FastB2B- ParErr- DEVSEL=fast >TAbort- <TAbort- <MAbort- >SERR- <PERR- INTx-
        Latency: 0, Cache Line Size: 64 bytes
        NUMA node: 0
        LnkCap: Port #0, Speed 16GT/s, Width x16, ASPM not supported
        LnkSta: Speed $SPEED, Width $WIDTH
EOF
else
    # list mode
    cat << EOF
3b:00.0 Infiniband controller: Mellanox Technologies MT2910 Family [ConnectX-7]
86:00.0 Infiniband controller: Mellanox Technologies MT2910 Family [ConnectX-7]
af:00.0 Infiniband controller: Mellanox Technologies MT2910 Family [ConnectX-7]
d8:00.0 Infiniband controller: Mellanox Technologies MT2910 Family [ConnectX-7]
EOF
fi
WRAPPER

chmod +x "$FAKE_LSPCI"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  PCIE WIDTH CHECK LAB"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  One HCA has degraded PCIe width (x8 instead of x16)."
echo "  Find which one."
echo ""
echo "  Step 1 - List Mellanox devices:"
echo "    $FAKE_LSPCI"
echo ""
echo "  Step 2 - Check each HCA's PCIe link:"
echo "    $FAKE_LSPCI -vv -s <address> | grep -i lnk"
echo ""
echo "  Compare LnkCap (max) vs LnkSta (current)"
echo "  Expected width: x16"
echo ""
echo "  When done, click 'Mark Complete' in the web UI."
echo "═══════════════════════════════════════════════════════"
echo ""
