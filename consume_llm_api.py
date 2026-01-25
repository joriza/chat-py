import requests

# URL de la API y modelo
api_url = "http://192.168.1.11:1234/v1/completions"
model_name = "liquid/lfm2-1.2b"

# Función para consumir la API
def query_llm(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "prompt": prompt,
        "max_tokens": 100,
        "temperature": 0.7
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al consumir la API: {e}")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    prompt = "¿Cuál es la capital de Francia?"
    result = query_llm(prompt)
    if result:
        print("Respuesta del modelo:")
        print(result.get("choices", [{}])[0].get("text", ""))