from openai import OpenAI
from Modelo import Modelo
from Historia import Historia
import os


def main():
    # Obtener API Key de entorno y verificar si está definida
    key = os.getenv("OPEN_API_KEY")
    if not key:
        print("Error: API key not found. Please set the OPEN_API_KEY environment variable.")
        return  # Salir si la API key no está configurada

    # Crear modelos para texto e imágenes
    model_text = Modelo(key, "gpt-3.5-turbo", "https://api.openai.com/v1")
    model_image = Modelo(key, "dall-e-3", "https://api.openai.com/v1")

    # Verificar si el archivo de imagen existe antes de procesarlo
    image_path = "dibujo.png"
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return  # Salir si la imagen no existe

    # Generar descripción de la imagen
    descripcion = model_text.describe_image(image_path)
    if not descripcion:
        print("Error: Could not generate image description.")
        return  # Salir si la descripción está vacía

    # Generar imagen basada en la descripción
    protagonista = model_image.generate_tale_image(descripcion)
    if not protagonista:
        print("Error: Could not generate protagonist image.")
        return  # Salir si falla la generación de la imagen

    # Pedir datos al usuario
    genero = input("Género de la historia:")
    nombre = input("Nombre del protagonista:")

    # Generar la historia
    historia = model_text.generate_tale(genero, nombre, descripcion)
    if not historia:
        print("Error: Could not generate story.")
        return  # Salir si la historia está vacía

    # Mostrar la historia con la imagen
    Historia(protagonista, historia)

    # Imprimir resultados en consola
    print("Descripción de la imagen:", descripcion)
    print("URL de la imagen generada:", protagonista)
    print("Historia generada:", historia)


if __name__ == "__main__":
    main()