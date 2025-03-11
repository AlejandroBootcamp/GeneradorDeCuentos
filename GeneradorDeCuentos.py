from openai import OpenAI
from Modelo import ModelFactory
from dotenv import load_dotenv
import os
import pygame
load_dotenv()

def save_image(response_content, output_filename):
    with open(output_filename, 'wb') as f:
        f.write(response_content)

def save_audio(audio_content, filename="output.mp3"):
    with open(filename, "wb") as audio_file:
        audio_file.write(audio_content)
    print(f"Audio saved as {filename}")

def play_audio(filename="output.mp3"):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def main():

    key1 = os.getenv("OPENAI_API_KEY")
    key2 = os.getenv("SEGMIND_API_KEY")

    if not key1 and key2:
        print("Error: API key not found. Please set the OPEN_API_KEY environment variable.")
        return

    factory = ModelFactory()

    model_text = factory.create_model("segmind",key2,"https://api.segmind.com/v1/tts-eleven-labs")

    x = model_text.narrated_tale("¡Perfecto! El hecho de que puedas guardar el archivo como MP3 en local y reproducirlo confirma que el problema no está en la generación del archivo de audio, sino en cómo se está manejando la respuesta en tu backend o cómo se está enviando al frontend. Vamos a enfocarnos en cómo puedes modificar tu backend para devolver el archivo de audio de manera que Streamlit pueda reproducirlo correctamente.")

    save_audio(x)

    play_audio("output.mp3")


    print(x)

if __name__ == "__main__":
    main()