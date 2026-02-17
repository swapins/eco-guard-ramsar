# Hardware Configurations

Complete setup guides and configuration files for deploying Eco-Guard-Ramsar across different embedded platforms.

---

## Quick Start: Platform Selection

Choose the appropriate deployment based on your requirements:

### **For Biological Indicator Detection (Unit B)** → **Jetson Nano**
⚡ **Best for:** AI-based image analysis, real-time computer vision  
📋 [Jetson Nano Deployment Guide](jetson_nano_deployment.md)

| Metric | Jetson Nano | Raspberry Pi 4 |
|--------|-------------|---|
| Inference Speed | 120–150 ms | 180–250 ms |
| Power (Idle) | 5W | 2.5W |
| GPU Acceleration | ✅ Yes (120+ CUDA cores) | ❌ No |
| TFLite Optimization | ✅ Excellent | ✅ Good |
| Cost | $99 | $55 |

### **For Physico-Chemical Sensors (Unit A)** → **Raspberry Pi 4B**
🌊 **Best for:** Sensor data collection, MQTT publishing, simple logic  
📋 [Raspberry Pi Deployment Guide](raspberry_pi_deployment.md)

| Metric | Raspberry Pi 4B | Jetson Nano |
|--------|---|---|
| Power Consumption | 1.5–3.5W | 5–10W |
| GPIO Flexibility | ✅ 27 GPIO pins | Limited |
| I2C/SPI Support | ✅ Native | ✅ Via adapter |
| Cost | $55 | $99 |
| Solar Viability | ✅ Excellent | ✅ Good |

---

## Configuration Files Structure

```
hardware_configs/
├── README.md                              # This file
├── jetson_nano_deployment.md              # Full Jetson Nano setup (GPU, TFLite, power)
├── raspberry_pi_deployment.md             # Full Raspberry Pi setup (I2C, GPIO, power)
├── sensor_calibration.yaml                # Unified sensor calibration values
├── mqtt_config.env                        # MQTT broker credentials (template)
├── tflite_model_config.yaml               # TensorFlow Lite inference settings
├── power_management.yaml                  # Solar charging and power budgets
└── deployment_checklist.txt               # Pre-deployment verification steps
```

---

## Key Configuration Files Explained

### 1. **Sensor Calibration** (`sensor_calibration.yaml`)
Stores physical calibration values for all analog sensors:
- **pH Probe:** Calibration points (pH 4, 7, 10) with measured voltages
- **Turbidity Sensor:** NTU conversion curve with temperature compensation
- **Nitrogen Sensor:** ISE sensor calibration and temperature effect
- **Temperature:** DS18B20 offset and accuracy specifications

**Usage:**
```python
import yaml
with open('hardware_configs/sensor_calibration.yaml') as f:
    config = yaml.safe_load(f)
    ph_calibration = config['sensors']['ph_probe']['linear_fit']
```

### 2. **MQTT Configuration** (`mqtt_config.env`)
Broker credentials and topic mappings:
```env
MQTT_BROKER=mqtt.example.com
MQTT_TOPIC_SENSOR=ramsar/sasthamcotta/unit_a/telemetry
MQTT_TOPIC_BIOLOGICAL=ramsar/sasthamcotta/unit_b/detections
```

**Load in code:**
```python
from dotenv import load_dotenv
load_dotenv('hardware_configs/mqtt_config.env')
broker = os.getenv('MQTT_BROKER')
```

### 3. **TFLite Model Config** (`tflite_model_config.yaml`)
Inference parameters for biological detection:
- Model path and version
- Input preprocessing (image normalization)
- Output class names
- GPU delegate settings
- Confidence thresholds (0.70–0.85 typical)

### 4. **Power Management** (`power_management.yaml`)
Solar and battery configuration:
- **Max Performance:** 98 W (peak inference, bright sun)
- **Balanced:** 6 W (transition hours)
- **Low Power:** 3 W (night, battery-only)
- Battery capacity: 5000 mAh (25 Wh typical)
- Solar panel: 50W rated (250 Wh/day expected)

---

## Deployment Comparison Matrix

