import streamlit as st

st.set_page_config(
    page_title="GenerAIdor de cuentos",
    page_icon="🤖",
    layout="wide"
)
def main():
    st.title("👸 GenerAIdor de Cuentos 📖")
    st.subheader("Genera tus propios cuentos con tus dibujos favoritos.")

    st.markdown("""
        <style>
            .stColumn {
                background-color: #d3d3d3;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="stColumn">', unsafe_allow_html=True)
        st.header("Sube una imagen para tu cuento")
        imagen = st.file_uploader("Elige una imagen", type=["jpg", "png", "jpeg"])
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stColumn">', unsafe_allow_html=True)
        st.header("Información del protagonista")
        nombre_protagonista = st.text_input("Nombre del protagonista:")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stColumn">', unsafe_allow_html=True)
        st.header("Selecciona el género de la historia")
        genero = st.selectbox("Elige un género", ["Acción", "Fantasía", "Ciencia Ficción", "Drama", "Comedia", "Terror"])
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Generar historia"):
        if nombre_protagonista and genero:
            st.success(f"Historia de {genero} con {nombre_protagonista} generada.")

            if imagen:
                st.image(imagen, caption="Imagen del protagonista", use_column_width=True)
            else:
                st.warning("No se ha subido ninguna imagen.")
        else:
            st.warning("Completa todos los campos antes.")

if __name__ == "__main__":
    main()