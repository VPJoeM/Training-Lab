#!/bin/bash
# IB Port Down Lab - inject a fake down port into ibstat output

MARKER="/tmp/.training_lab_ib_down"
FAKE_IBSTAT="/tmp/fake_ibstat_wrapper.sh"

# pick a random HCA to be "down"
HCAS=("mlx5_0" "mlx5_1" "mlx5_2" "mlx5_3")
DOWN_HCA="${HCAS[$((RANDOM % 4))]}"
DOWN_PORT="1"

echo "down_hca=$DOWN_HCA" > "$MARKER"
echo "down_port=$DOWN_PORT" >> "$MARKER"

# create a wrapper script that modifies ibstat output
cat > "$FAKE_IBSTAT" << 'WRAPPER'
#!/bin/bash
# wrapper that injects a down port into ibstat output

DOWN_HCA=$(grep "down_hca" /tmp/.training_lab_ib_down 2>/dev/null | cut -d= -f2)

if [ "$1" = "-l" ]; then
    /usr/sbin/ibstat -l 2>/dev/null || echo -e "mlx5_0\nmlx5_1\nmlx5_2\nmlx5_3"
elif [ -n "$1" ] && [ "$1" = "$DOWN_HCA" ]; then
    # show this specific HCA as down
    cat << EOF
CA '$DOWN_HCA'
        CA type: MT4129
        Number of ports: 1
        Firmware version: 28.39.1002
        Hardware version: 0
        Node GUID: 0xb8cef603006b5a5e
        System image GUID: 0xb8cef603006b5a62
        Port 1:
                State: Down
                Physical state: Polling
                Rate: 40
                Base lid: 0
                LMC: 0
                SM lid: 0
                Capability mask: 0x00010000
                Port GUID: 0xb8cef603006b5a5f
                Link layer: InfiniBand
EOF
else
    # run real ibstat but inject our fake down port
    REAL_OUTPUT=$(/usr/sbin/ibstat 2>/dev/null)
    if [ -z "$REAL_OUTPUT" ]; then
        # no real IB hardware - generate fake output
        for hca in mlx5_0 mlx5_1 mlx5_2 mlx5_3; do
            if [ "$hca" = "$DOWN_HCA" ]; then
                STATE="Down"
                PHYS="Polling"
                RATE="40"
            else
                STATE="Active"
                PHYS="LinkUp"
                RATE="400"
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
                State: $STATE
                Physical state: $PHYS
                Rate: $RATE
                Base lid: 65535
                LMC: 0
                SM lid: 65534
                Capability mask: 0x2651e84a
                Port GUID: 0xb8cef603006b5a5f
                Link layer: InfiniBand
EOF
        done
    else
        # real hardware - modify the down HCA in output
        echo "$REAL_OUTPUT" | awk -v down="$DOWN_HCA" '
            /^CA / { current_ca = $2; gsub(/'\''/, "", current_ca) }
            /State:/ && current_ca == down { gsub(/Active/, "Down"); gsub(/LinkUp/, "Polling") }
            /Physical state:/ && current_ca == down { gsub(/LinkUp/, "Polling") }
            /Rate:/ && current_ca == down { gsub(/[0-9]+/, "40") }
            { print }
        '
    fi
fi
WRAPPER

chmod +x "$FAKE_IBSTAT"

# create alias for current session
alias ibstat="$FAKE_IBSTAT"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  IB PORT DOWN LAB"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  One of the InfiniBand ports is DOWN."
echo "  Find which HCA and port is affected."
echo ""
echo "  Run: sudo ibstat"
echo "  (or use: $FAKE_IBSTAT if alias doesn't work)"
echo ""
echo "  Look for:"
echo "    State: Down"
echo "    Physical state: Polling"
echo ""
echo "  When done, click 'Mark Complete' in the web UI."
echo "═══════════════════════════════════════════════════════"
echo ""

# export the wrapper path so verify can find it
export FAKE_IBSTAT
