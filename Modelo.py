import openai
import base64

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ModelFactory:
    @staticmethod
    def create_model(type,api_key, base_url):
        match type:
            case "text":
                return TextModel(api_key, base_url)
            case "image":
                return ImageModel(api_key, base_url)
            case _:
                raise ValueError(f"Unrecognized model type: {type}")

class Modelo(metaclass=Singleton):
    def __init__(self,api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        openai.api_key = self.api_key

    def clean_prompt(self,prompt): #Método para limpiar el prompt
        prompt = prompt.strip()
        prompt = prompt.capitalize()
        return prompt

class TextModel(Modelo):
    def generate_tale(self, genre, name, text):
        completion = openai.chat.completions.create(  ##funcion openAI Petición POST
            model= "gpt-4-turbo",
            messages=[
                {"role": "system",
                 "content": f"Eres un generador de historias cortas. Tu trabajo es crear cuentos infantiles breves. El género de la historia, el nombre del protagonista y su descripción se proporcionarán en el mensaje del usuario. La historia no debe exceder los dos párrafos."},
                {"role": "user", "content": f"Quiero que el género sea {genre}, el nombre del protagonista sea {name}, y su descripción sea {text}, y esto."},
            ],
            temperature=0.7,  ## aleatoriedad creatividad/respuesta
            max_tokens=4096,  ## limite
        )
        response = completion.choices[0].message.content
        return response

    def describe_image(self, image_path):
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        except FileNotFoundError:
            return "Error: The specified image file was not found."

        image_obj = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}

        try:
            response = openai.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente que describe imágenes de forma breve y precisa."},
                    {"role": "user", "content": [
                        {"type": "text", "text": "Describe esta imagen brevemente en pocas palabras y de manera concisa."},
                        image_obj
                    ]}
                ],
                max_tokens=100
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error processing image: {e}"

class ImageModel(Modelo):
    def generate_tale_image(self, prompt):
        aux = prompt + ". I want a Pixar 3D render cartoon image style."
        try:
            response = openai.images.generate(prompt=aux, size="1024x1024", n=1)
            return response.data[0].url
        except Exception as e:
            return f"Error generating image: {e}"