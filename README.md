# Eco-Guard-Ramsar - Edge-AI Ecological Monitoring System
**Edge-AI Systems for Ecological Monitoring in Protected Wetlands**

This repository contains the software framework for the **PeachBot Eco** units deployed at Sasthamcotta Lake, Kerala, India (a designated Ramsar site). The system provides autonomous, solar-powered monitoring of both physico-chemical and biological indicators of wetland health.

---

## Research Foundation

This project implements the technical framework for:  
> *"Dedicated Edge-AI Single-Board Computer Systems for Ecological Monitoring in Protected Wetlands: Evidence from a Ramsar Site in India."*

**Author:** Swapin Vidya  
**Affiliation:** PeachBot Technologies (Agastya Biologic Solutions)

---

## System Architecture

### Dual-Unit Deployment
- **Unit A:** Real-time monitoring of pH, Turbidity, and Nitrogen levels
- **Unit B:** AI-assisted image analysis for biological indicators (E. coli, Chaoborus spp.)

### Performance Metrics
| Metric | Result |
| :--- | :--- |
| **Operational Uptime** | 98% |
| **Inference Latency** | 120–180 ms |
| **Deployment Site** | Sasthamcotta Lake, Kerala, India |
| **Power Source** | Solar with battery backup |

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
├── data_samples/                   # Sample sensor data
├── hardware_configs/               # Hardware-specific configs
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