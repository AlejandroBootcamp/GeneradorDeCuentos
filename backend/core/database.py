import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Credenciales del .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Comprueba si las variables de entorno están bien
if not SUPABASE_URL or not SERVICE_ROLE_KEY:
    raise ValueError("Missing Supabase URL or Service Role Key in environment variables.")

# inicializa supabase
supabase: Client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

def insert_data(personaje: str, genero: str, descripcion: str):
    """Insertar un nuevo cuento en la tabla 'cuentos'."""
    data = {
        "personaje": personaje,
        "genero": genero,
        "historia": descripcion
    }

    response = supabase.table("cuentos").insert(data).execute()
    return response

#def update_data(table: str, email: str, updates: dict):
    #    """Update records in a Supabase table based on filters."""
    # response = (
    #     supabase.table(table)
    #      .update(updates)
    #      .eq('email',email)
    #     .execute()
    # )
#   return response

#def select_data(table: str, email: str = None):
    # """Select records from a Supabase table based on optional filters."""
    # response = (
    #   supabase.table(table)
    #    .select("*")
    #    .eq('email',email)
    #     .execute()
    # )
# return response

# Example usage
if __name__ == "__main__":
    insert_data("Chico con pelo naranja", "fantasia", "Este es el cuento corto que sirve como ejemplo")
