import requests
import streamlit as st
import io
import base64

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="HistorIA",
    page_icon="📖",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #efe9d6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([2,3])

with col1:
    st.write("")
with col2:
    st.image("./static/images/logo.png", width=300)

def main():

    if "historia_generada" not in st.session_state:
        st.session_state.historia_generada = False
    if "tale" not in st.session_state:
        st.session_state.tale = []
    if "imagen" not in st.session_state:
        st.session_state.imagen = None
    if "image_response" not in st.session_state:
        st.session_state.image_response = None

    col1, col2, col3 = st.columns(3, gap="large", border=True)

    with st.container():
        with col1:
            st.markdown("### Sube una imagen para tu cuento")
            imagen = st.file_uploader("Elige una imagen", type=["jpg", "png", "jpeg"])
            if imagen:
                st.session_state.imagen = imagen.getvalue()

        with col2:
            st.markdown("### Información del protagonista")
            nombre_protagonista = st.text_input("Nombre del protagonista:")

        with col3:
            st.markdown("### Selecciona el género de la historia")
            genero = st.selectbox("Elige un género",
                                  ["Acción", "Fantasía", "Ciencia Ficción", "Drama", "Comedia", "Terror"])

        if st.button("Generar historia"):
            with st.spinner('Generando historia...'):
                if nombre_protagonista and genero:
                    if st.session_state.imagen:
                        files = {'image_file': st.session_state.imagen}
                        description_response = requests.post(f"{API_URL}/describe-image/", files=files)

                        if description_response.status_code == 200:
                            description = description_response.json().get("description", "")

                            image_response = requests.post(f"{API_URL}/generate-image/", json={
                                'genre': genero,
                                'description': description
                            })

                            if image_response.status_code == 200:
                                st.session_state.image_response = image_response.content

                                tale_response = requests.post(f"{API_URL}/generate-tale/", json={
                                    'genre': genero,
                                    'name': nombre_protagonista,
                                    'description': description
                                })

                                if tale_response.status_code == 200:
                                    st.session_state.tale = tale_response.json().get("tale", [])
                                    st.session_state.historia_generada = True
                                    st.success(f"Cuento generado con éxito.")

                                    with st.expander("Ver imagen y cuento generado"):
                                        image_stream = io.BytesIO(st.session_state.image_response)
                                        st.image(image_stream, caption="Imagen del protagonista",
                                                 use_container_width=False, width=200)

                                        st.write("\n\n".join(st.session_state.tale))

                                        narrate_response = requests.post(f"{API_URL}/narrate-tale/",
                                                                         json={"tale": "\n\n".join(st.session_state.tale)})

                                        if narrate_response.status_code == 200:
                                            audio_data = narrate_response.content

                                            if audio_data:
                                                st.audio(audio_data, format='audio/mp3', autoplay=False)
                                            else:
                                                st.warning("No se pudo generar la narración de la historia.")
                                        else:
                                            st.warning("Hubo un error al solicitar la narración.")
                                else:
                                    st.warning("Error de generación.")
                            else:
                                st.warning("No se ha generado la imagen.")
                        else:
                            st.warning("No se ha subido ninguna imagen.")
                    else:
                        st.warning("Completa todos los campos antes.")

    if st.session_state.historia_generada:
        if st.button("Generar PDF"):
            with st.spinner('Generando PDF...'):
                story = "\n\n".join(st.session_state.tale)
                image_bytes = st.session_state.image_response

                image_base64 = base64.b64encode(image_bytes).decode("utf-8")

                pdf_response = requests.post(f"{API_URL}/generate-pdf/",
                                             json={"story": story, "image_bytes": image_base64})

                if pdf_response.status_code == 200:
                    st.success("PDF generado con éxito.")
                    st.download_button(
                        label="Descargar PDF",
                        data=pdf_response.content,
                        file_name="cuento_generado.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.warning("No se pudo generar el PDF.")

if __name__ == "__main__":
    main()