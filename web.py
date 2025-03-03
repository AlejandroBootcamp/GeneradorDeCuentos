from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Modelo de datos esperado en la petición POST
class HistoriaRequest(BaseModel):
    nombre_protagonista: str
    genero: str

@app.get("/{nombre}/{genero}")
def obtener_datos(nombre: str, genero: str):
    """Devuelve los datos enviados en la URL."""
    return {"nombre_protagonista": nombre, "genero": genero}

@app.post("/generar_historia")
async def generar_historia(request: HistoriaRequest):
    """Recibe los datos en un POST y los imprime en la consola."""
    nombre_protagonista = request.nombre_protagonista
    genero = request.genero

    # Imprimir en la consola del backend
    print(f"Nombre del protagonista: {nombre_protagonista}")
    print(f"Género de la historia: {genero}")

    # Responder a Streamlit
    return {"mensaje": f"Historia de {genero} con {nombre_protagonista} recibida en backend."}

# Ejecutar el servidor solo si se ejecuta este archivo directamente
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
