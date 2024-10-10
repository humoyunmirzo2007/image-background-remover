from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from rembg import remove
import cv2
import numpy as np
from PIL import Image
import io

app = FastAPI()

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    image_data = await file.read()

    input_image = Image.open(io.BytesIO(image_data))

    image_without_bg = remove(input_image)

    image_without_bg = image_without_bg.convert("RGBA")

    open_cv_image = np.array(image_without_bg)

    b, g, r, alpha = cv2.split(open_cv_image)

    _, alpha = cv2.threshold(alpha, 240, 255, cv2.THRESH_BINARY)

    final_image = cv2.merge([b, g, r, alpha])

    final_image_pil = Image.fromarray(final_image)

    background_color = (222, 222, 223, 255)  # RGBA formatda (#dededf)
    background_image = Image.new("RGBA", final_image_pil.size, background_color)

    final_composite = Image.alpha_composite(background_image, final_image_pil)

    output_io = io.BytesIO()
    final_composite.save(output_io, format="PNG")
    output_io.seek(0)  # Faylni boshidan o'qish uchun

    return StreamingResponse(output_io, media_type="image/png", headers={
        "Content-Disposition": f"attachment; filename={file.filename}"
    })
