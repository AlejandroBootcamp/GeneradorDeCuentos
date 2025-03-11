from Modelo import ModelFactory
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException, Form, File, UploadFile, Response
from typing import Optional
import base64
from fastapi.responses import StreamingResponse
import io
import os

api = FastAPI()
factory = ModelFactory()
load_dotenv()

#OPENAI
key_o = os.getenv("OPENAI_API_KEY")
url_o = os.getenv("OPENAI_URL")

#SEGMIND
key_s = os.getenv("SEGMIND_API_KEY")

url_s_i = os.getenv("SEGMIND_URL_IMG")
url_s_v = os.getenv("SEGMIND_URL_VOICE")

class TaleRequest(BaseModel):
    genre:str
    name:str
    description:str

class GenerateImageRequest(BaseModel):
    genre:str
    description:str

class NarratorRequest(BaseModel):
    tale:str

class PDFRequest(BaseModel):
    story: str
    image_bytes: bytes

@api.post("/describe-image/")
async def describe_image(
        image_url: Optional[str] = Form(None),
        image_file: Optional[UploadFile] = File(None)
):
    if not image_url and not image_file:
        raise HTTPException(status_code=400, detail="Debes proporcionar una URL de imagen o un archivo de imagen.")

    model_text = factory.create_model("openai", key_o, url_o)

    if image_file:
        image_data = await image_file.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")
        description = model_text.describe_image(base64_image=base64_image)
    else:
        description = model_text.describe_image(image_url=image_url)

    return {'description':description}

@api.post("/generate-tale/")
async def generate_tale(tale_request:TaleRequest):
    genre = tale_request.genre
    name = tale_request.name
    description = tale_request.description
    model_text = factory.create_model("openai", key_o, url_o)
    res = model_text.generate_tale(genre, name, description)
    return {'tale':res}

@api.post("/generate-image/")
async def generate_image(generate_image_request:GenerateImageRequest):
    genre = generate_image_request.genre
    description = generate_image_request.description
    model_image = factory.create_model("segmind", key_s, url_s_i)
    image_data = model_image.generate_image(genre, description)
    image_stream = io.BytesIO(image_data)
    #image_base64 = base64.b64encode(image_data).decode('utf-8')
    return StreamingResponse(image_stream, media_type="image/png")

@api.post("/narrate-tale/")
async def narrate_tale(narrator:NarratorRequest):
    model_voice = factory.create_model("segmind", key_s, url_s_v)
    audio_data = model_voice.narrated_tale(narrator.tale)
    return Response(content=audio_data, media_type="audio/mp3")


@api.post("/generate-pdf/")
async def generate_pdf_endpoint(request: PDFRequest):
    image_bytes = base64.b64decode(request.image_bytes)

    pdf_buffer = generate_pdf(request.story, image_bytes)

    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=cuento_generado.pdf"}
    )

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io

def generate_pdf(story, image_bytes, filename="cuento_generado.pdf"):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    left_margin = 50
    right_margin = 50
    top_margin = 50
    bottom_margin = 50

    if image_bytes:
        image = ImageReader(io.BytesIO(image_bytes))
        image_width = 300
        image_height = 600

        image_x = (width - image_width) / 2
        image_y = height - top_margin - image_height
        pdf.drawImage(image, image_x, image_y, width=image_width, height=image_height)

    pdf.setFont("Helvetica", 12)
    text = pdf.beginText(left_margin, image_y - 20)
    text.setFont("Helvetica", 12)
    text.setLeading(14)

    max_line_width = width - left_margin - right_margin
    for line in story.split("\n"):
        words = line.split()
        current_line = ""
        for word in words:
            if pdf.stringWidth(current_line + " " + word, "Helvetica", 12) < max_line_width:
                current_line += " " + word if current_line else word
            else:
                text.textLine(current_line)
                current_line = word

        if current_line:
            text.textLine(current_line)

    if text.getY() < bottom_margin:
        pdf.showPage()

    pdf.drawText(text)

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer