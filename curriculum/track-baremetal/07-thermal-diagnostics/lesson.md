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

> **Where do the files end up?** By default, the thermal script writes everything to `/tmp/thermal_results/` on the target node. To pull them to your laptop, use scp, rsync, or the sshv wrapper:
> ```bash
> scp -r user@<node>:/tmp/thermal_results/ ./results/
> # or via rsync
> rsync -avz user@<node>:/tmp/thermal_results/ ./results/
> ```

## Manual Thermal Test

If you don't have the thermal diagnostics script handy, or you just want to understand what it's actually doing under the hood, you can run the full workflow manually. Same results, just more typing.

### 1. Start the GPU stress test

You need DCGM installed on the node first -- see [Module 03](../03-dcgm-basics/lesson.md) if you haven't set that up yet.

Pick one of these depending on what you have available:

```bash
# option A: dcgmproftester (comes with DCGM, hammers the GPUs hard)
dcgmproftester --no-dcgm-validation -t 1004 -d 600
# runs for 600 seconds (~10 min), test ID 1004 is the standard FP64 stress

# option B: dcgmi diag level 3 (built-in diagnostic suite)
dcgmi diag -r 3
# level 3 includes the stress test plus memory and PCIe checks
```

Run whichever one you pick in a tmux/screen session so it doesn't die if your SSH drops.

### 2. Poll temperatures during the test

In a separate terminal (or another tmux pane), loop nvidia-smi to capture temps while the stress test runs:

```bash
# poll every 5 seconds, log to csv
while true; do
  nvidia-smi --query-gpu=timestamp,index,gpu_name,temperature.gpu,temperature.memory,power.draw,utilization.gpu \
    --format=csv,noheader >> /tmp/thermal_poll.csv
  sleep 5
done
```

Let this run for the entire duration of the stress test. Kill it with Ctrl+C when the test finishes.

### 3. Collect a TSR from iDRAC

Once the stress test completes, grab a Tech Support Report while the system is still warm. See [Module 06](../06-tsr-collection/lesson.md) for the full breakdown on TSR collection, but the short version:

```bash
# via racadm (replace with your iDRAC IP)
racadm -r <idrac-ip> -u root -p <password> techsupreport collect
# wait for it to finish, then export
racadm -r <idrac-ip> -u root -p <password> techsupreport export -f /tmp/TSR_thermal.zip
```

### 4. Bundle the artifacts

Package everything into a single tar for easy handling:

```bash
mkdir -p /tmp/thermal_results
cp /tmp/thermal_poll.csv /tmp/thermal_results/
cp /tmp/TSR_thermal.zip /tmp/thermal_results/
# grab the dcgmproftester log if you used option A
cp /tmp/dcgmproftester.log /tmp/thermal_results/ 2>/dev/null

tar czf /tmp/thermal_bundle_$(hostname)_$(date +%Y%m%d).tar.gz -C /tmp thermal_results/
```

### 5. Download to your laptop

Pull the bundle off the node:

```bash
# scp
scp user@<node>:/tmp/thermal_bundle_*.tar.gz ./

# rsync (handy if the file is large or connection is flaky)
rsync -avz user@<node>:/tmp/thermal_bundle_*.tar.gz ./

# or if you're using the sshv wrapper from the toolkit
./scripts/sshv/pull-file.sh <node> /tmp/thermal_bundle_*.tar.gz ./results/
```

That's the whole thing. The thermal diagnostics script just automates these five steps, but knowing the manual path is useful when you're debugging or when the script isn't cooperating.

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
