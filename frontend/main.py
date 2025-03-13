from http.client import responses
import requests
import streamlit as st
import io

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="GenerAIdor de cuentos",
    page_icon="🤖",
    layout="wide"
)

def main():
    st.title("👸 GenerAIdor de Cuentos 📖")
    st.subheader("Genera tus propios cuentos con tus dibujos favoritos.")

    col1, col2, col3= st.columns(3, gap="large", border=True)

    with st.container():

        with col1:
            st.markdown("### Sube una imagen para tu cuento")
            imagen = st.file_uploader("Elige una imagen", type=["jpg", "png", "jpeg"])

        with col2:
            st.markdown("### Información del protagonista")
            nombre_protagonista = st.text_input("Nombre del protagonista:")

        with col3:
            st.markdown("### Selecciona el género de la historia")
            genero = st.selectbox("Elige un género", ["Acción", "Fantasía", "Ciencia Ficción", "Drama", "Comedia", "Terror"])

        if st.button("Generar historia"):
            with st.spinner('Generando historia...'):

                if nombre_protagonista and genero:
                    if imagen:
                        image_data = imagen.getvalue()
                        files = {'image_file': image_data}
                        result = requests.post(f"{API_URL}/describe-image/", files=files)
                        if result.status_code == 200:
                            # Solo intentamos convertir la respuesta a JSON si la solicitud fue exitosa
                            response_json = result.json()
                            description_response = response_json.get("description")
                            tokens_used = response_json.get("tokens_used", 0)
                        else:
                            st.warning(f"Error en la solicitud. Código de estado: {result.status_code}")
                            st.write(result.text)  # Ver el contenido completo de la respuesta para depuración

                        if description_response.status_code == 200:
                            response_json = description_response.json()
                            description = response_json.get("description", "")
                            #tokens_used = response_json.get("tokens_used", 0)  # Obtener los tokens usados
                            st.write(f"Tokens utilizados para describir la imagen: {tokens_used}")  # Mostrar tokens

                            image_response = requests.post(f"{API_URL}/generate-image/", json={
                                'genre': genero,
                                'description': description
                            })

                            if image_response.status_code == 200:
                                tale_response = requests.post(f"{API_URL}/generate-tale/", json={
                                    'genre': genero,
                                    'name': nombre_protagonista,
                                    'description': description
                                })

                                if tale_response.status_code == 200:
                                    tale = tale_response.json().get("tale", [])

                                    if image_response and tale:
                                        st.success(f"Cuento generado con éxito.")
                                        with st.container():
                                            image_data = image_response.content
                                            image_stream = io.BytesIO(image_data)
                                            st.image(image_stream, caption="Imagen del protagonista",
                                                     use_container_width=False, width=200)
                                            st.write("\n\n".join(tale))
                                    else:
                                        st.warning("Error de generación.")
                        else:
                            st.warning("Error al describir la imagen.")
                    else:
                        st.warning("No se ha subido ninguna imagen.")
                else:
                    st.warning("Completa todos los campos antes.")


if __name__ == "__main__":
    main()