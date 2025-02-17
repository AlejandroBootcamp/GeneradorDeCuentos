from openai import OpenAI
from Modelo import Modelo
<<<<<<< HEAD
from Historia import Historia
import os

def main():
    key = os.getenv(
        "OPEN_API_KEY")
    model_text = Modelo(key, "gpt-3.5-turbo", "https://api.openai.com/v1")
    model_image = Modelo(key, "dall-e-3", "https://api.openai.com/v1")

    descripcion = model_text.describe_image("dibujo.png")
    protagonista = model_image.generate_tale_image(descripcion)
    genero = input("Género de la historia:\n")
    nombre = input("Nombre del protagonista:\n")
    historia = model_text.generate_tale(genero, nombre, descripcion)

    Historia(protagonista, historia)

    print(descripcion)
    print(protagonista)
    print(historia)

=======
import os

def main():
    client = OpenAI()
    key = os.getenv(
        "")
    model = Modelo(key,"gpt-3.5-turbo","https://api.openai.com/v1")
    print(model.generate_response("Quiero que el género sea de aventuras y el protagonista sea un niño pelirrojo"))

>>>>>>> e854c77ee4966239335293a029521aa2c65bf05b
if __name__ == "__main__":
    main()
