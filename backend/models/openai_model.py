from backend.core.factory import ModelFactory
from backend.services.openai_client import OpenAIClient

@ModelFactory.register("openai")
class OpenAIModel:
    def __init__(self, api_key):
        self.client = OpenAIClient(api_key)

    def generate_tale(self, genre, name, description):
        system_message = {
            "role": "system",
            "content": "Eres un generador de historias cortas. Tu trabajo es crear cuentos infantiles breves. El género de la historia, el nombre del protagonista y la descripción del protagonista se proporcionarán en el prompt."
                       "La historia debe tener una introducción, un nudo y un desenlace, cada parte estará separada UNICAMENTE con saltos de linea."
        }

        user_message = {
            "role": "user",
            "content": f"Quiero que el género sea {genre}, el nombre del protagonista sea {name}. La descripción del protagonista es {description}."
        }

        response = self.client.generate_text(
            messages=[system_message, user_message]
        )

        return response.split("\n\n")

    def describe_image(self, image_url=None, base64_image=None):
        return self.client.describe_image(image_url, base64_image)