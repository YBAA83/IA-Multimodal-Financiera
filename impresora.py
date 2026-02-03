import os
from fpdf import FPDF
from datetime import datetime

class ReportePDF(FPDF):
    def header(self):
        # --- ZONA DEL LOGO ---
        # Busca el archivo 'logo.png' en la misma carpeta
        if os.path.exists("logo.png"):
            # image(archivo, x, y, ancho)
            # x=10mm (margen izq), y=8mm (margen sup), ancho=30mm
            self.image("logo.png", 10, 8, 30)
            # Movemos el título a la derecha para que no pise el logo
            self.set_x(45)

        # --- ZONA DEL TÍTULO ---
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(0, 51, 102)
        # Cambiamos la alineación a izquierda 'L' si hay logo
        align_mode = 'L' if os.path.exists("logo.png") else 'C'
        self.cell(0, 10, 'MONSTRUO IA - PROYECCIONES FINANCIERAS', 0, 1, align_mode)
        
        # Un poco más de espacio antes de empezar el texto
        self.ln(15)

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
    # Márgenes estándar (izq, arriba, der)
    pdf.set_margins(20, 20, 20)
    pdf.set_font("Helvetica", size=11)
    
    # Limpieza y codificación
    texto_limpio = texto_ia.replace("**", "").replace("##", "").replace("###", "").replace("- ", "* ")
    texto_final = texto_limpio.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.multi_cell(0, 7, txt=texto_final, align='L')
    pdf.output(ruta_final)