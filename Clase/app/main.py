from fastapi import FastAPI, Request, HTTPException
#from app.monitoring.performance import measure_request_time
#from app.monitoring.logging import log_error
from app.monitoring.costs import log_openai_cost
from app.database import supabase_client
from openai import OpenAI
import os

app = FastAPI()

# Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Middleware de monitoreo de rendimiento (APM)
#app.middleware("http")(measure_request_time)

@app.get("/")
async def root():
    return {"message": "API de monitoreo en ejecución 🚀"}

# Endpoint para probar errores y monitoreo de logging
@app.get("/error")
async def trigger_error():
    try:
        1 / 0  # Error forzado
    except Exception as e:
        log_error("/error", str(e))
        raise HTTPException(status_code=500, detail="Error interno registrado")

# Endpoint para generar respuesta con OpenAI y monitorear costos
@app.post("/generate")
async def generate_response(prompt: str, model: str = "gpt-3.5-turbo"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )

        tokens_used = response.usage.total_tokens
        cost = log_openai_cost(model, tokens_used)

        return {"response": response.choices[0].message.content, "tokens_used": tokens_used, "cost": cost}
    except Exception as e:
        log_error("/generate", str(e))
        raise HTTPException(status_code=500, detail="Error generando respuesta")