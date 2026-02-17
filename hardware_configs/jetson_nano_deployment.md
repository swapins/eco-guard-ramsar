# Jetson Nano Deployment Configuration

Complete setup guide for deploying Eco-Guard-Ramsar on NVIDIA Jetson Nano (for Unit B: AI-based biological detection).

---

## Hardware Specifications

### Jetson Nano Module
| Component | Specification |
|-----------|---------------|
| **Processor** | NVIDIA Tegra X1 (quad-core ARM A57 @ 1.43 GHz) |
| **GPU** | 128-core Maxwell |
| **RAM** | 4 GB LPDDR4 (shared with GPU) |
| **Storage** | microSD card (256 GB recommended) |
| **Power** | 5V/4A USB-C or barrel connector |
| **OS** | JetPack 4.6.3 (CUDA 10.2) |
| **TensorFlow Lite** | Optimized for ARM64 architecture |

### Additional Hardware
- **Camera Module:** Raspberry Pi v2 Camera (8 MP, CSI-2 interface)
- **Sensor Bridge:** Adafruit ADS1115 (I2C ADC for analog sensors)
- **Power Supply:** USB-C PD 5V/4A minimum
- **Communication:** Ethernet or USB WiFi adapter
- **Storage:** microSD U3 card (A2 speed rated)

---

## Jetson Nano vs Raspberry Pi

| Feature | Jetson Nano | Raspberry Pi 4 |
|---------|-------------|----------------|
| **TensorFlow Lite Inference** | **Optimized (GPU-accelerated)** | CPU-based |
| **Inference Speed** | 120–150 ms | 180–250 ms |
| **Power Consumption** | 5W (idle) → 10W (inference) | 3W (idle) → 8W (full load) |
| **Video Encoding** | Hardware H.264/H.265 | Software encoding (slow) |
| **AI/ML Frameworks** | TensorFlow Lite, PyTorch | TensorFlow Lite (limited) |
| **Cost** | ~$99 | ~$55–75 |
| **Solar Viability** | Good (higher power, faster inference) | Better (lower power, slower) |

**Why Jetson Nano for Unit B:**
- GPU acceleration reduces inference latency 120–180 ms (vs 200+ ms on Pi)
- Supports larger biological detection models
- Better for video encoding if cloud upload required
- NVIDIA CUDA ecosystem for model optimization

---

## Installation Steps

### Step 1: Flash JetPack to microSD Card

