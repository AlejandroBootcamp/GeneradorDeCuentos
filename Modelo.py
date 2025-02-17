<<<<<<< HEAD
import openai
import base64
from langchain_core.runnables.utils import Input

class Modelo:
    def __init__(self,api_key, model, base_url):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        openai.api_key = self.api_key

    def generate_tale(self, genero, nombre, texto):
        descripcion = texto
        completion = openai.chat.completions.create(  ##funcion openAI Petición POST
            model= self.model,
            messages=[
                {"role": "system",
                 "content": f"You are a short story generator. Your job is to create brief children's stories. The genre of the story, the name of the protagonist, and their description will be provided in the user's prompt. The story should not exceed two paragraphs."},

                {"role": "user", "content": f"I want the genre to be {genero}, the name of the protagonist to be {nombre}, and their description to be {descripcion}, and this."},
            ],
            temperature=0.7,  ## aleatoriedad creatividad/respuesta
            max_tokens=4096,  ## limite
        )

        response = completion.choices[0].message.content
        return response

    def generate_tale_image(self, prompt):
        aux = prompt + ". I want a Pixar 3D render cartoon image style."
        response = openai.images.generate(  # Generación de imagen
            prompt=aux,
            size="1024x1024",  # Tamaño de la imagen
            n=1  # Número de imágenes a generar
        )

        return response.data[0].url
    
    def describe_image(self, image_path):
        # Leer la imagen en binario y convertirla a base64
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        # Crear el objeto de imagen correctamente
        image_obj = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}

        # Llamar a la API con la imagen
        response = openai.chat.completions.create(
            model="gpt-4-turbo",  # Modelo con soporte de imágenes
            messages=[
                {"role": "system", "content": "You are an assistant who describes images briefly and accurately."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Describe this image briefly in a few words and in a concise manner. Everything you say should be related to the description of the image."},
                    image_obj  # Pasar la imagen en el formato correcto
                ]}
            ],
            max_tokens=100  # Limitar la respuesta
        )

        # Obtener la respuesta
        description = response.choices[0].message.content
        return description

    def clean_prompt(self,prompt):
        prompt = prompt.strip()
        prompt = prompt.capitalize()
        return prompt
