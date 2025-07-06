import base64
import io

import img2pdf
from fastapi import HTTPException
from PIL import Image, ImageOps


def convert_jpeg_file_to_pdf(file_base64):
    try:

        image_data = base64.b64decode(file_base64)

        # Открываем изображение с помощью Pillow
        img = Image.open(io.BytesIO(image_data))

        # Уменьшаем ширину до 1200 пикселей (сохраняем пропорции)
        if img.width > 1200:
            ratio = 1200 / img.width
            new_height = int(img.height * ratio)
            img = img.resize((1200, new_height), Image.LANCZOS)

        # Конвертируем в RGB если нужно (для JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')

        # Сохраняем в буфер с первоначальным качеством
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG', quality=95)
        compressed_data = img_buffer.getvalue()

        # Если размер больше 500KB - уменьшаем качество
        if len(compressed_data) > 500 * 1024:
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='JPEG', quality=60)  # quality=60 соответствует 0.6
            compressed_data = img_buffer.getvalue()

        pdf_bytes = img2pdf.convert(compressed_data)
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

        return pdf_base64

    except Exception as e:
        raise HTTPException(400, detail=f"Ошибка конвертации изображения: {str(e)}")
