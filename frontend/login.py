import streamlit as st
import re

st.set_page_config(page_title="Login", layout="wide", initial_sidebar_state="collapsed")

if "usuarios_registrados" not in st.session_state:
    st.session_state.usuarios_registrados = {"admin": "admin"}

if "formulario" not in st.session_state:
    st.session_state.formulario = "login"
st.title("Login/Register")

def formulario_registro():
    username = st.text_input("Nombre de Usuario")
    password = st.text_input("Contraseña", type="password")
    confirm_password = st.text_input("Confirmar Contraseña", type="password")

    username = username.lower()

    if st.button("Crear cuenta"):
        if password == confirm_password:
            mensaje_error = validar_contraseña(password)
            if mensaje_error:
                st.error(mensaje_error)
            else:
                registrar(username, password)
        else:
            st.error("¡Las contraseñas no coinciden!")

def formulario_login():
    username = st.text_input("Nombre de Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        iniciar_sesion(username, password)

def iniciar_sesion(username, password):
    if username in st.session_state.usuarios_registrados and st.session_state.usuarios_registrados[
        username] == password:
        st.success("¡Bienvenido!")
    else:
        st.error("¡Usuario o contraseña incorrectos!")

def registrar(username, password):
    if username not in st.session_state.usuarios_registrados:
        st.session_state.usuarios_registrados[username] = password
        st.success("¡Usuario registrado con éxito!")
        st.session_state.formulario = "login"
    else:
        st.error("¡El nombre de usuario ya existe!")

def validar_contraseña(password):
    if not re.search(r"[A-Z]", password):
        return "La contraseña debe contener al menos una mayúscula."
    if not re.search(r"\d", password):
        return "La contraseña debe contener al menos un número."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "La contraseña debe contener al menos un símbolo especial."
    return None

if st.session_state.formulario == "login":
    formulario_login()
elif st.session_state.formulario == "registro":
    formulario_registro()

if st.button("¿No tienes cuenta? Regístrate aquí"):
    print(st.session_state.formulario)
    if st.session_state.formulario == "login":
        st.session_state.formulario = "registro"
        st.rerun()
    else:
        st.session_state.formulario = "login"
        st.rerun()
