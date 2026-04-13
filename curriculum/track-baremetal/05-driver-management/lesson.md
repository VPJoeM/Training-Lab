# Driver Management

The NVIDIA software stack has multiple components that all need to be compatible with each other. When they're not, things break in confusing ways.

## The Stack

From bottom to top:

1. **NVIDIA Kernel Driver** -- the base driver that talks to the GPU hardware
2. **CUDA Toolkit** -- libraries and tools for GPU compute
3. **Fabric Manager** -- manages NVLink/NVSwitch topology (critical for multi-GPU)
4. **NCCL** -- NVIDIA's collective communication library (used by training frameworks)
5. **cuDNN, TensorRT, etc.** -- higher-level libraries

## Version Compatibility

This is where most driver issues come from. The driver version, CUDA version, and Fabric Manager version all need to be compatible. NVIDIA publishes compatibility matrices, but the short version is: **all three major versions need to match.**

Check what's currently installed:

```bash
nvidia-smi                     # shows driver + CUDA version
cat /usr/local/cuda/version.txt  # CUDA toolkit version
systemctl status nvidia-fabricmanager  # Fabric Manager status
```

**Common failure mode**: Someone upgrades the driver but not Fabric Manager, or vice versa. nvidia-smi works fine for single-GPU ops but multi-GPU training fails because Fabric Manager can't talk to the new driver.

## install-drivers.sh

Our script handles the full driver installation workflow:

```bash
./scripts/gpu/install-drivers.sh
```

It manages:

- Driver package download and installation
- CUDA toolkit setup
- Fabric Manager installation and version matching
- Kernel module loading
- Post-install validation

## Manual Driver Installation

Know how to do it by hand so you understand what `install-drivers.sh` automates.

**Step 1 -- Remove old drivers (if needed):**

```bash
# check what's currently installed
dpkg -l | grep -i nvidia

# remove everything nvidia (nuclear option -- careful on production)
sudo apt-get purge -y 'nvidia-*' 'libnvidia-*'
sudo apt-get autoremove -y
```

**Step 2 -- Add the NVIDIA repo and install:**

```bash
# add the CUDA keyring if missing
if ! dpkg -l | grep -q cuda-keyring; then
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu$(lsb_release -rs | tr -d '.')/x86_64/cuda-keyring_1.1-1_all.deb
    sudo dpkg -i cuda-keyring_1.1-1_all.deb
    sudo apt-get update
fi

# install a specific driver version (example: 550)
sudo apt-get install -y nvidia-driver-550
sudo apt-get install -y cuda-toolkit-12-4
```

**Step 3 -- Install Fabric Manager (MUST match driver major version):**

```bash
# find the right version
apt-cache search nvidia-fabric

# install matching version
sudo apt-get install -y nvidia-fabricmanager-550
sudo systemctl enable nvidia-fabricmanager
sudo systemctl start nvidia-fabricmanager
```

**Step 4 -- Verify everything:**

```bash
nvidia-smi                              # driver loaded, GPUs visible
modinfo nvidia | grep ^version          # kernel module version
systemctl status nvidia-fabricmanager   # FM running
nvidia-smi topo -m                      # NVLink topology intact
```

After a driver install or upgrade, a reboot is usually required for the new kernel module to load. Don't skip this -- the old module stays resident in memory until you do.

```bash
# reboot to load the new kernel module (required after driver changes)
sudo reboot
# after reboot, verify everything loaded correctly
nvidia-smi
modinfo nvidia | grep ^version
```

**Step 5 -- Load on boot:**

```bash
# make sure the nvidia modules load at boot
sudo nvidia-persistenced --user root
sudo systemctl enable nvidia-persistenced
```

## Detecting Version Mismatch

Quick check for mismatches:

```bash
# driver version from nvidia-smi
nvidia-smi --query-gpu=driver_version --format=csv,noheader

# kernel module version
modinfo nvidia | grep ^version

# fabric manager version
nvidia-fabricmanager --version 2>/dev/null || dpkg -l | grep fabricmanager
```

If the driver and Fabric Manager major versions don't match, that's your problem.

## What's Next

Labs: identify a version mismatch from nvidia-smi output, walk through a driver reinstallation.
