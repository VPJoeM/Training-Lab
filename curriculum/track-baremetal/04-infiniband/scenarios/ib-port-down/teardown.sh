#!/bin/bash
# clean up the IB port down lab

rm -f /tmp/.training_lab_ib_down
rm -f /tmp/fake_ibstat_wrapper.sh
unalias ibstat 2>/dev/null || true

echo "IB port down lab cleaned up"
