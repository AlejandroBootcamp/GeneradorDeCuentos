import openai
import requests

class OpenAIClient:
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.base_url = base_url

        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

    def generate_text(self, messages, model="gpt-4-turbo", temperature=0.7, max_tokens=4096):
        try:
            completion = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise self.handle_error(e)

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

    def request_questions(self, message, model="gpt-4-turbo", temperature=0.7, max_tokens=4096):
        try:
            completion = openai.chat.completions.create(
                model=model,
                messages=message,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return completion.choices[0].message.content
        except Exception as e:
            raise self.handle_error(e)

    def handle_error(self, error):
        if isinstance(error, requests.exceptions.RequestException):
            return f"Error en la solicitud HTTP: {str(error)}"
        elif isinstance(error, openai.error.OpenAIError):
            return f"Error en la API de OpenAI: {str(error)}"
        else:
            return f"Error inesperado: {str(error)}"