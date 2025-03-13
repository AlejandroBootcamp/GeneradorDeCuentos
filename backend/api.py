from Modelo import ModelFactory
import os
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException, Form, File, UploadFile
from typing import Optional
import base64
from fastapi.responses import StreamingResponse
import io

api = FastAPI()
factory = ModelFactory()
load_dotenv()

#OPENAI
key_o = os.getenv("OPENAI_API_KEY")
url_o = os.getenv("OPENAI_URL")

#SEGMIND
key_s = os.getenv("SEGMIND_API_KEY")
url_s = os.getenv("SEGMIND_URL")

#TODO::Probar URL
@api.post("/describe-image/")
async def describe_image(
        image_url: Optional[str] = Form(None),
        image_file: Optional[UploadFile] = File(None)
):
    if not image_url and not image_file:
        raise HTTPException(status_code=400, detail="Debes proporcionar una URL de imagen o un archivo de imagen.")

    model_text = factory.create_model("text", key_o, url_o)

    if image_file:
        image_data = await image_file.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")
        result = model_text.describe_image(base64_image=base64_image)
        print(result["description"])
        print(result["tokens_used"])
    else:
        result = model_text.describe_image(image_url=image_url)

    return result


class TaleRequest(BaseModel):
    genre:str
    name:str
    description:str

@api.post("/generate-tale/")
async def generate_tale(tale_request:TaleRequest):
    genre = tale_request.genre
    name = tale_request.name
    description = tale_request.description
    model_text = factory.create_model("text", key_o, url_o)
    res = model_text.generate_tale(genre, name, description)
    return {'tale':res}

class GenerateImageRequest(BaseModel):
    genre:str
    description:str

@api.post("/generate-image/")
async def generate_image(generate_image_request:GenerateImageRequest):
    genre = generate_image_request.genre
    description = generate_image_request.description
    model_image = factory.create_model("image", key_s, url_s)
    image_data = model_image.generate_image(genre, description)
    image_stream = io.BytesIO(image_data)
    #image_base64 = base64.b64encode(image_data).decode('utf-8')
    return StreamingResponse(image_stream, media_type="image/png")