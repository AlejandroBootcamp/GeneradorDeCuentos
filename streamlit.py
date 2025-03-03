import streamlit as st
import requests
FASTAPI_URL = "http://127.0.0.1:8000/generar_historia"

st.title("Generador de Cuentos")

st.header("Sube una imagen para tu cuento")
imagen = st.file_uploader("Elige una imagen", type=["jpg", "png", "jpeg"])

st.header("Información del protagonista")
nombre_protagonista = st.text_input("Nombre del protagonista:")

st.header("Selecciona el género de la historia")
genero = st.selectbox("Elige un género", ["Acción", "Fantasía", "Ciencia Ficción", "Drama", "Comedia", "Terror"])

if st.button("Generar historia"):
    if nombre_protagonista and genero:
        data = {"nombre_protagonista": nombre_protagonista, "genero": genero}
        response = requests.post(FASTAPI_URL, json=data)

        if response.status_code == 200:
            st.success(f"Historia de {genero} con {nombre_protagonista} enviada al backend.")
            #st.write("Respuesta del backend:", response.json()) #Esta linea la usé para comprobar q funcionaba, borrala si no la necesitas
        else:
            st.error("Error al enviar los datos al backend.")
    else:
        st.warning("Completa todos los campos antes.")
