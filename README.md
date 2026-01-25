# Chat LLM con Streamlit

Este proyecto es una aplicación de chat basada en **Streamlit** que permite interactuar con un modelo de lenguaje grande (LLM) alojado en un servidor compatible con la API de OpenAI, como **LMStudio**. La aplicación permite enviar mensajes al modelo y recibir respuestas generadas automáticamente.

## Características
- Interfaz de usuario sencilla y minimalista.
- Configuración dinámica de la URL de la API y el nombre del modelo desde la barra lateral.
- Ajuste del número máximo de tokens para controlar la longitud de las respuestas.
- Respuestas en tiempo real del modelo.

## Requisitos previos
- Python 3.7 o superior.
- Un servidor LLM compatible con la API de OpenAI (por ejemplo, LMStudio).

## Instalación
1. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd llm-py
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # En Windows
   source .venv/bin/activate  # En macOS/Linux
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Asegúrate de que el servidor LLM esté en ejecución y accesible desde la URL configurada.

## Uso
1. Ejecuta la aplicación Streamlit:
   ```bash
   streamlit run app.py
   ```

2. Abre tu navegador en la URL proporcionada por Streamlit (por defecto, `http://localhost:8501`).

3. Configura la URL de la API y el nombre del modelo en la barra lateral si es necesario.

4. Escribe un mensaje en el cuadro de texto y presiona el botón **Enviar** para recibir una respuesta del modelo.

## Configuración
La configuración de la aplicación se guarda en un archivo `config.json`. Este archivo contiene los siguientes valores predeterminados:

```json
{
    "api_url": "http://192.168.1.11:1234/v1/completions",
    "model_name": "liquid/lfm2-1.2b"
}
```

Puedes modificar estos valores directamente en el archivo o desde la barra lateral de la aplicación.

## Personalización
- **Ajustar el número máximo de tokens**: Puedes usar el control deslizante en la barra lateral para ajustar el valor de `max_tokens`, lo que determina la longitud máxima de las respuestas generadas por el modelo.
- **Cambiar la URL de la API y el modelo**: Usa los campos de texto en la barra lateral para actualizar estos valores.

## Dependencias
- `streamlit`
- `requests`

## Contribuciones
Si deseas contribuir a este proyecto, por favor realiza un fork del repositorio, realiza tus cambios y envía un pull request.

## Licencia
Este proyecto está bajo la licencia MIT. Puedes consultar más detalles en el archivo `LICENSE`.