from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import shutil
import os

from .detection import load_model, detect_potholes
from .utils import save_pothole

app = FastAPI(
    title="Pothole Detection API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    load_model()


@app.post("/detect")
async def detect_endpoint(
    file: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    allowed_extensions = {".jpg", ".jpeg", ".png", ".bmp"}
    ext = os.path.splitext(file.filename.lower())[1]

    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp:
            shutil.copyfileobj(file.file, temp)
            temp_path = temp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        result = detect_potholes(temp_path)

        saved = False

        if result["detected"] and result["detections"]:
            max_conf = max(d["confidence"] for d in result["detections"])

            saved = save_pothole(latitude, longitude, max_conf)

            if saved:
                print(f"✅ Saved pothole @ {latitude},{longitude}")
            else:
                print("⚠️ Duplicate or skipped")

        return {
            "detected": result["detected"],
            "detections": result["detections"],
            "saved": saved
        }

    finally:
        try:
            os.unlink(temp_path)
        except:
            pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
