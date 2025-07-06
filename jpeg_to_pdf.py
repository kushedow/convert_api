import base64

import img2pdf
from fastapi import HTTPException


def convert_jpeg_file_to_pdf(file_base64):
    try:

        image_data = base64.b64decode(file_base64)
        pdf_bytes = img2pdf.convert(image_data)
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        return pdf_base64

    except Exception as e:
        raise HTTPException(400, detail=f"Ошибка конвертации изображения: {str(e)}")
