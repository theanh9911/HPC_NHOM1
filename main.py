from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model
import io
import os
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Cho phép truy cập từ mọi domain (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tạo thư mục static nếu chưa tồn tại
STATIC_DIR = "static"
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount thư mục static để phục vụ HTML và các file tĩnh
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

IMG_SIZE = 224

# Tạo lại model với kiến trúc ResNet50
def create_model():
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    predictions = Dense(1, activation='sigmoid')(x)
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Khóa các layer của ResNet50
    for layer in base_model.layers:
        layer.trainable = False
    
    return model

# Load model với xử lý lỗi
model_path = os.path.join("model", "model.h5")
try:
    logger.info(f"Đang load model từ {model_path}")
    # Tạo model mới với kiến trúc giống như khi train
    model = create_model()
    # Load weights từ file đã lưu
    model.load_weights(model_path)
    # Compile model
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    logger.info("Load model thành công")
except Exception as e:
    logger.error(f"Lỗi khi load model: {str(e)}")
    raise RuntimeError(f"Không thể load model: {str(e)}")

# Di chuyển index.html vào thư mục static nếu chưa có
index_path = os.path.join(STATIC_DIR, "index.html")
if not os.path.exists(index_path) and os.path.exists("index.html"):
    import shutil
    shutil.move("index.html", index_path)
    logger.info("Đã di chuyển index.html vào thư mục static")

# Hàm xử lý ảnh
def preprocess_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize((IMG_SIZE, IMG_SIZE))
        # Chuẩn hóa ảnh theo cách của ResNet50
        image = np.array(image)
        image = tf.keras.applications.resnet50.preprocess_input(image)
        return np.expand_dims(image, axis=0)
    except Exception as e:
        logger.error(f"Lỗi khi xử lý ảnh: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Lỗi xử lý ảnh: {str(e)}")

@app.get("/")
async def read_root():
    """Endpoint chính để phục vụ trang chủ"""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/health")
async def health_check():
    """Endpoint kiểm tra trạng thái server"""
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict")
async def predict(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="Không có file nào được upload")
    
    results = []
    for file in files:
        try:
            if not file.content_type.startswith("image/"):
                results.append({
                    "filename": file.filename,
                    "error": "File không phải ảnh"
                })
                continue

            image_bytes = await file.read()
            img = preprocess_image(image_bytes)
            pred_prob = model.predict(img, verbose=0)[0][0]
            label = "PNEUMONIA" if pred_prob > 0.5 else "NORMAL"
            
            results.append({
                "filename": file.filename,
                "prediction": label,
                "confidence": float(pred_prob)
            })
        except Exception as e:
            logger.error(f"Lỗi khi xử lý file {file.filename}: {str(e)}")
            results.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return JSONResponse(content=results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
