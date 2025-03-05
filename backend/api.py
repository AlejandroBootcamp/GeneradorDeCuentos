from Modelo import ModelFactory
import os
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI,HTTPException, Form, File, UploadFile
from typing import Optional
import base64

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
        description = model_text.describe_image(base64_image=base64_image)
    else:
        description = model_text.describe_image(image_url=image_url)

    return {"description":description}

@api.post("/generate-tale/")
async def generate_tale(genre:str, name:str, description:str):
    model_text = factory.create_model("text", key_o, url_o)
    res = model_text.generate_tale(genre, name, description)
    return {"tale":res}

@api.post("/generate-image/")
async def generate_image(genre:str, desc:str):
    model_image = factory.create_model("image", key_s, url_s)
    image_data = model_image.generate_image(genre, desc)
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    return {"image": image_base64}