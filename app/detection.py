import os
from ultralytics import YOLO
from fastapi import HTTPException

model = None


def load_model():
    global model

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(BASE_DIR, "models", "best.pt")

    print(f"📦 Loading model from: {model_path}")

    if not os.path.exists(model_path):
        raise RuntimeError(f"❌ Model not found: {model_path}")

    model = YOLO(model_path)
    print("✅ YOLOv8 model loaded")


def detect_potholes(image_path: str):
    global model

    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        results = model.predict(
            source=image_path,
            conf=0.15,   # 🔥 key fix
            imgsz=640,
            device="cpu",
            verbose=False
        )

        detections = []

        for result in results:
            boxes = result.boxes

            if boxes is not None:
                for box in boxes:
                    confidence = float(box.conf[0])
                    bbox = box.xyxy[0].tolist()

                    detections.append({
                        "confidence": confidence,
                        "bbox": bbox
                    })

        print("DEBUG detections:", detections)  # 🔥 debug

        return {
            "detected": len(detections) > 0,
            "detections": detections
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")