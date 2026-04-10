#!/bin/bash
# IB Degraded Speed Lab - inject a port running at reduced rate

MARKER="/tmp/.training_lab_ib_degraded"
FAKE_IBSTAT="/tmp/fake_ibstat_degraded.sh"

# pick a random HCA to be "degraded"
HCAS=("mlx5_0" "mlx5_1" "mlx5_2" "mlx5_3")
DEGRADED_HCA="${HCAS[$((RANDOM % 4))]}"

echo "degraded_hca=$DEGRADED_HCA" > "$MARKER"

# create a wrapper script that shows degraded speed
cat > "$FAKE_IBSTAT" << 'WRAPPER'
#!/bin/bash
# wrapper that injects a degraded speed port

DEGRADED_HCA=$(grep "degraded_hca" /tmp/.training_lab_ib_degraded 2>/dev/null | cut -d= -f2)

# generate output for all HCAs
for hca in mlx5_0 mlx5_1 mlx5_2 mlx5_3; do
    if [ "$hca" = "$DEGRADED_HCA" ]; then
        RATE="200"  # HDR instead of NDR
    else
        RATE="400"  # NDR (expected)
    fi
    cat << EOF
CA '$hca'
        CA type: MT4129
        Number of ports: 1
        Firmware version: 28.39.1002
        Hardware version: 0
        Node GUID: 0xb8cef603006b5a5e
        System image GUID: 0xb8cef603006b5a62
        Port 1:
                State: Active
                Physical state: LinkUp
                Rate: $RATE
                Base lid: 65535
                LMC: 0
                SM lid: 65534
                Capability mask: 0x2651e84a
                Port GUID: 0xb8cef603006b5a5f
                Link layer: InfiniBand
EOF
done
WRAPPER

chmod +x "$FAKE_IBSTAT"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  IB DEGRADED SPEED LAB"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  This is an NDR (400 Gb/s) cluster, but one HCA is"
echo "  running at reduced speed."
echo ""
echo "  Run: $FAKE_IBSTAT"
echo "  (wrapper simulating ibstat output)"
echo ""
echo "  Expected rate: 400 (NDR)"
echo "  Look for a port with lower rate (HDR = 200)"
echo ""
echo "  When done, click 'Mark Complete' in the web UI."
echo "═══════════════════════════════════════════════════════"
echo ""
