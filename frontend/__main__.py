import requests
import streamlit as st
import io
import base64
import json

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
        background-color: #C5D9E8;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.image("./static/images/logo2.png", width=900)

def main():

    if 'qa_pairs' not in st.session_state:
        st.session_state.qa_pairs = {}
    if "historia_generada" not in st.session_state:
        st.session_state.historia_generada = False
    if "tale" not in st.session_state:
        st.session_state.tale = []
    if "imagen" not in st.session_state:
        st.session_state.imagen = None
    if "image_response" not in st.session_state:
        st.session_state.image_response = None
    if "preguntas_generadas" not in st.session_state:
        st.session_state.preguntas_generadas = None
    if "respuestas_preguntas" not in st.session_state:
        st.session_state.respuestas_preguntas = []

    col1, col2, col3= st.columns(3, gap="large", border=True)

    with st.container():
        with col1:
            st.markdown("### Sube una imagen para tu cuento")
            imagen = st.file_uploader("Elige una imagen", type=["jpg", "png", "jpeg"])
            if imagen:
                st.session_state.imagen = imagen.getvalue()

        with col2:
            st.markdown("### Información del protagonista")
            nombre_protagonista = st.text_input("Nombre del protagonista:")

            with st.expander("⚙️ Opciones avanzadas", expanded=False):
                st.markdown("### Test de personalidad del protagonista")

                if st.button("Generar preguntas"):
                    with st.spinner("Generando preguntas..."):
                        pregunta_response = requests.post(f"{API_URL}/request-questions/")
                        if pregunta_response.status_code == 200:
                            preguntas = pregunta_response.json().get('questions', [])

                            if isinstance(preguntas, str):
                                try:
                                    preguntas = json.loads(preguntas)
                                except:
                                    preguntas = [preguntas] if preguntas else []

                            st.session_state.preguntas_generadas = preguntas
                            st.session_state.respuestas_preguntas = [''] * len(preguntas)
                            st.session_state.respuestas_enviadas = False
                        else:
                            st.warning("Hubo un error al generar las preguntas.")

                if st.session_state.preguntas_generadas and not st.session_state.respuestas_enviadas:
                    st.markdown("## Responde a las siguientes preguntas")
                    st.markdown("Las preguntas que dejes en blanco no se tendrán en cuenta\n")
                    for i, pregunta in enumerate(st.session_state.preguntas_generadas):

                        def update_respuesta(i=i):
                            st.session_state.respuestas_preguntas[i] = st.session_state[f"respuesta_{i}"]

                        st.text_input(
                            f"Pregunta {i + 1}: {pregunta}",
                            value=st.session_state.respuestas_preguntas[i],
                            key=f"respuesta_{i}",
                            on_change=update_respuesta
                        )

                    if st.button("Enviar respuestas"):
                        respuestas_validas = {
                            st.session_state.preguntas_generadas[i]: respuesta
                            for i, respuesta in enumerate(st.session_state.respuestas_preguntas)
                            if respuesta.strip()
                        }
                        st.session_state.qa_pairs = respuestas_validas
                        st.session_state.respuestas_enviadas = True
                        st.success("Respuestas guardadas correctamente!")
                    print(st.session_state.respuestas_preguntas)

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
                                    'description': description,
                                    'qa_pairs' : st.session_state.qa_pairs
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