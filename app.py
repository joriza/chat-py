import streamlit as st
from consume_llm_api import query_llm
import json
import requests

# Cargar configuración desde un archivo JSON con valores predeterminados
def load_config():
    # Actualizar la URL predeterminada en la configuración para seguir la convención de OpenAI
    default_config = {
        "api_url": "http://127.0.0.1:1234/v1/completions",
        "model_name": "liquid/lfm2-1.2b"
    }
    try:
        with open("config.json", "r") as config_file:
            user_config = json.load(config_file)
            # Combinar configuración predeterminada con la del usuario
            return {**default_config, **user_config}
    except FileNotFoundError:
        # Si no existe el archivo, usar la configuración predeterminada
        return default_config

# Guardar configuración en un archivo JSON
def save_config(api_url, model_name):
    config = {
        "api_url": api_url,
        "model_name": model_name
    }
    with open("config.json", "w") as config_file:
        json.dump(config, config_file)

# Cargar configuración inicial
config = load_config()

# Título de la aplicación
st.title("Chat LLM - Configuración")

# Formulario para configurar la API
st.sidebar.header("Configuración de la API")
api_url = st.sidebar.text_input("API URL", value=config.get("api_url", ""))
model_name = st.sidebar.text_input("Model Name", value=config.get("model_name", ""))

# Ampliar el rango del control deslizante para max_tokens
st.sidebar.header("Configuración de Respuesta")
max_tokens = st.sidebar.slider("Máximo de tokens", min_value=50, max_value=2000, value=300, step=50)

if st.sidebar.button("Guardar configuración"):
    save_config(api_url, model_name)
    st.sidebar.success("Configuración guardada correctamente.")

# Entrada del usuario
st.header("Chat con el modelo LLM")
user_input = st.text_area(
    "Escribe tu mensaje:", 
    height=50, 
    max_chars=500, 
    placeholder="Escribe aquí tu mensaje...",
    on_change=lambda: st.session_state.update(enter_pressed=True),
    key="user_input"
)

# Actualizar la función query_llm para aceptar max_tokens como parámetro
def query_llm_with_tokens(prompt, max_tokens):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": 0.7
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al consumir la API: {e}")
        return None

# Botón para enviar el mensaje o usar Ctrl + Enter
if st.button("Enviar") or st.session_state.get("enter_pressed", False):
    if user_input:
        if not api_url or not model_name:
            st.error("Por favor, configure la API URL y el Model Name en la barra lateral.")
        else:
            # Actualizar la configuración en tiempo real
            save_config(api_url, model_name)
            # Llamar a la función query_llm con la configuración actualizada
            response = query_llm_with_tokens(user_input, max_tokens)
            if response:
                # Mostrar la respuesta del modelo
                st.write("**Respuesta del modelo:**")
                st.write(response.get("choices", [{}])[0].get("text", ""))
            else:
                st.error("Hubo un error al comunicarse con el modelo.")
    else:
        st.warning("Por favor, escribe un mensaje antes de enviar.")