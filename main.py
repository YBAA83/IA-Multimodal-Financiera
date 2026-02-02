import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from impresora import generar_pdf

# 1. CONFIGURACIÓN E IDENTIDAD
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model_name = "models/gemini-flash-latest"
url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"

print("\n--- 🤖 INICIANDO EL MONSTRUO (IA FINANCIERA) ---")

# 2. CARGA Y PROCESAMIENTO DE DATOS
try:
    df = pd.read_csv('movimientos.csv')
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    
    # KPIs Rápidos
    ingresos = df[df['Monto'] > 0]['Monto'].sum()
    gastos = abs(df[df['Monto'] < 0]['Monto'].sum())
    balance = ingresos - gastos
except Exception as e:
    print(f"❌ Error en datos: {e}")
    exit()

# 3. GENERACIÓN DE GRÁFICOS
print("📊 Creando visualizaciones de alto nivel...")

# A. Gráfico de Tendencia (Línea de Vida)
plt.figure(figsize=(10, 5))
tendencia = df.groupby('Fecha')['Monto'].sum().cumsum()
plt.plot(tendencia.index, tendencia.values, marker='o', color='#3498db', linewidth=3)
plt.fill_between(tendencia.index, tendencia.values, color='#3498db', alpha=0.1)
plt.title('Evolucion del Flujo de Caja Neto Acumulado')
plt.grid(True, alpha=0.3)
ruta_linea = os.path.join("output", "grafico_tendencia.png")
plt.savefig(ruta_linea)
plt.close()

# B. Gráfico de Donut (Distribución de Gastos)
gastos_df = df[df['Monto'] < 0].copy()
gastos_df['Monto'] = abs(gastos_df['Monto'])
distribucion = gastos_df.groupby('Categoria')['Monto'].sum()

plt.figure(figsize=(6, 6))
plt.pie(distribucion, labels=distribucion.index, autopct='%1.1f%%', startangle=90, 
        colors=['#ff9f43', '#ee5253', '#5f27cd', '#54a0ff'], wedgeprops=dict(width=0.4))
plt.title('Desglose de Gastos por Categoria')
ruta_donut = os.path.join("output", "grafico_donut.png")
plt.savefig(ruta_donut)
plt.close()

# 4. CONSULTA A LA IA (Contexto Multimodal)
print("🧠 El Monstruo esta razonando sobre el futuro...")
tabla_md = df.to_markdown()
prompt = f"""
Actua como un Ingeniero Financiero de elite. Analiza esta situacion:
{tabla_md}

Resumen: Ingresos {ingresos}€ | Gastos {gastos}€ | Balance {balance}€

Tareas:
1. Basado en la tendencia (Burn Rate), ¿cuando se agotara la liquidez?
2. Identifica riesgos criticos (Pagos en efectivo o gastos desproporcionados).
3. Dame 3 recomendaciones estrategicas para el proximo trimestre.
"""

payload = {"contents": [{"parts": [{"text": prompt}]}]}
headers = {'Content-Type': 'application/json'}

try:
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        texto_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
        
        # 5. MAQUETACIÓN DEL INFORME FINAL
        # Elegimos el gráfico de Tendencia para el informe principal
        generar_pdf(texto_ia, "Informe_Maestro_Financiero.pdf", ruta_linea)
        print(f"\n✅ INFORME GENERADO: Revisa la carpeta 'output'")
    else:
        print(f"❌ Error API: {response.text}")
except Exception as e:
    print(f"❌ Error Critico: {e}")