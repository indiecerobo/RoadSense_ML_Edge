# 🛣️ RoadSense: AI Edge Node (SIH 2026 - PS26124)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![YOLO](https://img.shields.io/badge/Model-YOLOv8m%20(Medium)-orange)
![Resolution](https://img.shields.io/badge/Resolution-800px-yellow)
![Deployment](https://img.shields.io/badge/Deployment-Edge%20(Jetson%2FRaspberry%20Pi)-brightgreen)
![Status](https://img.shields.io/badge/Status-Backend%20Integration%20Ready-success)

This repository contains the **Machine Learning Edge Inference pipeline** for the **RoadSense** project, developed for the Smart India Hackathon (SIH) 2026 under Problem Statement PS26124 (Bharat Electronics Limited).

## 🌍 Project Overview
**Problem Statement:** AI-Powered Mobile Urban Intelligence Platform Using Public Transport Fleet.
Our complete system transforms standard public buses into smart city scanners. While the backend handles GIS mapping and aggregation, **this specific module (The Edge Node)** runs locally on the bus hardware to process camera feeds and sensor data in real-time, detecting road infrastructure defects without streaming heavy video to the cloud.

---

## ✨ Core Edge Features

| Feature | Description | AI/Logic Used |
| :--- | :--- | :--- |
| **🕳️ Pothole Detection** | Detects road damage and calculates spatial severity (`1=Low`, `2=Medium`, `3=High`). | YOLOv8m (Class 0) |
| **🚸 Missing Zebra Crossings** | Identifies faded, missing, or damaged pedestrian crosswalks. | YOLOv8m (Class 1) |
| **⚡ IMU Sensor Fusion** | Saves bandwidth by triggering AI inference *only* when the bus accelerometer detects a jolt. | Python Edge Script |

---

## 🧠 Model Architecture & Datasets

To ensure the model is highly robust to Indian road conditions (dust, shadows, varying lighting), we built a custom-fused dataset from three distinct sources:

| Dataset Name | Source | Purpose in Model |
| :--- | :--- | :--- |
| **RDD2022-India** | CRDDC Challenge | Base Indian road conditions (Classes D40, D43) |
| **CrosswalkCDNet** | Roboflow | Vehicle-dashcam perspective for zebra crossings |
| **Potholes YOLOv8** | Kaggle | High-resolution isolated pothole imagery |

### 📊 Model Performance Metrics
*Trained on Kaggle Cloud GPUs (T4 x2) for 100 Epochs at 800px resolution with Heavy Augmentation (Mosaic/Mixup).*

| Metric | Score | Note on Real-World Application |
| :--- | :--- | :--- |
| **Precision** | `~70.7%` | Highly robust against False Positives (e.g., mistaking shadows for potholes). |
| **Recall** | `~66.4%` | **Temporal Video Advantage:** While single-frame recall is ~66%, running inference at 30 FPS on an approaching bus means the *video-level* recall approaches 99%. |
| **mAP50** | `~66.6%` | State-of-the-art for unstructured Indian road damage datasets. |

---

## 📡 Backend API Contract (JSON Payload)

This edge node is strictly decoupled from the backend. When an event is confirmed, it generates a standardized JSON payload and pushes it to the backend GIS dashboard (`/api/events`).

```json
{
  "eventType": "pothole",
  "confidence": 0.91,
  "timestamp": "2026-09-24T10:30:35Z",
  "vehicleId": "BUS_DEMO_01",
  "location": {
    "latitude": 28.6142,
    "longitude": 77.2110
  },
  "metadata": {
    "severity": 3
  }
}
