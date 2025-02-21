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
    def create_model(type, api_key, base_url):
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
                 "content": f"Eres un generador de historias cortas. Tu trabajo es crear cuentos infantiles breves. El género de la historia, el nombre del protagonista y la descripción del protagonista se proporcionarán en el prompt."
                            f"La historia debe tener una introducción, un nudo y un desenlace, cada parte separada UNICAMENTE con saltos de linea, y deben de ser breves."},
                {"role": "user", "content": f"Quiero que el género sea {genre}, el nombre del protagonista sea {name}. La descripción del protagonista es {text}."},
            ],
            temperature=0.7,  ## aleatoriedad creatividad/respuesta
            max_tokens=4096,  ## limite
        )

        response = completion.choices[0].message.content

        parts = response.split("\n\n")

        return parts

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
                    {"role": "system", "content": "Eres un asistente que transforma un dibujo de un niño en un personaje de Disney. "},
                    {"role": "user", "content": [
                        {"type": "text", "text": "Haz una descripción breve de este personaje usando solo 'KEYWORDS'. Palabras a evitar en la descripción: Dibujo, simple, trazos"},
                        image_obj
                    ]}
                ],
                max_tokens=100
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error processing image: {e}"

class ImageModel(Modelo):
    def generate_tale_image(self, desc, prompt1, prompt2, prompt3):

        estilo = (
            "Ilustración digital en alta calidad con estilo de fantasía realista. "
            "Colores vibrantes, iluminación cinematográfica y detalles bien definidos. "
            "Trazos suaves y renderizado completo, sin apariencia de boceto. "
            "Sombreado detallado con profundidad realista y texturas refinadas. "
            "Inspirado en la animación clásica de Disney en 2D, con un acabado similar a pinturas digitales profesionales."
        )

        prompts = [
                f"Retrato de {desc}. En esta escena introductoria, el personaje se encuentra en {prompt1}. "
                f"Su ropa y expresión reflejan su estado inicial. Fondo detallado acorde a la historia. {estilo} "
                "No debe haber texto, letras ni símbolos en la imagen.",

                f"Retrato de {desc}. Durante este punto clave de la historia, el personaje está experimentando {prompt2}. "
                f"Su apariencia ha cambiado acorde a la evolución de la historia: sus ropas, expresión y postura reflejan lo que ha vivido. {estilo} "
                "No debe haber texto, letras ni símbolos en la imagen.",

                f"Retrato de {desc}. En la escena final de su historia, el personaje se encuentra en {prompt3}. "
                f"Su vestimenta, expresión y actitud muestran el desenlace de su aventura. {estilo} "
                "No debe haber texto, letras ni símbolos en la imagen."
                ]
        images_urls = []
        try:
            for prompt in prompts:
                response = openai.images.generate(model="dall-e-3",prompt=prompt,size="1024x1024", n=1)
                images_urls.append(response.data[0].url)
            return images_urls
        except Exception as e:
            return f"Error generating image: {e}"