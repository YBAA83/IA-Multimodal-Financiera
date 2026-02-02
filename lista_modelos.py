import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

print("--- 📋 SOLICITANDO LISTA DE MODELOS DISPONIBLES ---")

try:
    response = requests.get(url)
    if response.status_code == 200:
        modelos = response.json()
        for m in modelos['models']:
            # Solo listamos los que pueden generar contenido
            if 'generateContent' in m['supportedGenerationMethods']:
                print(f"Modelo: {m['name']} | Versión: {m['version']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {e}")