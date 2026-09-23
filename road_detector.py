from ultralytics import YOLO

class RoadSenseDetector:
    def __init__(self, model_path="best.pt", conf_thresh=0.60):
        self.model = YOLO(model_path)
        self.conf_thresh = conf_thresh
        self.class_names = {0: "pothole", 1: "missing_zebra"}

    def predict(self, frame):
        results = self.model(frame, conf=self.conf_thresh, verbose=False)
        detections = []

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                event_name = self.class_names.get(cls_id)
                if not event_name: continue

                detection_dict = {
                    "eventType": event_name,
                    "confidence": round(conf, 2),
                    "metadata": {}
                }

                if event_name == "pothole":
                    coords = box.xyxy[0].tolist()
                    box_area = (coords[2] - coords[0]) * (coords[3] - coords[1])
                    severity = 3 if box_area > 45000 else (2 if box_area > 18000 else 1)
                    detection_dict["metadata"]["severity"] = severity

                detections.append(detection_dict)
        return detections
