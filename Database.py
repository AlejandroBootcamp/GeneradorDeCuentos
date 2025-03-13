import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime




load_dotenv()

# Credenciales del .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Comprueba si las variables de entorno están bien
if not SUPABASE_URL or not SERVICE_ROLE_KEY:
    raise ValueError("Missing Supabase URL or Service Role Key in environment variables.")

# inicializa supabase
supabase: Client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)
def log_request_cost(operation: str, cost: int):
    """Registrar el costo de una petición en la base de datos."""
    data = {
        "fecha": datetime.utcnow().isoformat(),  # Guarda la fecha en formato ISO
        "operacion": operation,
        "costo": cost
    }

    response = supabase.table("costos_peticiones").insert(data).execute()
    return response


def insert_data2(personaje: str, genero: str, descripcion: str):
    """Insertar un cuento y registrar el costo de la petición."""
    COSTO_INSERT = 5

    data = {"personaje": personaje, "genero": genero, "historia": descripcion}
    response = supabase.table("cuentos").insert(data).execute()

    if response.data:
        log_request_cost("INSERT", COSTO_INSERT)

    return response


def select_data():
    """Seleccionar cuentos y registrar el costo de la petición."""
    COSTO_SELECT = 1

    response = supabase.table("cuentos").select("*").execute()

    if response.data:
        log_request_cost("SELECT", COSTO_SELECT)

    return response


def update_data(email: str, updates: dict):
    """Actualizar un cuento y registrar el costo de la petición."""
    COSTO_UPDATE = 3

    response = supabase.table("cuentos").update(updates).eq("email", email).execute()

    if response.data:
        log_request_cost("UPDATE", COSTO_UPDATE)

    return response


def get_total_cost():
    """Obtener el costo total de todas las peticiones realizadas."""
    response = supabase.table("costos_peticiones").select("costo").execute()

    if response.data:
        total_cost = sum(item["costo"] for item in response.data)
        return {"total_cost": total_cost}

    return {"total_cost": 0}


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
    print(select_data())  # Debería costar 1 crédito y registrarse
    print(insert_data2("Mago", "fantasía", "Un mago encuentra una gema mágica."))
    print(update_data("user1@mail.com", {"historia": "Historia modificada"}))
    print(get_total_cost())  # Debería mostrar el costo total registrado