| Feature | Jetson Nano | Raspberry Pi 4B | Notes |
|---------|------------|---|---|
| **Cost** | $99 | $55–75 | Jetson needs GPU cooling |
| **CPU** | ARM Cortex-A57 (4 cores @ 1.43 GHz) | ARMv8 (4 cores @ 1.5 GHz) | Similar CPU performance |
| **GPU** | 128-core Maxwell | None | **Jetson advantage for AI** |
| **RAM** | 4 GB LPDDR4 | 4 GB LPDDR4 | Same |
| **Power (Idle)** | 5W | 2.5W | **Pi advantage for solar** |
| **Power (Inference)** | 8–10W | 4–6W | Jetson faster but draws more |
| **Inference Time** | 120–150 ms | 180–250 ms | Jetson 50% faster |
| **GPIO Pins** | 14 (limited) | 27 (flexible) | **Pi better for sensors** |
| **I2C Support** | Via Adafruit HAT | Native I2C bus 1,3 | **Pi native advantage** |
| **CUDA/AI Support** | ✅ Yes | ❌ No | **Jetson only** |
| **Heat Generation** | Moderate (needs heatsink) | Low | Jetson hotter, needs cooling |
| **Deployment Suitable For** | Unit B (AI detection) | Unit A (sensors + MQTT) | Specialized uses |

---

## Hardware Shopping List

### **Unit A (Raspberry Pi 4B) - Physico-Chemical Monitoring**
```
Component                          Cost    Supplier
─────────────────────────────────────────────────────
Raspberry Pi 4B (4GB)              $55     raspberrypi.com
microSD Card (128GB, U3)           $12     MicroCenter
USB-C 5V/3A PSU                    $8      Amazon
Case with heatsink                 $15     Various
─────────────────────────────────────────────────────
Sensor Bundle:
  - ADS1115 ADC (I2C)              $12     Adafruit
  - pH Probe + Electronics          $30     SensorMate
  - Turbidity Sensor                $25     Atlas Scientific
  - Nitrogen ISE + Box              $35     YSI
  - DS18B20 Temperature             $5      Amazon
  - Cables (I2C, 1-Wire)            $10     Amazon
─────────────────────────────────────────────────────
Power Supply:
  - 50W Solar Panel                 $40     Amazon
  - MPPT Charger (15A)              $30     Victron
  - 5000 mAh LiFePO4 Battery        $25     Amazon
─────────────────────────────────────────────────────
TOTAL: ~$300
```

### **Unit B (Jetson Nano) - Biological Detection**
```
Component                          Cost    Supplier
─────────────────────────────────────────────────────
Jetson Nano Developer Kit          $99     NVIDIA
microSD Card (256GB, U3)           $20     Amazon
USB-C 5V/4A PSU                    $12     Amazon
Heatsink + Fan                     $15     Amazon
─────────────────────────────────────────────────────
Camera & Vision:
  - Raspberry Pi v2 Camera (8 MP)  $12     Adafruit
  - 200mm CSI Ribbon Cable         $5      Adafruit
  - Wide-angle lens (optional)     $20     Amazon
─────────────────────────────────────────────────────
Communication:
  - USB WiFi Adapter               $8      Amazon
  - Ethernet Cable (optional)      $3      Amazon
─────────────────────────────────────────────────────
Power Supply:
  - 50W Solar Panel                $40     Amazon
  - MPPT Charger                   $30     Victron
  - 5000 mAh LiFePO4               $25     Amazon
─────────────────────────────────────────────────────
TOTAL: ~$290
```

---

## Network Topology

