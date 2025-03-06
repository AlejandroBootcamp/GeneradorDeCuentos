import openai
import base64
import requests
import base64
import os
from dotenv import load_dotenv
load_dotenv()

class ModelFactory:
    @staticmethod
    def create_model(type, api_key, base_url):
        match type:
            case "text":
                return TextModel(api_key, base_url)
            case "image":
                return ImageModel(api_key, base_url)
            case _:
                raise ValueError(f"Unrecognized model type: {type}")

class Modelo:
    def __init__(self,api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.api_key = api_key

    def handle_error(self, error):
        if isinstance(error, requests.exceptions.RequestException):
            return f"Error en la solicitud HTTP: {str(error)}"
        elif isinstance(error, openai.error.OpenAIError):
            return f"Error en la API de OpenAI: {str(error)}"
        else:
            return f"Error inesperado: {str(error)}"

class TextModel(Modelo):

    def generate_tale(self, genre, name, description):
       try:
        openai.api_key = self.api_key
        completion = openai.chat.completions.create(
            model= "gpt-4-turbo",
            messages=[
                {"role": "system",
                 "content": f"Eres un generador de historias cortas. Tu trabajo es crear cuentos infantiles breves. El género de la historia, el nombre del protagonista y la descripción del protagonista se proporcionarán en el prompt."
                            f"La historia debe tener una introducción, un nudo y un desenlace, cada parte estará separada UNICAMENTE con saltos de linea."},
                {"role": "user", "content": f"Quiero que el género sea {genre}, el nombre del protagonista sea {name}. La descripción del protagonista es {description}."},
            ],
            temperature=0.7,
            max_tokens=4096,
        )

        response = completion.choices[0].message.content

        parts = response.split("\n\n")

        return parts

       except Exception as e:
            return self.handle_error(e)

    def describe_image(self, image_url=None, base64_image=None):
        try:
            if image_url:
                image_obj = {"type": "image_url", "image_url": {"url": image_url}}
            elif base64_image:
                image_obj = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            else:
                return "Error: No se proporcionó una URL de imagen ni una imagen en base64."

            openai.api_key = self.api_key

            response = openai.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system",
                     "content": "Eres un asistente especializado en describir imágenes de manera detallada, incluyendo todos los elementos relevantes, colores, texturas, emociones y contextos visuales. La descripción debe ser lo más completa posible, sin omitir ningún detalle que ayude a generar una imagen precisa y mejorada."},
                    {"role": "user", "content": [
                        {"type": "text",
                         "text": "Describe esta imagen brevemente en pocas palabras y de manera concisa."},
                        image_obj
                    ]}
                ],
                max_tokens=100
            )
            return response.choices[0].message.content

        except Exception as e:
            return self.handle_error(e)

    def describe_image_local(self, image_path):
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        except FileNotFoundError:
            return "Error: The specified image file was not found."

        image_obj = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}

        openai.api_key = self.api_key

        try:
            response = openai.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system",
                     "content": "Eres un asistente especializado en describir imágenes de manera detallada, incluyendo todos los elementos relevantes, colores, texturas, emociones y contextos visuales. La descripción debe ser lo más completa posible, sin omitir ningún detalle que ayude a generar una imagen precisa y mejorada."},
                    {"role": "user", "content": [
                        {"type": "text",
                         "text": "Describe esta imagen brevemente en pocas palabras y de manera concisa."},
                        image_obj
                    ]}
                ],
                max_tokens=100
            )
            return response.choices[0].message.content
        except Exception as e:
            return self.handle_error(e)

class ImageModel(Modelo):
    def generate_image(self, genre, desc):

        estilo = (
            "Ilustración digital en alta calidad con estilo de fantasía realista. "
            "Colores vibrantes, iluminación cinematográfica y detalles bien definidos. "
            "Trazos suaves y renderizado completo, sin apariencia de boceto. "
            "Sombreado detallado con profundidad realista y texturas refinadas. "
            "Inspirado en la animación clásica de Disney en 2D, con un acabado similar a pinturas digitales profesionales."
        )

        data = {
            "prompt": f"Haz un personaje de {genre} siguiendo esta descripción: {desc}. La imagen generada quiero que tenga"
                      f"este estilo: {estilo}",
            "aspect_ratio": "9:16"
        }
        try:
            response = requests.post(
                self.base_url,
                json=data,
                headers={"x-api-key": self.api_key}
            )

            if response.status_code == 200:
                print(f"Response content type: {response.headers['Content-Type']}")
                print(f"Content length: {response.headers['Content-Length']}")

                if "image" in response.headers["Content-Type"]:
                    return response.content
                else:
                    print("Error en la respuesta de la API externa:", response.text)
                    return f"Error: {response.text}"

            else:
                print("Error HTTP:", response.status_code)
                return f"Error HTTP: {response.status_code}"
        except Exception as e:
            return self.handle_error(e)