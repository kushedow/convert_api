from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import io
from pypdf import PdfWriter

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
