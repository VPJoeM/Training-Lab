#!/bin/bash
MARKER="/tmp/.training_lab_fm_status"
FAKE_SYSTEMCTL="/tmp/fake_systemctl_fm.sh"

# randomly make FM running or failed
if [ $((RANDOM % 2)) -eq 0 ]; then
    FM_STATUS="running"
else
    FM_STATUS="failed"
fi

echo "fm_status=$FM_STATUS" > "$MARKER"

cat > "$FAKE_SYSTEMCTL" << 'WRAPPER'
#!/bin/bash
FM_STATUS=$(grep "fm_status" /tmp/.training_lab_fm_status 2>/dev/null | cut -d= -f2)

if [[ "$*" == *"nvidia-fabricmanager"* ]]; then
    if [ "$FM_STATUS" = "running" ]; then
        cat << 'EOF'
● nvidia-fabricmanager.service - NVIDIA Fabric Manager Service
     Loaded: loaded (/lib/systemd/system/nvidia-fabricmanager.service; enabled)
     Active: active (running) since Mon 2024-01-15 10:30:00 UTC; 2 days ago
   Main PID: 1234 (nv-fabricmanage)
      Tasks: 6 (limit: 1234567)
     Memory: 45.2M
        CPU: 1min 23s
     CGroup: /system.slice/nvidia-fabricmanager.service
             └─1234 /usr/bin/nv-fabricmanager -c /etc/nvidia-fabricmanager/fabricmanager.cfg

Jan 15 10:30:00 gpu001 nv-fabricmanager[1234]: Fabric Manager started
Jan 15 10:30:01 gpu001 nv-fabricmanager[1234]: NVSwitch devices: 4
Jan 15 10:30:01 gpu001 nv-fabricmanager[1234]: GPU devices: 8
EOF
    else
        cat << 'EOF'
● nvidia-fabricmanager.service - NVIDIA Fabric Manager Service
     Loaded: loaded (/lib/systemd/system/nvidia-fabricmanager.service; enabled)
     Active: failed (Result: exit-code) since Mon 2024-01-15 10:30:00 UTC; 5min ago
    Process: 1234 ExecStart=/usr/bin/nv-fabricmanager -c /etc/nvidia-fabricmanager/fabricmanager.cfg (code=exited, status=1/FAILURE)
   Main PID: 1234 (code=exited, status=1/FAILURE)

Jan 15 10:30:00 gpu001 nv-fabricmanager[1234]: Version mismatch with driver
Jan 15 10:30:00 gpu001 nv-fabricmanager[1234]: Expected driver: 535.x, Found: 550.x
Jan 15 10:30:00 gpu001 systemd[1]: nvidia-fabricmanager.service: Failed with result 'exit-code'.
EOF
    fi
else
    /bin/systemctl "$@"
fi
WRAPPER

chmod +x "$FAKE_SYSTEMCTL"

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  FABRIC MANAGER STATUS LAB"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "  Check if Fabric Manager is running properly."
echo ""
echo "  Command:"
echo "    $FAKE_SYSTEMCTL status nvidia-fabricmanager"
echo ""
echo "  Look for 'active (running)' or 'failed'"
echo ""
echo "  When done, click 'Mark Complete' in the web UI."
echo "═══════════════════════════════════════════════════════"
echo ""
