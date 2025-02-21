import requests
import base64
import os
from dotenv import load_dotenv
load_dotenv()

# Use this function to convert an image file from the filesystem to base64
def image_file_to_base64(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return base64.b64encode(image_data).decode('utf-8')

# Use this function to fetch an image from a URL and convert it to base64
def image_url_to_base64(image_url):
    response = requests.get(image_url)
    image_data = response.content
    return base64.b64encode(image_data).decode('utf-8')

def save_image(response_content, output_filename):
    with open(output_filename, 'wb') as f:
        f.write(response_content)


api_key = os.getenv("SEGMIND_API_KEY")
url = "https://api.segmind.com/v1/luma-photon-txt-2-img"

estilo = (
    "Ilustración digital en alta calidad con estilo de fantasía realista. "
    "Colores vibrantes, iluminación cinematográfica y detalles bien definidos. "
    "Trazos suaves y renderizado completo, sin apariencia de boceto. "
    "Sombreado detallado con profundidad realista y texturas refinadas. "
    "Inspirado en la animación clásica de Disney en 2D, con un acabado similar a pinturas digitales profesionales."
)

# Request payload
data = {
  "prompt": f"Retrato de: Niña rubia, expresión preocupada, ojos grandes azules, blusa rosa, corbata a rayas, calcetas rayadas, pose sentada, cabello largo."+
            f"En esta escena introductoria, el personaje se encuentra en En el corazón de un bosque encantado, donde las flores susurraban y los árboles bailaban con el viento, vivía Tadea, una niña con cabellos tan dorados como el sol y ojos azules como el cielo en un día claro. Siempre vestía una blusa rosa con una corbata a rayas y sus calcetas también rayadas se asomaban cada vez que se sentaba en su rincón favorito bajo el Gran Roble de los Secretos." +
            f"Su ropa y expresión reflejan su estado inicial. Fondo detallado acorde a la historia. {estilo} " +
            f"No debe haber texto, letras ni símbolos en la imagen.",
  "aspect_ratio": "1:1"
}

headers = {'x-api-key': api_key}

response = requests.post(url, json=data, headers=headers)
##print(response.content)  # The response is the generated image
save_image(response.content, "generated_image.jpg")
image_base64 = image_file_to_base64("generated_image.jpg")
print("Imagen guardada como generated_image.jpg")