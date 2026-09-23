# RoadSense ML Edge Node (SIH 2026 - PS26124)

This repository contains the Machine Learning Edge Inference pipeline for RoadSense. 
It is designed to run on onboard bus hardware (Jetson/Raspberry Pi) and communicate strictly via the Backend API Contract.

## Features
- **Pothole Detection (Class 0):** Uses YOLOv8m (800px) with dynamic severity calculation (Low/Medium/High).
- **Zebra Crossing Defect Detection (Class 1):** Detects faded/missing crosswalks.
- **IMU Trigger Integration:** Designed to save bandwidth by triggering pothole inference only on accelerometer jolts.

## How to run locally (Mock Backend)
1. Install dependencies: `pip install -r requirements.txt`
2. Start the mock backend: `python mock_backend.py`
3. (Add `best.pt` to this folder once training is complete).
