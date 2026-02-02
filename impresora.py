import os
from fpdf import FPDF
from datetime import datetime

class ReportePDF(FPDF):
    def header(self):
        # Logo Adaptativo
        logo = "logo.png" if os.path.exists("logo.png") else "logo.jpg"
        if os.path.exists(logo):
            self.image(logo, 10, 8, 25)
            self.set_x(40)
        else:
            self.set_x(10)

        # Identidad de Marca
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'IA FINANCIERA - JAIRO ENG.', 0, 1, 'L')
        
        self.set_x(40 if os.path.exists(logo) else 10)
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, 'Analisis Algoritmico de Flujo de Caja y Tendencias', 0, 1, 'L')
        
        self.ln(10)
        self.set_draw_color(0, 51, 102)
        self.line(10, 32, 200, 32) # Linea divisoria
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150)
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cell(0, 10, f'Generado por El Monstruo v2.0 | {fecha} | Pagina {self.page_no()}', 0, 0, 'C')

def generar_pdf(texto_auditoria, nombre_archivo="Reporte.pdf", ruta_grafico=None):
    ruta_final = os.path.join("output", nombre_archivo)
    pdf = ReportePDF()
    pdf.add_page()
    
    # Insertar Gráfico si existe
    if ruta_grafico and os.path.exists(ruta_grafico):
        pdf.image(ruta_grafico, x=20, y=45, w=170)
        pdf.ln(95) # Ajuste de espacio para el texto

    # Formateo de texto
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(40, 40, 40)
    
    # Limpieza y codificación (Soporte para acentos y ñ)
    texto_limpio = texto_auditoria.replace("**", "").replace("##", "").replace("###", "").replace("* ", "• ")
    texto_final = texto_limpio.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.multi_cell(0, 7, txt=texto_final, align='L')
    pdf.output(ruta_final)