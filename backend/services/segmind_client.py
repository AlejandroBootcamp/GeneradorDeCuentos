import requests

class SegmindClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def generate_image(self, data: dict):
        try:
            response = requests.post(
                self.base_url,
                json=data,
                headers={"x-api-key": self.api_key}
            )

            if response.status_code == 200:
                if "image" in response.headers["Content-Type"]:
                    return response.content
                return response.json()
            else:
                raise Exception(f"HTTP Error {response.status_code}: {response.text}")
        except Exception as e:
            raise self.handle_error(e)

    def narrate_tale(self, data: dict):

        try:
            response = requests.post(
                self.base_url,
                json=data,
                headers={"x-api-key": self.api_key}
            )

            if response.status_code == 200:
                if "audio" in response.headers.get("Content-Type", ""):
                    return response.content
                else:
                    raise Exception(f"Respuesta inesperada de la API: {response.text}")
            else:
                raise Exception(f"Error HTTP {response.status_code}: {response.text}")

        except Exception as e:
            raise self.handle_error(e)

    def handle_error(self, error):
        if isinstance(error, requests.exceptions.RequestException):
            return f"Error en la solicitud HTTP: {str(error)}"
        else:
            return f"Error inesperado: {str(error)}"