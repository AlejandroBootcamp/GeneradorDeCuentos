from openai import OpenAI
from Modelo import ModelFactory
from Historia import Historia
from dotenv import load_dotenv
import os
load_dotenv()

def save_image(response_content, output_filename):
    with open(output_filename, 'wb') as f:
        f.write(response_content)

def main():

    key1 = os.getenv("OPENAI_API_KEY")
    key2 = os.getenv("SEGMIND_API_KEY")

    if not key1 and key2:
        print("Error: API key not found. Please set the OPEN_API_KEY environment variable.")
        return

    factory = ModelFactory()

    model_text = factory.create_model("text",key1,"https://api.openai.com/v1")

    model_image = factory.create_model("image",key2,"https://api.segmind.com/v1/luma-photon-txt-2-img")

    image_path = "nina.jpg"

    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return

    descripcion = model_text.describe_image_local(image_path)
    print(descripcion)
    if not descripcion:
        print("Error: Could not generate image description.")
        return

    genero = input("Género de la historia: ")
    nombre = input("Nombre del protagonista: ")

    historia = model_text.generate_tale(genero, nombre, descripcion)
    if not historia:
        print("Error: Could not generate story.")
        return

    protagonista = model_image.generate_image(genero, descripcion)
    save_image(protagonista.content, "imagen.jpg")

    #Historia("./imagen.jpg", historia)

    print("Descripción de la imagen:", descripcion)
    print("URL de la imagen generada:", protagonista)
    print("Historia generada:", historia)

if __name__ == "__main__":
    main()