import os
import requests
import time
from dotenv import load_dotenv
from impresora import generar_pdf

# 1. Configuración de entorno
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Usamos 'gemini-flash-latest' para máxima estabilidad y evitar errores 429
MODELO = "gemini-flash-latest"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent?key={api_key}"

# 2. Datos para el análisis
datos_flujo_caja = """
Historial Mensual Real (Q1 2026):
- Enero: Ingresos 50.000€, Gastos 35.000€
- Febrero: Ingresos 48.000€, Gastos 38.000€
- Marzo: Ingresos 52.000€, Gastos 42.000€
"""

prompt_maestro = f"""
Actúa como un Director Financiero (CFO) y experto en IA. 
Analiza estos datos financieros: {datos_flujo_caja}

TAREA:
1. Proyecta el cierre del próximo trimestre (Q2).
2. Calcula la tendencia del margen operativo.
3. Identifica riesgos si los gastos operativos suben un 10% mensual.
4. Sugiere 3 recomendaciones estratégicas.
"""

def ejecutar_analisis(reintentos=3):
    print(f"--- 🤖 EL MONSTRUO TRABAJANDO CON {MODELO} ---")
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt_maestro}]}]}

    for i in range(reintentos):
        try:
            response = requests.post(URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                texto_analisis = data['candidates'][0]['content']['parts'][0]['text']
                
                # Generar el PDF
                generar_pdf(texto_analisis, "Analisis_Proyectivo_2026.pdf")
                print(f"\n✅ ¡MISIÓN CUMPLIDA! PDF generado con éxito.")
                return 
            
            elif response.status_code == 429:
                espera = 60 # Esperamos el minuto reglamentario
                print(f"⚠️ Cuota llena. Reintento {i+1}/{reintentos} en {espera} segundos...")
                time.sleep(espera)
            else:
                print(f"❌ Error API ({response.status_code}): {response.text}")
                break

        except Exception as e:
            print(f"❌ Error crítico: {e}")
            break

if __name__ == "__main__":
    ejecutar_analisis()