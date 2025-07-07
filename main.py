from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import io
from pypdf import PdfWriter
from xhtml2pdf import pisa

from docx_to_pdf import convert_docx_file_to_pdf
from file_utils import save_base64_as_file, get_file_content_as_base64
from jpeg_to_pdf import convert_jpeg_file_to_pdf
from png_to_pdf import convert_png_file_to_pdf

app = FastAPI(
    title="PDF Merger API",
    description="API to merge multiple Base64 encoded PDF files into one.",
    version="1.0.0",
)

origins = [
    "*"  # Allows all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PDFMergeRequest(BaseModel):
    """
    Represents the request body for merging PDFs.
    It expects a list of Base64 encoded PDF strings.
    """
    files: list[str]


class FileConversionRequest(BaseModel):
    """
    Represents the request body for a single file conversion.
    It expects one Base64 encoded file string.
    """
    file_base64: str


@app.post("/pdf/to/merge", summary="Merge PDF files", response_description="Merged PDF as Base64 string")
async def merge_pdfs(request: PDFMergeRequest):

    merger = PdfWriter()

    try:

        for index, b64_pdf in enumerate(request.files):

            pdf_bytes = base64.b64decode(b64_pdf)
            pdf_file_object = io.BytesIO(pdf_bytes)
            merger.append(pdf_file_object)

        output_pdf_buffer = io.BytesIO()
        merger.write(output_pdf_buffer)
        merger.close()
        merged_pdf_bytes = output_pdf_buffer.getvalue()
        merged_pdf_base64 = base64.b64encode(merged_pdf_bytes).decode('utf-8')

        return {"file_base64": merged_pdf_base64}

    except base64.binascii.Error:

        raise HTTPException(status_code=400, detail="Invalid Base64 string provided for one or more PDF files.")
    except Exception as e:

        raise HTTPException(status_code=400, detail=f"Error merging PDFs: {e}")


@app.post("/docx/to/pdf", summary="Convert DOCX to PDF", response_description="Converted PDF as a Base64 string")
async def docx_to_pdf(request: FileConversionRequest):
    """
    Converts a single DOCX file to PDF.
    - **Prerequisite**: Requires LibreOffice (Linux/macOS) or MS Word (Windows) installed on the server.
    - **Input**: A JSON object with a 'file_base64' key, containing a Base64-encoded DOCX string.
    - **Output**: A JSON object with a 'file_base64' key, containing the converted PDF as a Base64 string.
    """

    file_base64 = request.file_base64
    file_name: str = save_base64_as_file(file_base64, "docx")
    convert_docx_file_to_pdf(f"./temp/{file_name}.docx")
    file_base64 = get_file_content_as_base64(f"./temp/{file_name}.pdf")
    return {"file_base64": file_base64}


@app.post("/png/to/pdf")
async def png_to_pdf(request: FileConversionRequest):
    file_base64 = convert_png_file_to_pdf(request.file_base64)
    return {"file_base64": file_base64}

@app.post("/jpeg/to/pdf")
async def jpeg_to_pdf(request: FileConversionRequest):
    file_base64 = convert_jpeg_file_to_pdf(request.file_base64)
    return {"file_base64": file_base64}


@app.post("/html/to/pdf")
async def html_to_pdf(request: FileConversionRequest):
    """
    Converts HTML content to PDF using xhtml2pdf engine.
    - **Input**: Base64 encoded HTML string
    - **Output**: Base64 encoded PDF document
    """
    try:
        # Decode base64 HTML content
        html_bytes = base64.b64decode(request.file_base64)
        html_content = html_bytes.decode('utf-8')

        # Create a bytes buffer for PDF output
        pdf_buffer = io.BytesIO()

        # Convert HTML to PDF
        pisa_status = pisa.CreatePDF(
            html_content,
            dest=pdf_buffer,
            encoding='utf-8',
            show_error_as_pdf=True
        )

        # Check for conversion errors
        if pisa_status.err:
            raise HTTPException(
                status_code=500,
                detail="HTML to PDF conversion failed"
            )

        # Get PDF bytes and encode to base64
        pdf_bytes = pdf_buffer.getvalue()
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

        return {"file_base64": pdf_base64 }

    except base64.binascii.Error:
        raise HTTPException(status_code=400, detail="Invalid Base64 format")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Conversion error: {str(e)}"
        )


@app.get("/health", summary="Проверка работоспособности сервиса")
async def health_check():
    return {"status": "ok", "message": "Service is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
