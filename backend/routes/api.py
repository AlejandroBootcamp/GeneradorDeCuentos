from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException, Form, File, UploadFile, Response
from typing import Optional, Dict
from backend.core.factory import ModelFactory
from ..models.openai_model import OpenAIModel
from ..models.segmind_model import SegmindModel
import base64
from fastapi.responses import StreamingResponse
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.enums import TA_JUSTIFY
import io

api = FastAPI()
load_dotenv()

#OPENAI
key_o = os.getenv("OPENAI_API_KEY", "").strip()
url_o = os.getenv("OPENAI_URL", "").strip()

openai_model = ModelFactory.create_model("openai", key_o)

#SEGMIND
key_s = os.getenv("SEGMIND_API_KEY", "").strip()

url_s_i = os.getenv("SEGMIND_URL_IMG", "").strip()
url_s_v = os.getenv("SEGMIND_URL_VOICE", "").strip()

segmind_model_i = ModelFactory.create_model("segmind", key_s, url_s_i)
segmind_model_v = ModelFactory.create_model("segmind", key_s, url_s_v)

class TaleRequest(BaseModel):
    genre:str
    name:str
    description:str
    qa_pairs: Optional[Dict[str, str]] = None

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

    if image_file:
        image_data = await image_file.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")
        description = openai_model.describe_image(base64_image=base64_image)
    else:
        description = openai_model.describe_image(image_url=image_url)

    return {'description':description}

@api.post("/request-questions/")
async def request_questions():
    res = openai_model.request_questions()
    return{'questions':res}

@api.post("/generate-tale/")
async def generate_tale(tale_request:TaleRequest):

    result = openai_model.generate_tale(
        genre=tale_request.genre,
        name=tale_request.name,
        description=tale_request.description,
        qa_pairs=tale_request.qa_pairs
    )

    print(tale_request.qa_pairs)

    return {
        "tale": result,
        "metadata": {
            "genre": tale_request.genre,
            "name": tale_request.name,
            "qa_used": bool(tale_request.qa_pairs)
        }
    }

#TODO::Formateo JSON
@api.post("/generate-image/")
async def generate_image(generate_image_request:GenerateImageRequest):
    genre = generate_image_request.genre
    description = generate_image_request.description
    image_data = segmind_model_i.generate_image(genre, description)
    image_stream = io.BytesIO(image_data)
    return StreamingResponse(image_stream, media_type="image/png")

#TODO::Formateo JSON
@api.post("/narrate-tale/")
async def narrate_tale(narrator:NarratorRequest):
    audio_data = segmind_model_v.narrated_tale(narrator.tale)
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


def generate_pdf(story, image_bytes=None, filename="cuento_generado.pdf"):
    try:
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        margins = {
            'left': 50,
            'right': 50,
            'top': 50,
            'bottom': 50
        }
        usable_width = width - margins['left'] - margins['right']
        usable_height = height - margins['top'] - margins['bottom']

        styles = getSampleStyleSheet()
        custom_style = ParagraphStyle(
            'Custom',
            parent=styles['Normal'],
            fontSize=12,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        )

        if image_bytes:
            try:
                img = ImageReader(io.BytesIO(image_bytes))
                img_width, img_height = img.getSize()

                max_img_width = usable_width
                max_img_height = usable_height * 0.4

                ratio = min(max_img_width / img_width, max_img_height / img_height)
                img_width *= ratio
                img_height *= ratio

                img_x = (width - img_width) / 2
                img_y = height - margins['top'] - img_height

                pdf.drawImage(img, img_x, img_y, width=img_width, height=img_height)
                text_start_y = img_y - 20
            except Exception as img_error:
                print(f"Error procesando imagen: {img_error}")
                text_start_y = height - margins['top']
        else:
            text_start_y = height - margins['top']

        text_frame = Frame(
            margins['left'],
            margins['bottom'],
            usable_width,
            text_start_y - margins['bottom'],
            leftPadding=0,
            bottomPadding=0,
            rightPadding=0,
            topPadding=0,
            showBoundary=0
        )

        paragraphs = [p for p in story.split('\n\n') if p.strip()]
        story_content = [Paragraph(p, custom_style) for p in paragraphs]

        remaining_content = story_content
        current_y = text_start_y

        while remaining_content:

            if current_y < margins['bottom'] + 100:
                pdf.showPage()
                current_y = height - margins['top']

            available_height = current_y - margins['bottom']

            frame = Frame(
                margins['left'],
                margins['bottom'],
                usable_width,
                available_height,
                leftPadding=0,
                bottomPadding=0,
                rightPadding=0,
                topPadding=0,
                showBoundary=0
            )

            added = frame.addFromList(remaining_content, pdf)
            remaining_content = remaining_content[added:]
            current_y = margins['bottom'] + frame._aH - frame._y

            if remaining_content:
                pdf.showPage()
                current_y = height - margins['top']

        pdf.save()
        buffer.seek(0)
        return buffer

    except Exception as e:
        print(f"Error generando PDF: {e}")
        raise