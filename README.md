# Pothole Detection API

A FastAPI-based backend server for detecting potholes in images using a trained YOLOv8 model.

## Requirements

- Python 3.8+
- Trained YOLOv8 model at `runs/detect/train5/weights/best.pt`

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure the YOLOv8 model file exists at the specified path.

## Running the Server

```bash
python api.py
```

Or with uvicorn directly:
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

## API Usage

### POST /detect

Detect potholes in an uploaded image.

**Request (multipart/form-data):**
- `file`: Image file (JPG, PNG, BMP, TIFF)
- `latitude`: Float value for latitude
- `longitude`: Float value for longitude

**Response:**
```json
{
  "detected": true,
  "detections": [
    {
      "confidence": 0.85,
      "bbox": [100.0, 200.0, 300.0, 400.0]
    }
  ]
}
```

## Detection Logic

- Runs YOLOv8 inference with confidence threshold of 0.4
- If any detection has confidence > 0.4, `detected` is set to `true`
- Detections are logged in-memory with location and timestamp

## Troubleshooting

- **Model not found**: Ensure `runs/detect/train5/weights/best.pt` exists
- **Import errors**: Install all requirements with `pip install -r requirements.txt`
- **CORS issues**: CORS is enabled for all origins (adjust in production)
- **Performance**: Model is loaded once at startup for optimal performance