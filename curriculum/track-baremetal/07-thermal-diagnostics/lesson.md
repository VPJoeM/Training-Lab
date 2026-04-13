# Thermal Diagnostics

Dell requires thermal validation on GPU servers to ensure cooling is adequate. This is a critical part of deployment qualification and ongoing maintenance.

## The Thermal Workflow

The Dell thermal validation process:

1. **Run GPU stress test** under controlled conditions
2. **Monitor temperatures** across all GPUs, CPUs, ambient sensors
3. **Collect metrics** (gpu_metrics.csv, DCGM data)
4. **Collect a TSR** from iDRAC for Dell's records
5. **Package results** and compare against Dell's thresholds

If any GPU exceeds Dell's temperature thresholds during the stress test, the server fails thermal validation and needs attention (rack position, airflow, fan profile, etc.).

## When to Use What

**DCGM diagnostics (via node toolkit)** -- your go-to for quick GPU stress testing. Run a Level 3 or Level 4 to verify GPUs are healthy. Use this for troubleshooting, post-RMA validation, or just checking if hardware is solid.

```bash
./scripts/sshv/start-node-toolkit.sh
# → Main Menu option 14 (Log Collection) → option 11 (Run DCGMI Diagnostics)
```

**Thermal diagnostics script** -- the full Dell thermal validation workflow. Use this when Dell specifically requires thermal validation (new deployments, rack moves, cooling changes). It wraps DCGM but adds temperature monitoring, TSR collection, and result packaging that Dell expects.

```bash
./scripts/gpu/thermal-diagnostics-2.6.2-vp.sh
```

What the thermal script does on top of DCGM:

- Runs DCGM stress test via dcgmproftester
- Polls temperatures at regular intervals throughout the test
- Triggers TSR collection from iDRAC via racadm
- Packages everything into a results bundle for Dell

**Artifacts produced**:

- `thermal_results.*.csv` -- time-series GPU temperature, power, utilization
- `dcgmproftester.log` -- DCGM stress test output
- `TSR_*.zip` -- Dell Tech Support Report
- Summary report with pass/fail per GPU

## Reading the Results

The `thermal_results.*.csv` file is your primary output. Key columns:

| Column | What to Check |
|--------|--------------|
| gpu_temp | Must stay below Dell's threshold (usually 83°C for H100) |
| mem_temp | HBM temperature -- usually tracks GPU temp closely |
| power_draw | Should be near TDP (700W for H100 SXM) |
| gpu_util | Should be 100% during stress test |

If a GPU shows lower power draw and lower temp than its siblings, it might not be getting proper PCIe power or has a hardware issue.

## What's Next

Labs: run thermal diagnostics on a single node, interpret the results and identify any issues.