```
┌─────────────────────────────────────────────────┐
│         MQTT Broker (Cloud or Local)            │
│      (e.g., Mosquitto, HiveMQ, AWS IoT)       │
└──────────────┬──────────────────────────────────┘
               │
      ┌────────┴─────────┐
      │                  │
   ┌──▼────────────────┐ │ ┌────────────────────┐
   │   Unit A (Pi 4B)  │ │ │ Unit B (Jetson)    │
   │                  │ │ │                    │
   │ • pH Sensor      │ │ │ • Camera (v2)      │
   │ • Turbidity      │ │ │ • TFLite Model     │
   │ • Nitrogen       │ │ │ • AI Detection     │
   │ • Publishes ...  │ │ │ • Publishes ...    │
   │   telemetry/TPC  │ │ │   detections/TPC   │
   └─────────────────┘ │ │ └────────────────────┘
                       │ │
                       └─┘ (WiFi/Ethernet)
                           (30m range typical)

Both units:
- Subscribe to ramsar/sasthamcotta/system/commands
- Periodic publish to respective topic
- Local data buffering on 24h network outage
- Resume publish when reconnected
```

---

## Installation Checklists

### **Pre-Deployment (Hardware)**
- [ ] Solder GPIO headers to Jetson Nano (if not pre-soldered)
- [ ] Install heatsink on Jetson Nano CPU
- [ ] Attach CSI ribbon cable to camera (aligned properly)
- [ ] Connect ADS1115 ADC via I2C (SDA/SCL)
- [ ] Connect 1-Wire temperature sensor to GPIO pin
- [ ] Test 12V→5V power regulation circuit
- [ ] Verify solar panel output (18V at open-circuit)
- [ ] Connect MPPT charger input/output correctly (respect polarity!)
- [ ] Mount waterproofing enclosure
- [ ] Cable strain relief (prevent wire damage)

### **Pre-Deployment (Software)**
- [ ] Download and flash JetPack / Raspberry Pi OS
- [ ] Configure WiFi SSID and password
- [ ] Enable I2C and 1-Wire interfaces
- [ ] Verify I2C device detection: `i2cdetect -y 1`
- [ ] Verify camera capture: `gst-launch` or `raspistill`
- [ ] Copy calibration files to `/hardware_configs/`
- [ ] Set MQTT credentials in `.env` file
- [ ] Test MQTT connection: `mosquitto_pub/sub`
- [ ] Load and test TFLite model (if Unit B)
- [ ] Verify sensor readings (unit test script)

### **Pre-Deployment (Deployment Site)**
- [ ] Mount solar panel facing south (Northern hemisphere) with tilt angle = latitude
- [ ] Orient unit away from direct wind to minimize vibration
- [ ] Immerse sensors in water at correct depth
- [ ] Tether floating unit to prevent drift
- [ ] Weatherproof all power connections
- [ ] Verify GPS location (optional, for metadata)
- [ ] Test WiFi/LTE signal strength at site
- [ ] Plan 24-month maintenance schedule

---

## Troubleshooting Reference

| Issue | Jetson | Raspberry Pi |
|-------|--------|---|
| "No module 'tensorflow'" | Reinstall with NVIDIA index | Use `pip install tensorflow-lite` |
| I2C device not found | Check if CSI devices on I2C bus 0 | Use `i2cdetect -y 1` on bus 1 |
| Camera no video | Reseat CSI ribbon cable | Check CSI port (red vs blue tags) |
| Low inference FPS | Reduce model size or use quantized | Enable GPU delegate (Jetson only) |
| Power consumption high | Disable GPU when idle | Use `powersave` governor |
| MQTT disconnecting | Check WiFi signal (-60 dBm+) | Increase publish interval |
| Sensor reading erratic | Verify ADC calibration values | Check I2C clock speed (100 kHz) |

---

## References

- [NVIDIA Jetson Nano Docs](https://docs.nvidia.com/jetson/nano/)
- [Raspberry Pi 4B Docs](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)
- [Adafruit Sensor Libraries](https://github.com/adafruit)
- [TensorFlow Lite Performance Optimization](https://www.tensorflow.org/lite/performance)
- [MQTT Protocol Specification](https://mqtt.org/)

---

## Support

For hardware-specific questions:
1. Check the platform-specific README (`jetson_nano_deployment.md` or `raspberry_pi_deployment.md`)
2. Review sensor datasheets in `models/` directory
3. Test with provided calibration values before field deployment
4. Document any sensor modifications in a local git branch

---

**Last Updated:** February 17, 2026  
**Validated Platforms:** Jetson Nano (JetPack 4.6.3), Raspberry Pi 4B (Debian Bullseye)
