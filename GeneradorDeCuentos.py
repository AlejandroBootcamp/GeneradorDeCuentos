from openai import OpenAI
from Modelo import Modelo
import os

def main():
    client = OpenAI()
    key = os.getenv(
        "")
    model = Modelo(key,"gpt-3.5-turbo","https://api.openai.com/v1")
    print(model.generate_response("Quiero que el género sea de aventuras y el protagonista sea un niño pelirrojo"))

if __name__ == "__main__":
    main()
