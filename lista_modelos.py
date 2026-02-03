import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Probamos con v1beta que suele dar la lista completa de lo que puedes usar
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

try:
    response = requests.get(url)
    if response.status_code == 200:
        modelos = response.json()
        print("\n--- 📜 MODELOS DISPONIBLES PARA TU CUENTA ---")
        for m in modelos['models']:
            # Filtramos solo los que permiten generar contenido
            if 'generateContent' in m['supportedGenerationMethods']:
                print(f"✅ ID: {m['name']} | Versión: {m['version']}")
        print("-------------------------------------------\n")
    else:
        print(f"❌ Error al consultar: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ Error de conexión: {e}")