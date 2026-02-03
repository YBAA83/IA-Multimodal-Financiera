import os
from fpdf import FPDF
from datetime import datetime

class ReportePDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'MONSTRUO IA - PROYECCIONES FINANCIERAS', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cell(0, 10, f'Generado por IA (YBAA83) el {fecha} | Pagina {self.page_no()}', 0, 0, 'C')

def generar_pdf(texto_ia, nombre_archivo):
    if not os.path.exists("output"):
        os.makedirs("output")
        
    ruta_final = os.path.join("output", nombre_archivo)
    pdf = ReportePDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    
    # Limpieza de Markdown para evitar caracteres extraños en el PDF
    texto_limpio = texto_ia.replace("**", "").replace("##", "").replace("###", "").replace("- ", "* ")
    
    # Codificación para evitar errores con tildes y eñes
    texto_final = texto_limpio.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.multi_cell(0, 7, txt=texto_final, align='L')
    pdf.output(ruta_final)