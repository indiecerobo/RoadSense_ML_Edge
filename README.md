# 🛣️ RoadSense ML Edge Node (SIH 2026 - PS26124)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![YOLO](https://img.shields.io/badge/Model-YOLOv8%20Medium-orange)
![Edge](https://img.shields.io/badge/Deployment-Edge%20(Jetson%2FRaspberry%20Pi)-brightgreen)
![Status](https://img.shields.io/badge/Status-Integration%20Ready-success)

This repository contains the **Machine Learning Edge Inference pipeline** for the RoadSense public transport fleet system. It is designed to run locally on onboard bus hardware and communicate strictly via a standardized JSON API contract with the centralized GIS backend.

## ✨ Core Features

*   **🕳️ Pothole Detection (Class 0):** High-resolution (800px) detection of road damage. Automatically calculates severity (`1=Low`, `2=Medium`, `3=High`) based on bounding box spatial area.
*   **🚸 Zebra Crossing Defect Detection (Class 1):** Detects faded, missing, or damaged crosswalks to ensure pedestrian safety.
*   **⚡ IMU Sensor Fusion Trigger:** To minimize bandwidth and CPU usage, continuous video streaming is disabled. The ML model is triggered to capture and infer only when the bus's onboard IMU detects an anomalous Z-axis accelerometer jolt.

## 🧠 Model Architecture & Dataset

The model is trained on a custom-fused dataset combining three major sources:
1.  **RDD2022-India:** Official Indian road damage dataset (Classes D40, D43).
2.  **CrosswalkCDNet:** Vehicle-dashcam perspective crosswalks.
3.  **Kaggle Potholes:** High-resolution isolated pothole imagery.

*   **Algorithm:** YOLOv8m (Medium)
*   **Resolution:** 800x800 for distant defect recognition
*   **Export Format:** `.onnx` for hardware-accelerated edge inference.

## 📡 Backend API Contract (JSON Payload)

The edge node outputs data exactly formatted to the Backend Spec. Example output sent to `/api/events`:

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