**Option A: Using NVIDIA SDK Manager (Recommended)**
1. Download [NVIDIA SDK Manager](https://developer.nvidia.com/nvidia-sdk-manager)
2. Insert microSD card (256 GB UHS Class 3 minimum)
3. Run SDK Manager:
   ```bash
   sdkmanager  # On Linux/WSL
   ```
4. Select: `Jetson Nano` → `JetPack 4.6.3`
5. Flash to microSD (takes ~30 minutes)
6. Insert into Jetson Nano and power on

**Option B: Command Line (Linux)**
```bash
# Download JetPack image
wget https://developer.nvidia.com/jetpack-sd-card-image

# Flash with dd (replace sdX with your microSD device)
sudo dd if=jetpack.img of=/dev/sdX bs=4M status=progress
sudo sync
```

### Step 2: Initial Boot and Setup
```bash
# Boot Jetson Nano with microSD
# Connect HDMI, mouse, keyboard
# Select language and timezone
# Create user account (suggest: `botadmin`)
# Set password

# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y \
  python3-pip \
  python3-dev \
  libhdf5-dev \
  libharfbuzz0b \
  libwebp6 \
  libtiff5 \
  libjasper1 \
  libjasper-dev
```

### Step 3: Install Dependencies

```bash
# Create virtual environment
python3 -m venv /home/botadmin/eco-guard-venv
source /home/botadmin/eco-guard-venv/bin/activate

# Install NumPy (pre-built for ARM64)
pip install --upgrade pip
pip install numpy==1.19.5

# Install TensorFlow Lite for Jetson
pip install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v461 tensorflow==2.5.0

# Install project dependencies
cd /home/botadmin/eco-guard-ramsar
pip install -r requirements.txt

# Verify TensorFlow Lite installation
python3 -c "import tensorflow as tf; print(tf.__version__); print(tf.sysconfig.get_build_info()['cuda_version'])"
```

### Step 4: Configure Camera Interface

```bash
# Enable CSI camera in device tree
sudo nano /boot/extlinux/extlinux.conf

# Add to APPEND line:
# nvargus_v4l2

# Reboot
sudo reboot

# Verify camera
python3 -c \
  "import cv2; cap = cv2.VideoCapture(0); ret, frame = cap.read(); print(f'Camera OK: {ret}')"
```

---

## Configuration Files

### 1. `jetson_gpio_pinmap.json`
GPIO and I2C pin mappings for sensors and communication.

```json
{
  "camera": {
    "interface": "csi",
    "port": 0,
    "resolution": [1920, 1080],
    "fps": 15,
    "format": "MJPEG"
  },
  "i2c": {
    "adc_bridge": {
      "bus": 1,
      "address": "0x48",
      "channels": {
        "ph_sensor": 0,
        "turbidity_sensor": 1,
        "nitrogen_sensor": 2,
        "temperature_sensor": 3
      }
    }
  },
  "uart": {
    "serial_port": "/dev/ttyUSB0",
    "baud_rate": 9600
  },
  "gpio": {
    "status_led_red": 216,
    "status_led_green": 217,
    "power_control": 332,
    "error_buzzer": 333
  }
}
```

### 2. `sensor_calibration.yaml`
Calibration values for analog sensors (Unit A data passed to Jetson via MQTT).

```yaml
unit_id: Unit_B
hardware_platform: Jetson Nano
timestamp_calibrated: 2026-02-17

sensors:
  temperature:
    model: "DS18B20"
    pin: GPIO_216
    calibration:
      offset: 0.0
      scale: 1.0
    range: [20.0, 35.0]

  adc_bridge:
    model: "Adafruit ADS1115"
    i2c_address: "0x48"
    gain: 2
    channels:
      - id: 0
        name: "pH Probe"
        voltage_range: [0, 5]
        sensor_range: [0, 14]
        calibration: {offset: 0.0, scale: 1.0}
      - id: 1
        name: "Turbidity (NTU)"
        voltage_range: [0, 5]
        sensor_range: [0, 50]
        calibration: {offset: 0.5, scale: 0.99}
      - id: 2
        name: "Nitrogen (mg/L)"
        voltage_range: [0, 5]
        sensor_range: [0, 10]
        calibration: {offset: 0.0, scale: 1.0}
      - id: 3
        name: "Temperature (°C)"
        voltage_range: [0, 5]
        sensor_range: [0, 40]
        calibration: {offset: -0.2, scale: 1.05}
```

### 3. `mqtt_config.env`
MQTT broker credentials and topic configuration.

```env
# MQTT Broker
MQTT_BROKER=broker.example.com
MQTT_PORT=1883
MQTT_USERNAME=ramsar_user
MQTT_PASSWORD=secure_password_here

# Topic Configuration
MQTT_TOPIC_PREFIX=ramsar/sasthamcotta
MQTT_TOPIC_SENSOR_DATA=ramsar/sasthamcotta/unit_a/telemetry
MQTT_TOPIC_BIOLOGICAL=ramsar/sasthamcotta/unit_b/detections
MQTT_TOPIC_STATUS=ramsar/sasthamcotta/system/status
MQTT_TOPIC_COMMANDS=ramsar/sasthamcotta/system/commands

# Message Format
MQTT_QOS=1
MQTT_RETAIN=false

# TLS/SSL (optional)
MQTT_TLS_ENABLED=false
MQTT_TLS_CAFILE=/etc/ssl/certs/ca-certificates.crt
MQTT_TLS_CERTFILE=/path/to/client-cert.pem
MQTT_TLS_KEYFILE=/path/to/client-key.pem
```

### 4. `tflite_model_config.yaml`
TensorFlow Lite model configuration for biological detection.

```yaml
model_name: "Bio-Indicator-Classifier-v1.0"
model_path: "/home/botadmin/eco-guard-ramsar/models/bio_classifier.tflite"
model_version: "1.0.0"

input:
  shape: [1, 224, 224, 3]
  type: float32
  preprocessing:
    mean: [127.5, 127.5, 127.5]
    std: [127.5, 127.5, 127.5]
    format: "RGB"

output:
  layer: 0
  type: float32
  num_classes: 3
  class_names: ["E. coli", "Chaoborus spp.", "Healthy Algae"]

inference:
  cpu_threads: 1
  use_nnapi: false
  use_gpu_delegate: true
  timeout_ms: 500

threshold:
  confidence_min: 0.70
  confidence_log: 0.85  # Log readings below this
  confidence_alert: 0.60  # Generate alert if below this

performance:
  latency_target_ms: 150
  batch_size: 1
  skip_frames: 4  # Process every 5th frame to reduce power
```

### 5. `power_management.yaml`
Power optimization settings for solar deployment.

```yaml
unit_id: Unit_B
platform: Jetson Nano

power_profiles:
  max_performance:
    cpu_governor: "performance"
    cpu_freq_max: 1428  # MHz
    gpu_freq_max: 921   # MHz
    idle_power: 10      # Watts
    use_case: "During peak sun (11am-3pm)"

  balanced:
    cpu_governor: "schedutil"
    cpu_freq_max: 1000
    gpu_freq_max: 700
    idle_power: 6
    use_case: "Morning/evening transition"

  low_power:
    cpu_governor: "powersave"
    cpu_freq_max: 500
    gpu_freq_max: 300
    idle_power: 3
    use_case: "Night/cloudy conditions (battery-only)"

battery:
  min_voltage: 4.5  # Volts (shutdown if below)
  max_voltage: 5.5
  capacity: 5000    # mAh
  charge_time_hours: 6

solar_panel:
  power_rating: 50  # Watts
  voc: 21           # Volts (open circuit)
  isc: 3.0          # Amperes (short circuit)
  mppt_enabled: true
  mppt_controller: "Victron BlueSolar MPPT 75/15"

charging:
  target_soc: 0.95  # Stop charging at 95% SOC
  charger_efficiency: 0.92
  lipo_cell_count: 6  # 6S battery (22.2V nominal)

scheduling:
  wake_time: "06:00"  # Sunrise
  sleep_time: "18:30" # Sunset
  inference_intervals_minutes:
    max: 15      # During peak sun
    balanced: 30 # Transition
    low_power: 60  # Battery only
```

---

## Optimization for Jetson Nano

### Enable GPU Acceleration for TensorFlow Lite
```bash
# Use GPU delegate for inference
python3 -c "
import tensorflow as tf

# Load model with GPU delegate
interpreter = tf.lite.Interpreter(
    model_path='models/bio_classifier.tflite',
    experimental_delegates=[tf.lite.experimental.load_delegate('libtensorflowlite_gpu_delegate.so')]
)
interpreter.allocate_tensors()
print('GPU delegate enabled')
"
```

### Disable Unused Services to Save Power
```bash
# Disable HDMI (saves ~1W)
sudo sh -c 'echo 0 > /sys/devices/virtual/graphics/fbcon/cursor_blink'

# Disable bluetooth
sudo systemctl disable bluetooth
sudo systemctl stop bluetooth

# Reduce governor frequency scaling overhead
echo "schedutil" | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

### Monitor Power Consumption
```bash
# Install tegrastats (pre-installed on JetPack)
tegrastats --interval 1000

# Sample output:
# RAM 2046/3964MB (lfb 512MB) CPU [8%@1020,11%@1020,0%@1020,0%@1020] EMC_FREQ 0% GR3D_FREQ 25% PLL@35C MCPU@35C PMIC@100C Temp@35C
```

---

## Deployment Checklist

- [ ] JetPack 4.6.3 flashed to microSD
- [ ] Python 3.7+ installed
- [ ] TensorFlow Lite GPU delegate working
- [ ] Camera interface enabled and tested
- [ ] I2C sensors accessible (check `i2cdetect -y 1`)
- [ ] MQTT broker reachable (`ping broker.example.com`)
- [ ] `.env` file configured with credentials
- [ ] TFLite model file present in `models/` directory
- [ ] Main script tested (`python3 main.py --test`)
- [ ] Systemd service configured for auto-start (see below)

### Auto-Start Configuration

Create `/etc/systemd/system/eco-guard-unit-b.service`:
```ini
[Unit]
Description=Eco-Guard Ramsar Unit B (Jetson Nano)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=botadmin
WorkingDirectory=/home/botadmin/eco-guard-ramsar
Environment="PATH=/home/botadmin/eco-guard-venv/bin"
ExecStart=/home/botadmin/eco-guard-venv/bin/python3 main.py
Restart=on-failure
RestartSec=30
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable eco-guard-unit-b.service
sudo systemctl start eco-guard-unit-b.service

# View logs
journalctl -u eco-guard-unit-b.service -f
```

---

## Troubleshooting

### "No module named 'tensorflow'"
```bash
# Reinstall with correct NVIDIA index
source ~/eco-guard-venv/bin/activate
pip install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v461 tensorflow==2.5.0
```

### Camera not found
```bash
# Check CSI connection (reseat ribbon cable)
# Verify device tree:
cat /proc/device-tree/aliases | grep camera

# Test with gstreamer
gst-launch-1.0 nvarguscamerasrc ! fakesink
```

### GPU delegate fails to load
```bash
# Check GPU library path
find /usr -name "*tensorflow*gpu*"

# If library missing, reinstall:
pip install --force-reinstall tensorflow==2.5.0-ubuntu1
```

### Low memory errors during inference
```bash
# Reduce model size or use quantized variant
# Or disable multi-threading:
interpreter.set_num_threads(1)
```

---

## Performance Benchmarks

| Operation | Jetson Nano | Time (ms) | Power (W) |
|-----------|-------------|----------|-----------|
| Load TFLite model | Once at startup | 150 | - |
| Inference (224×224 RGB) | With GPU delegate | 120–150 | 8–10 |
| Camera capture (1080p) | H.264 encode | 30 | 3–5 |
| MQTT publish (10 readings) | WiFi | 500–1000 | 2 |
| Idle (no activity) | System | - | 5–7 |

**Estimated Daily Power Consumption:**
- 12 hours sunlight: ~80 Wh (inference + sensors)
- 12 hours night: ~35 Wh (minimal operations)
- **Total:** ~115 Wh/day
- **50W solar panel:** Sufficient capacity for 98% uptime

---

## References

- [NVIDIA Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)
- [JetPack Documentation](https://docs.nvidia.com/jetson/jetpack/)
- [TensorFlow Lite Optimization](https://www.tensorflow.org/lite/performance/best_practices)
- [GPU Delegate for TFLite](https://www.tensorflow.org/lite/performance/gpu)

---

**Last Updated:** February 17, 2026  
**Configuration Version:** 1.0  
**Target Platform:** NVIDIA Jetson Nano (JetPack 4.6.3)
