# 🛣️ RoadSense: Edge AI Inference Engine

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/YOLOv8-Medium-FF6F00?logo=ultralytics&logoColor=white)](https://github.com/ultralytics/ultralytics)
[![Inference Resolution](https://img.shields.io/badge/Input%20Resolution-800x800-4B0082)]()
[![Target Hardware](https://img.shields.io/badge/Hardware-NVIDIA%20Jetson%20%2F%20Raspberry%20Pi-76B900?logo=nvidia&logoColor=white)]()
[![Hackathon](https://img.shields.io/badge/SIH%202026-PS26124-blueviolet)]()
[![Integration Status](https://img.shields.io/badge/Backend%20Contract-Verified%20%E2%9C%93-brightgreen)]()

> **SIH 2026 — PS26124: "AI-Powered Mobile Urban Intelligence Platform Using Public Transport Fleet"**  
> *Organization:* Bharat Electronics Limited (BEL)  
> *Module:* Onboard Edge Computer Vision Engine (Potholes & Missing Zebra Crossings)

---

## 📌 Executive Summary

**RoadSense** turns public transport buses into distributed smart-city surface scanners. Instead of streaming continuous, heavy HD video back to central infrastructure, this module performs **intelligent edge processing** directly on bus-mounted hardware.

The edge vision engine monitors forward-facing camera feeds and IMU telemetry to detect:
1. **Potholes & Road Surface Degradation** with automatic pixel-area severity estimation (`1 = Low`, `2 = Medium`, `3 = High`).
2. **Missing / Faded Zebra Crossings** to flag compromised pedestrian safety zones.
3. **Sensor-Fusion Triggering:** Coordinates with onboard accelerometer spikes to verify road shock events, slashing edge compute and cellular bandwidth by up to 90%.

---

## 📂 Repository Architecture

```text
RoadSense_ML_Edge/
├── configs/
│   └── data.yaml                   # Dataset paths and target class indices
├── models/
│   └── roadsense_yolov8/
│       └── weights/
│           ├── best.pt             # Trained weights (YOLOv8m @ 800px)
│           └── README.md           # Model provenance & export details
├── src/
│   ├── modules/
│   │   ├── __init__.py
│   │   └── severity.py             # Spatial bounding-box severity scoring
│   ├── utils/
│   │   ├── __init__.py
│   │   └── formatter.py            # API-compliant JSON event serializer
│   ├── __init__.py
│   ├── infer.py                    # Production edge detector class
│   └── train.py                    # Multi-dataset training pipeline
├── tests/
│   └── test_all.py                 # Live camera inference & backend integration test
├── mock_backend.py                 # Local Flask test listener (/api/events)
├── requirements.txt                # Pinned production dependencies
└── README.md                       # Documentation & benchmarks

1. The **IMU accelerometer** continuously monitors vertical road disturbance at low compute cost.
2. When the bus hits a road depression, an **inertial jerk spike ($G_z$)** exceeds the dynamic threshold.
3. The spike triggers the **Vision Engine** to inspect the temporally corresponding video frame.
4. If the vision model confirms a pothole with confidence $\ge 0.40$, an event payload is generated.

---

## 🔬 Dataset Engineering & Multi-Source Fusion

Public road datasets from western contexts fail on Indian roads due to unstructured traffic, high dust, varied asphalt composition, and unstandardized road markings. To ensure domain resilience, three datasets were unified into a single canonical training corpus:

| Dataset | Provider / Source | Raw Images | Classes Utilized | Engineering Justification |
| :--- | :--- | :---: | :--- | :--- |
| **RDD2022-India** | CRDDC Challenge / IIT Roorkee | 4,200+ | `D40` (Pothole), `D43` (Crosswalk Blur) | Captures genuine Indian asphalt textures, lighting, and degradation |
| **CrosswalkCDNet** | Vehicle Dashcam Dataset | 3,434 | `crosswalk` | Dedicated vehicle-mounted dashcam perspective across weather variants |
| **Kaggle Potholes YOLOv8** | Curated Benchmark | 1,977 | `pothole` | High-resolution cavity samples with deep shadow/rim boundaries |

### Class Harmonization & Label Cleaning
Raw source annotations were sanitized through an automated ingestion script:
* **Class 0 (`pothole`)**: Unified from Kaggle Class `0` and RDD2022 Class `6` (`D40`).
* **Class 1 (`missing_zebra`)**: Unified from CrosswalkCDNet Class `0` and RDD2022 Class `7` (`D43`).
* **Noise Removal:** Classes such as `D00` (wheel marks), `D10`/`D20` (surface cracks), and `D50` (manholes) were programmatically purged to eliminate contradictory gradient updates.

---

## 📊 Training Evolution & Empirical Benchmarks

The model was iteratively trained and refined across multiple stages on Kaggle Cloud GPUs (NVIDIA Tesla T4 x2, 16GB VRAM):

### Iteration Progression Table

| Iteration | Architecture | Resolution | Epochs | Key Changes | Precision | Recall | mAP@50 | Operational Note |
| :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :--- |
| **v1 (Baseline)** | YOLOv8n (Nano) | 640x640 | 40 | Base pretrained weights | 65.0% | 64.6% | 65.4% | Pothole recall bottlenecked at 40.5% due to 640px downsampling |
| **v2 (Pro)** | YOLOv8m (Medium) | 800x800 | 50 | Higher resolution, $box=8.5$ | 69.2% | 65.1% | 65.8% | Small defects became visually distinct; feature extraction improved |
| **v3 (Final Engine)** | **YOLOv8m (Medium)** | **800x800** | **100** | **Heavy Augmentations (Mosaic, MixUp), Cosine LR** | **70.7%** | **66.4%** | **66.7%** | **State-of-the-art robustness on real Indian road conditions** |

### Detailed Hyperparameter Configuration

```yaml
# configs/hyperparameters.yaml
model: yolov8m.pt
imgsz: 800
epochs: 100
batch: 8
optimizer: AdamW
lr0: 0.001667
lrf: 0.01
cos_lr: True
box: 8.5        # Heavily penalized bounding box error to optimize spatial fit
cls: 1.5        # Heightened classification loss to prevent defect misclassification
mosaic: 1.0     # 100% mosaic augmentation
mixup: 0.15     # Blended frames to improve occlusion tolerance
degrees: 10.0   # Angular tolerance for bus roll/pitch
patience: 25    # Early stopping window
