from backend.core.factory import ModelFactory
from backend.services.segmind_client import SegmindClient

@ModelFactory.register("segmind")
class SegmindModel:
    def __init__(self, api_key: str, base_url: str):
        self.client = SegmindClient(api_key, base_url)

    def generate_image(self, genre: str, desc: str):
        estilo = (
            "Ilustración digital en alta calidad con estilo de fantasía realista. "
            "Colores vibrantes, iluminación cinematográfica y detalles bien definidos. "
            "Trazos suaves y renderizado completo, sin apariencia de boceto. "
            "Sombreado detallado con profundidad realista y texturas refinadas. "
            "Inspirado en la animación clásica de Disney en 2D, con un acabado similar a pinturas digitales profesionales."
        )

        data = {
            "prompt": f"Haz un personaje de {genre} siguiendo esta descripción: {desc}. Estilo: {estilo}",
            "aspect_ratio": "9:16"
        }
        return self.client.generate_image(data)

    def narrated_tale(self, prompt: str):
        data = {
            "prompt": prompt,
            "voice": "Will"
        }
        return self.client.narrate_tale(data)