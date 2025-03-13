from openai import OpenAI
import supabase
from datetime import datetime
from app.database import supabase_client
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TABLE_NAME = "cost_logs"

TOKEN_COSTS = {"gpt-4": 0.03 / 1000, "gpt-3.5-turbo": 0.002 / 1000}

def log_openai_cost(model: str, tokens_used: int):
    cost = tokens_used * TOKEN_COSTS.get(model, 0)
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "model": model,
        "tokens_used": tokens_used,
        "cost": cost
    }
    supabase_client.table(TABLE_NAME).insert(log_data).execute()
    return cost