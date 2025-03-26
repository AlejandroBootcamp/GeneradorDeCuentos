from backend.core.factory import ModelFactory
from backend.services.openai_client import OpenAIClient

@ModelFactory.register("openai")
class OpenAIModel:
    def __init__(self, api_key):
        self.client = OpenAIClient(api_key)

    def generate_tale(self, genre, name, description, qa_pairs=None):
        system_message = {
            "role": "system",
            "content": (
                "Eres un generador de historias cortas especializado en cuentos infantiles. "
                "Debes crear historias con introducción, nudo y desenlace claros, separados por saltos de línea.\n"
                "Instrucciones adicionales:\n"
                "- Incorpora detalles de personalidad basados en las preguntas/respuestas proporcionadas\n"
                f"- Mantén un tono apropiado para el género: {genre}\n"
                f"- El protagonista debe llamarse: {name}"
            )
        }

        qa_context = ""
        if qa_pairs and isinstance(qa_pairs, dict):
            qa_context = "\n\nContexto de personalidad:\n"
            qa_context += "\n".join([f"- {q} → {a}" for q, a in qa_pairs.items()])

        user_message = {
            "role": "user",
            "content": (
                f"Género: {genre}\n"
                f"Protagonista: {name}\n"
                f"Descripción base: {description}\n"
                f"{qa_context}\n\n"
                "Por favor genera una historia coherente que integre todos estos elementos."
            )
        }

        response = self.client.generate_text(
            messages=[system_message, user_message]
        )

        return response.split("\n\n")

    def describe_image(self, image_url=None, base64_image=None):
        return self.client.describe_image(image_url, base64_image)

    def request_questions(self):

        system_message = {
            "role": "system",
            "content": ("Elabora 5 preguntas aleatorias para la creación de la personalidad de un personaje"
                       "ficticio. Las preguntas deben de ser sencillas y de situaciones concretas en las que dicho personaje"
                       "pueda verse envuelto. Para la realización de las preguntas ten en cuenta que en base a las respuestas de dichas preguntas se basará la personalidad"
                       "del protagonista. Quiero que la respuesta sea únicamente una lista de python  y que esté preparada para que sea tratada, es decir, que no"
                        "esté comentada."
                        )
        }

        response  = self.client.request_questions(message=[system_message])
        return response