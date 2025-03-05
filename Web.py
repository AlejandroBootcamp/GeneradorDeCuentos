from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class HistoriaRequest(BaseModel):
    nombre_protagonista: str
    genero: str

@app.get("/{nombre}/{genero}")
def obtener_datos(nombre: str, genero: str):
    return {"nombre_protagonista": nombre, "genero": genero}

@app.post("/generar_historia")
async def generar_historia(request: HistoriaRequest):
    nombre_protagonista = request.nombre_protagonista
    genero = request.genero

    print(f"Nombre del protagonista: {nombre_protagonista}")
    print(f"Género de la historia: {genero}")

    return {"mensaje": f"Historia de {genero} con {nombre_protagonista} recibida en backend."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)