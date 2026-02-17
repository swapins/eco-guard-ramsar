# Data Samples - Sasthamcotta Lake Monitoring

This directory contains representative datasets from field deployments at Sasthamcotta Lake, Ramsar Site #1212.

## Dataset Description

### 1. `sensor_readings_2026_02.csv`
**Physico-chemical monitoring data from Unit A (pH, Turbidity, Nitrogen)**

| Column | Data Type | Range | Unit | Notes |
|--------|-----------|-------|------|-------|
| `timestamp` | ISO 8601 | - | - | UTC time of measurement |
| `unit_id` | String | `Unit_A`, `Unit_B` | - | Identifies deployment unit |
| `ph` | Float | 6.5–8.5 | pH | Acidity/basicity of water |
| `turbidity_ntu` | Float | 0.5–5.0 | NTU | Water clarity (high = murky) |
| `nitrogen_mg_l` | Float | 0.5–2.5 | mg/L | Nutrient concentration |
| `temperature_c` | Float | 20.0–35.0 | °C | Water temperature |
| `battery_soc` | Integer | 0–100 | % | Battery state of charge (SOC) |
| `signal_strength_dbm` | Integer | -100 to 0 | dBm | MQTT signal strength (less negative = stronger) |

**Interpretation:**
- **pH 7.45–7.70:** Slightly alkaline water, typical for tropical lakes
- **Turbidity 1.8–3.1 NTU:** Moderate water clarity variation
- **Nitrogen 0.95–1.48 mg/L:** Normal nutrient levels for wetlands
- **Battery SOC drops at night:** indicates solar charging during day
- **Signal strength -40 to -68 dBm:** Acceptable MQTT connectivity

### 2. `biological_detections_2026_02.csv`
**AI-based biological indicator detections from Unit B (image analysis)**

| Column | Data Type | Range | Notes |
|--------|-----------|-------|-------|
| `timestamp` | ISO 8601 | - | UTC time of image capture |
| `unit_id` | String | `Unit_B` | Computer vision unit |
| `species_detected` | String | See below | ML classification result |
| `confidence_score` | Float | 0.7–0.99 | Model confidence (0.0 = uncertain, 1.0 = certain) |
| `image_hash` | String | SHA-256 | Identifies image in `images/` directory |
| `detection_model_version` | String | 1.0.0+ | TFLite model version used |

**Species Categories:**
- **Healthy Algae:** Normal photosynthetic organisms (60% occurrence in data)
- **Chaoborus spp.:** Phantom midges (15–20% occurrence) - indicator of food web health
- **E. coli:** Pathogenic bacteria (10–15% occurrence) - water quality concern

**Confidence Interpretation:**
- `> 0.90`: High confidence detection, suitable for automated alerts
- `0.85–0.90`: Moderate confidence, recommend manual review
- `< 0.85`: Low confidence, may indicate poor image quality or ambiguous sample

---

## Data Collection Protocol

### Sampling Frequency
- **Sensor readings (Unit A):** Every 1 hour
- **Biological images (Unit B):** Every 1 hour (5 minutes post-sensor)
- **Daily samples:** 24 readings per unit per day
- **Monthly data volume:** ~720 sensor records + 720 biological detections

### Field Conditions
- **Location:** Sasthamcotta Lake, Kollam District, Kerala, India
- **Coordinates:** ~8.8°N, 76.5°E
- **Climate:** Tropical monsoon (high humidity, seasonal rainfall)
- **Deployment Period:** Year-round (data shown: February 2026)

---

## Data Quality Notes

### Known Variations
1. **Turbidity spikes** (2.5–3.1 NTU): Likely from wind-driven resuspension
2. **pH drift** (7.45→7.70): Normal diurnal variation from photosynthesis
3. **Confidence score drops** (<0.80): Observed on cloudy days (poor image illumination)
4. **Battery SOC recovery:** 42–98% indicates successful solar charging cycles

### Gaps in Data
- No data recorded during system maintenance (planned downtime)
- Signal strength gaps indicate temporary network disconnections (typical in rural deployment)

---

## Usage Examples

### Python: Load and Analyze
```python
import pandas as pd
import numpy as np

# Load sensor data
sensors = pd.read_csv('sensor_readings_2026_02.csv', parse_dates=['timestamp'])

# Calculate daily averages
daily_ph = sensors.groupby(sensors['timestamp'].dt.date)['ph'].mean()
print(f"Average pH: {daily_ph.mean():.2f}")

# Filter biological detections with high confidence
bio = pd.read_csv('biological_detections_2026_02.csv', parse_dates=['timestamp'])
high_confidence = bio[bio['confidence_score'] > 0.90]
print(f"High-confidence detections: {len(high_confidence)}")
```

### CSV Loading in Excel/Google Sheets
1. Open the CSV file in your spreadsheet tool
2. Set column `timestamp` format to `DateTime`
3. Create pivot tables for daily/weekly summaries
4. Plot pH and turbidity trends over time

---

## Extending with New Data

When adding new field data:

1. **Maintain column order** - do not rearrange columns
2. **Use ISO 8601 timestamps** - format: `YYYY-MM-DD HH:MM:SS`
3. **Validate ranges:**
   - pH: 5.0–9.0 (reject outliers outside 6.0–8.5)
   - Turbidity: 0.0–50.0 NTU (alert if > 5.0)
   - Battery SOC: 0–100% (reject if > 100)
4. **Version the dataset:** Rename old files before adding new data
   - Example: `sensor_readings_2026_02_v1.csv` → `sensor_readings_2026_02_v2.csv`

---

## Related Documentation

- [Hardware Configurations](../hardware_configs/) - Sensor calibration for these parameters
- [Main README](../) - Data processing pipeline and MQTT integration
- [TensorFlow Lite Model](../models/) - Details on biological detection model

---

**Last Updated:** February 17, 2026  
**Data Source:** PeachBot Eco Units A & B, Sasthamcotta Lake
