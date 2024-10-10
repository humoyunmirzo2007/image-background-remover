from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io
import os

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to my API!"}

@app.post("/image")
async def remove_bg(file: UploadFile = File(...)):
    # Faylni o'qish
    image_data = await file.read()

    # Faylni Image ob'ektiga aylantirish
    input_image = Image.open(io.BytesIO(image_data))

    # Fonni o'chirish
    output_image = remove(input_image)

    # Yangi rasmni saqlash uchun io.BytesIO dan foydalanamiz
    output_io = io.BytesIO()
    output_image.save(output_io, format='PNG')
    output_io.seek(0)  # Faylni boshidan o'qish uchun

    # Faylni StreamingResponse yordamida qaytarish
    return StreamingResponse(output_io, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
