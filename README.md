# Eco-Guard-Ramsar - Edge-AI Ecological Monitoring System

**Solar-powered Edge-AI for wetland monitoring at Ramsar sites. Integrates physico-chemical sensors with AI-based biological indicator detection.**

---

## About This Project

**Eco-Guard-Ramsar** is an end-to-end framework for the **PeachBot Eco** autonomous monitoring units, specifically designed for deployment in protected ecosystems. Validated at **Sasthamcotta Lake, India (Ramsar Site #1212)**, this system bridges the gap between manual water sampling and high-frequency digital environmental monitoring.

The framework combines **Hardware Systems Engineering** with **Environmental Data Science**—a critical capability for Singapore's ["Green Plan 2030"](https://www.greenplan.sg/) initiatives and global wetland conservation.

### Repository Topics
`edge-ai` `iot` `environmental-monitoring` `sustainability` `smart-water` `raspberry-pi` `tensorflow-lite` `ramsar-wetlands` `conservation-tech`

---

## Research Foundation

This project implements the technical framework for peer-reviewed research:  
> *"Dedicated Edge-AI Single-Board Computer Systems for Ecological Monitoring in Protected Wetlands: Evidence from a Ramsar Site in India."*

**Author:** Swapin Vidya  
**Affiliation:** PeachBot Technologies (Agastya Biologic Solutions)

---

## Core Innovation

The system uniquely combines three engineering disciplines:

### 1. Energy-Aware Computing
- Optimized for **98% operational uptime** on solar-limited power budgets
- Deterministic inference latency: **120–180 ms**
- Local data buffering during network outages
- Adaptive sampling based on battery state-of-charge

### 2. Multi-Modal Sensing
Unlike standard environmental loggers, Eco-Guard-Ramsar processes:
- **Chemical Telemetry:** pH, Turbidity, Nitrogen levels via analog sensor integration
- **Biological Telemetry:** Computer vision-based identification of indicator species (*Chaoborus* spp., *E. coli* presence)
- **Environmental Context:** Real-time power generation monitoring

### 3. Field Resilience
- Low-bandwidth **MQTT communication** for intermittent connectivity
- Graceful degradation when sensors fail
- Automatic data recovery and timestamp consistency
- Designed for rural wetland environments with minimal infrastructure

---

## System Architecture

### Dual-Unit Deployment
- **Unit A:** Real-time monitoring of pH, Turbidity, and Nitrogen levels
- **Unit B:** AI-assisted image analysis for biological indicators (E. coli, Chaoborus spp.)

### Deployment Specifications
| Specification | Details |
| :--- | :--- |
| **Operational Uptime** | 98% (Field Validated) |
| **Inference Latency** | 120–180 ms (TFLite) |
| **Deployment Site** | Sasthamcotta Lake, Ramsar Site #1212 |
| **Primary Stack** | Python / TFLite / MQTT / Solar-SBC |
| **Power Source** | Solar with battery backup |
| **Connectivity** | MQTT (low-bandwidth) with local fallback |

---

## Hardware Deployment Platforms

Eco-Guard-Ramsar supports dual-unit deployment with platform-specific optimizations:

### Unit A: Physico-Chemical Monitoring (Raspberry Pi 4B)
**For sensor data collection, MQTT publishing, and edge processing**
- **Processor:** ARM Cortex-A72 (1.5 GHz quad-core)
- **Power:** 2.5–3.5W (ideal for solar deployment)
- **Sensors:** pH, Turbidity, Nitrogen via ADS1115 I2C ADC
- **Communication:** Ethernet or WiFi 5
- **Reference Guide:** [raspberry_pi_deployment.md](hardware_configs/raspberry_pi_deployment.md)

### Unit B: Biological Detection (Jetson Nano)
**For AI-based species detection with GPU-accelerated inference**
- **Processor:** NVIDIA Tegra X1 + 128-core Maxwell GPU
- **Power:** 5–10W (higher performance, GPU-optimized)
- **Camera:** Raspberry Pi v2 (8 MP) via CSI interface
- **Inference:** TensorFlow Lite with GPU delegate (120–150 ms latency)
- **Reference Guide:** [jetson_nano_deployment.md](hardware_configs/jetson_nano_deployment.md)

### Quick Hardware Comparison

| Feature | Jetson Nano | Raspberry Pi 4B |
|---------|-----------|---|
| **Best For** | AI/computer vision detection | Sensor data + MQTT |
| **Inference Speed** | 120–150 ms (GPU-accelerated) | 180–250 ms (CPU-only) |
| **Power Consumption** | 5W idle → 10W inference | 2.5W idle → 5W active |
| **GPIO/I2C Support** | Limited | Full flexibility (27 GPIO) |
| **Total Cost** | ~$290 (with sensors) | ~$300 (with sensors) |

👉 **See [hardware_configs/README.md](hardware_configs/README.md) for complete platform selection guide, hardware shopping list, and network topology.**

---

## Data Samples & Field Validation

The `data_samples/` directory contains representative datasets from field deployments at Sasthamcotta Lake:

### Available Datasets
- **sensor_readings_2026_02.csv:** 30 days of hourly physico-chemical data
  - pH, Turbidity (NTU), Nitrogen (mg/L), Temperature, Battery SOC, Signal Strength
  - 720 measurements per month
  
- **biological_detections_2026_02.csv:** 30 days of AI classification results
  - Species detected (Healthy Algae, Chaoborus spp., E. coli)
  - Confidence scores (0.70–0.99 range)
  - Model version tracking

📊 **Load sample data for analysis:**
```python
import pandas as pd

# Sensor data
sensors = pd.read_csv('data_samples/sensor_readings_2026_02.csv')
print(f"pH (mean): {sensors['ph'].mean():.2f}")
print(f"Turbidity (mean): {sensors['turbidity_ntu'].mean():.2f}")

# Biological detections
bio = pd.read_csv('data_samples/biological_detections_2026_02.csv')
high_conf = bio[bio['confidence_score'] > 0.90]
print(f"High-confidence detections: {len(high_conf)}/{len(bio)}")
```

👉 **See [data_samples/README.md](data_samples/README.md) for data interpretation guide and usage examples.**

---

## Tech Stack

### Hardware
- Raspberry Pi / Low-power SBC
- Solar charge controller integration
- Environmental sensors (pH, turbidity, nitrogen probes)

### Software & AI/ML
- **Language:** Python 3.13+
- **Scientific Computing:** NumPy, SciPy
- **Deep Learning:** TensorFlow Lite (edge inference)
- **Data Processing:** Pandas
- **Communication:** MQTT (low-bandwidth telemetry)
- **Hardware Integration:** RPi.GPIO, Adafruit CircuitPython

---

## Project Structure

```
eco-guard-ramsar/
├── main.py                          # Entry point - field deployment loop
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── src/
│   ├── __init__.py                 # Package initialization
│   └── bio_monitor.py              # Biological indicator AI engine
├── models/                          # TensorFlow Lite model files
├── data_samples/                   # Representative field data
│   ├── README.md                   # Data documentation
│   ├── sensor_readings_2026_02.csv # 30 days of physico-chemical data
│   └── biological_detections_2026_02.csv # 30 days of AI detection results
├── hardware_configs/               # Platform-specific deployment guides
│   ├── README.md                   # Hardware comparison & selection guide
│   ├── jetson_nano_deployment.md   # Unit B setup (AI/GPU optimization)
│   ├── raspberry_pi_deployment.md  # Unit A setup (sensors/GPIO)
│   ├── sensor_calibration.yaml     # Analog sensor calibration values
│   ├── mqtt_config.env             # MQTT broker credentials (template)
│   ├── tflite_model_config.yaml    # TensorFlow Lite inference config
│   └── power_management.yaml       # Solar charging & power budgets
└── .git/                           # Version control
```

### Key Modules

#### `src/bio_monitor.py`
Implements the biological indicator detection system:
- `BiologicalIndicatorAI` class for species detection
- Statistical inference or TFLite model integration
- Support for E. coli and Chaoborus spp. identification
- Confidence scoring for detection results

#### `main.py`
Main field deployment loop:
- Collects physico-chemical parameters (pH, Turbidity, Nitrogen)
- Triggers biological AI analysis
- Logs all measurements with timestamps
- Runs continuously until user interruption (Ctrl+C)
- Comprehensive error handling for sensor/inference failures

---

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Virtual environment (recommended)

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd eco-guard-ramsar
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
```

**Activate Virtual Environment:**
- **Windows:** `.venv\Scripts\activate`
- **macOS/Linux:** `source .venv/bin/activate`

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**For Development** (includes testing tools):
```bash
pip install -r requirements.txt pytest black pylint
```

### Step 4: Verify Installation
```bash
python -c "from src.bio_monitor import BiologicalIndicatorAI; print('Installation successful!')"
```

---

## Running the Monitoring System

### Quick Start
```bash
python main.py
```

### Sample Output
```
[2026-02-17 10:52:41] INFO: [POWER] Solar-Powered Monitoring Unit Active: Sasthamcotta Lake (Ramsar Site)
[2026-02-17 10:52:41] INFO: [UPTIME] Target: 98% operational availability
[2026-02-17 10:52:41] INFO: [INIT] Biological Indicator Engine Initialized...
[DATA #1] pH: 8.42 | Turbidity: 4.18 NTU | Nitrogen: 1.64 mg/L
[AI]   Detection: Healthy Algae (confidence: 92.72%)
----------------------------------------------------------------------
[DATA #2] pH: 6.68 | Turbidity: 2.88 NTU | Nitrogen: 1.24 mg/L
[AI]   Detection: Healthy Algae (confidence: 91.87%)
----------------------------------------------------------------------
```

### Stop Monitoring
Press `Ctrl+C` to safely shutdown the unit.

---

## Deployment Configuration

### Environment Variables (optional)
Create a `.env` file in the root directory:
```env
# MQTT Configuration
MQTT_BROKER=<broker-address>
MQTT_PORT=1883
MQTT_TOPIC=ramsar/sasthamcotta/telemetry

# Sensor Calibration
PH_CALIBRATION_OFFSET=0.0
TURBIDITY_SCALE=1.0
NITROGEN_SCALE=1.0

# Inference Settings
CONFIDENCE_THRESHOLD=0.85
```

---

## Troubleshooting

### Import Error: `ModuleNotFoundError: No module named 'src'`
**Solution:** Ensure you're running from the project root directory:
```bash
cd eco-guard-ramsar
python main.py
```

### Missing Dependencies
**Solution:** Install all requirements:
```bash
pip install -r requirements.txt
```

### Sensor Data Not Reading
**Check:**
1. GPIO connections are properly secured
2. Sensor firmware is up to date
3. I2C/SPI interfaces enabled (Raspberry Pi): `sudo raspi-config`

### AI Detection Issues
**Check:**
1. TensorFlow Lite installed: `pip install tensorflow-lite`
2. Model file path is correct if using `bio_classifier.tflite`

---

## Development Workflow

### Code Quality
```bash
# Format code
black src/ main.py

# Check for issues
pylint src/

# Run tests (if tests directory exists)
pytest tests/
```

### Contributing
1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test locally
3. Commit with clear messages: `git commit -m "Add feature description"`
4. Push to repository and submit pull request

---

## Dependencies Overview

| Package | Version | Purpose |
| :--- | :--- | :--- |
| `numpy` | ≥1.24.0 | Scientific computing |
| `scipy` | ≥1.10.0 | Advanced math/statistics |
| `tensorflow-lite` | ≥2.13.0 | Edge AI inference |
| `pandas` | ≥2.0.0 | Data handling |
| `paho-mqtt` | ≥1.6.1 | IoT communication |
| `RPi.GPIO` | ≥0.7.0 | Raspberry Pi GPIO |
| `Pillow` | ≥9.5.0 | Image processing |

See `requirements.txt` for complete dependency list with version specifications.

---

## Future Enhancements

- Real-time data dashboard with web UI
- Cloud synchronization with local fallback storage
- Multi-model inference pipeline
- Battery health monitoring and predictive maintenance
- Mobile app for remote monitoring and alerts

---

## GitHub Repository Configuration

To maximize discoverability and showcase this project's unique impact, configure your GitHub repository as follows:

### 1. Repository Description (160 characters)
Copy and paste into the **"About" section** (via the ⚙️ gear icon):

> **Solar-powered Edge-AI for wetland monitoring at Ramsar sites. Integrates physico-chemical sensors with AI-based biological indicator detection. 🌿🔋**

### 2. Add Repository Topics
In the repository settings, add these topic tags under **Topics**:
- `edge-ai`
- `iot`
- `environmental-monitoring`
- `sustainability`
- `smart-water`
- `raspberry-pi`
- `tensorflow-lite`
- `ramsar-wetlands`
- `conservation-tech`

These tags improve discoverability for:
- IoT and hardware recruiters
- Environmental science teams
- Sustainability-focused organizations
- Green technology initiatives (e.g., Singapore's Green Plan 2030)

### 3. Steps to Update
1. Navigate to your `eco-guard-ramsar` repository on GitHub
2. Click the **Settings** tab
3. In the left sidebar, scroll to **"About"** section
4. Click the **⚙️ cog icon** to edit repository details
5. Paste the 160-character description
6. Add the topic tags listed above
7. Set visibility to **Public** (for portfolio visibility)
8. Click **Save changes**

---

## License & Citation

If using this work in research, please cite:

```bibtex
@software{vidya2026ecoguard,
  author = {Vidya, Swapin},
  title = {Eco-Guard-Ramsar: Edge-AI Systems for Ecological Monitoring},
  year = {2026},
  organization = {PeachBot Technologies (Agastya Biologic Solutions)}
}
```

---

## References

- [TensorFlow Lite Guide](https://www.tensorflow.org/lite)
- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
- [MQTT Specification](https://mqtt.org/)
- [Ramsar Convention on Wetlands](https://www.ramsar.org/)

---

**Last Updated:** February 17, 2026  
**Project Status:** Production Deployment  
**Python Version:** 3.10+