from openai import OpenAI
from Modelo import ModelFactory
from Historia import Historia
from dotenv import load_dotenv
import os
load_dotenv()

def main():

    key = os.getenv("OPENAI_API_KEY")

    if not key:
        print("Error: API key not found. Please set the OPEN_API_KEY environment variable.")
        return

    factory = ModelFactory()

    model_text = factory.create_model("text",key,"https://api.openai.com/v1")
    model_image = factory.create_model("image",key,"https://api.openai.com/v1")

    image_path = "nina.jpg"
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return


    descripcion = model_text.describe_image(image_path)
    if not descripcion:
        print("Error: Could not generate image description.")
        return

    genero = input("Género de la historia: ")
    nombre = input("Nombre del protagonista: ")

    historia = model_text.generate_tale(genero, nombre, descripcion)
    if not historia:
        print("Error: Could not generate story.")
        return

    protagonista = model_image.generate_tale_image(descripcion, historia[0], historia[1], historia[2])
    if not protagonista:
        print("Error: Could not generate protagonist image.")
        return

    Historia(protagonista, historia)

    print("Descripción de la imagen:", descripcion)
    print("URL de la imagen generada:", protagonista)
    print("Historia generada:", historia)

if __name__ == "__main__":
    main()
