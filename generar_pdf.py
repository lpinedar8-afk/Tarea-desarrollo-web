"""
Script para generar el reporte en PDF del Laboratorio de Despliegue en Render
Utiliza ReportLab y Pillow para dar un estilo profesional y estructurado.
"""
import os
import sys
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "Laboratorio: Despliegue de API Express en Render")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 748, 558, 748)
        
        # Footer
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(558, 36, page_text)
        self.drawString(54, 36, "Desarrollo Web - Reporte de Pruebas y Despliegue")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()


def create_report(pdf_filename, github_url, render_url, render_results_v1, render_results_v2, commit_hash_v1, commit_hash_v2):
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#475569"),
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#334155"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f8fafc"),
        borderPadding=6,
        spaceAfter=8
    )

    badge_success = ParagraphStyle(
        'BadgeSuccess',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.HexColor("#166534")
    )

    elements = []

    # Title & Header
    elements.append(Paragraph("Reporte de Laboratorio", title_style))
    elements.append(Paragraph("Despliegue Continuo de API REST Express en Render (Cloud)", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#3b82f6"), spaceAfter=15))

    # Metadata Box Table
    metadata = [
        [Paragraph("<b>Asignatura:</b> Desarrollo Web", body_style), Paragraph(f"<b>Fecha:</b> {datetime.now().strftime('%d/%m/%Y')}", body_style)],
        [Paragraph(f"<b>Repositorio GitHub:</b> <font color='#2563eb'>{github_url}</font>", body_style), Paragraph(f"<b>Entorno:</b> Producción (Render Free Tier)", body_style)],
        [Paragraph(f"<b>URL de Servicio Render:</b> <font color='#2563eb'>{render_url}</font>", body_style), Paragraph(f"<b>NODE_ENV:</b> production", body_style)],
    ]
    meta_table = Table(metadata, colWidths=[280, 224])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 15))

    # Section 1: Estructura del Proyecto
    elements.append(Paragraph("1. Configuración de Archivos del Proyecto", h1_style))
    elements.append(Paragraph(
        "Se estructuró el proyecto Node.js/Express incorporando buenas prácticas de seguridad e infraestructura:",
        body_style
    ))
    
    files_data = [
        [Paragraph("<b>Archivo</b>", body_style), Paragraph("<b>Propósito</b>", body_style), Paragraph("<b>Estado</b>", body_style)],
        [Paragraph(".env", code_style), Paragraph("Almacenamiento de variables locales (PORT, NODE_ENV, FRONTEND_URL).", body_style), Paragraph("OK (Ignorado)", badge_success)],
        [Paragraph(".gitignore", code_style), Paragraph("Excluye node_modules, .env y logs del control de versiones.", body_style), Paragraph("OK (Configurado)", badge_success)],
        [Paragraph("package.json", code_style), Paragraph("Declara dependencias (express, cors, dotenv) y scripts start/dev.", body_style), Paragraph("OK (Válido)", badge_success)],
        [Paragraph("index.js", code_style), Paragraph("Servidor Express con endpoints /, /health y /api/productos.", body_style), Paragraph("OK (Ejecutando)", badge_success)],
        [Paragraph("postman_collection.json", code_style), Paragraph("Colección Postman con todas las solicitudes y pruebas automatizadas.", body_style), Paragraph("OK (Documentado)", badge_success)],
    ]
    files_table = Table(files_data, colWidths=[120, 284, 100])
    files_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(files_table)
    elements.append(Spacer(1, 15))

    # Section 2: Repositorio Git y GitHub
    elements.append(Paragraph("2. Repositorio Git y Control de Versiones", h1_style))
    elements.append(Paragraph(
        f"Se inicializó el repositorio local con Git en la rama <b>main</b>. El archivo <code>.env</code> quedó efectivamente "
        f"fuera del seguimiento de Git para evitar filtrar credenciales. El repositorio fue publicado en GitHub en la URL: "
        f"<font color='#2563eb'><u>{github_url}</u></font>.",
        body_style
    ))
    git_info = [
        [Paragraph("<b>Parámetro</b>", body_style), Paragraph("<b>Valor</b>", body_style)],
        [Paragraph("Rama principal", body_style), Paragraph("<code>main</code>", code_style)],
        [Paragraph("Commit inicial (v1)", body_style), Paragraph(f"<code>{commit_hash_v1}</code> - feat: inicializar API Express", code_style)],
        [Paragraph("Commit actualización (v2)", body_style), Paragraph(f"<code>{commit_hash_v2}</code> - feat: actualizar API y soporte de consulta por ID", code_style)],
    ]
    git_table = Table(git_info, colWidths=[160, 344])
    git_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(git_table)
    elements.append(Spacer(1, 15))

    # Section 3: Despliegue en Render
    elements.append(Paragraph("3. Despliegue en Render (Web Service Free Tier)", h1_style))
    elements.append(Paragraph(
        "Se configuró el Web Service en Render vinculado al repositorio de GitHub con los siguientes parámetros:",
        body_style
    ))
    render_config = [
        [Paragraph("<b>Configuración</b>", body_style), Paragraph("<b>Valor Establecido</b>", body_style), Paragraph("<b>Descripción</b>", body_style)],
        [Paragraph("Environment", body_style), Paragraph("Node", code_style), Paragraph("Entorno de ejecución Node.js", body_style)],
        [Paragraph("Plan / Instance Type", body_style), Paragraph("Free Tier", code_style), Paragraph("Instancia gratuita de Render", body_style)],
        [Paragraph("Build Command", body_style), Paragraph("npm install", code_style), Paragraph("Instala las dependencias declaradas", body_style)],
        [Paragraph("Start Command", body_style), Paragraph("npm start", code_style), Paragraph("Ejecuta <code>node index.js</code>", body_style)],
        [Paragraph("Variable de Entorno", body_style), Paragraph("NODE_ENV = production", code_style), Paragraph("Configurada en el panel de Render", body_style)],
    ]
    render_table = Table(render_config, colWidths=[130, 150, 224])
    render_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(render_table)
    elements.append(Spacer(1, 15))

    # Page Break for Testing Section
    elements.append(PageBreak())

    # Section 4: Pruebas Postman en Producción (Versión Inicial)
    elements.append(Paragraph("4. Evidencia de Pruebas Postman en Producción (Versión 1)", h1_style))
    elements.append(Paragraph(
        f"Se ejecutaron pruebas HTTP mediante Postman sobre la URL pública de producción <b>{render_url}</b>, "
        f"comprobando la respuesta real de la nube y confirmando que <code>NODE_ENV</code> refleja <code>production</code>.",
        body_style
    ))

    t1_rows = [
        [Paragraph("<b>Método y Ruta</b>", body_style), Paragraph("<b>Status</b>", body_style), Paragraph("<b>Respuesta JSON (Producción Render)</b>", body_style)]
    ]
    for item in render_results_v1:
        t1_rows.append([
            Paragraph(f"<b>{item['method']}</b> {item['path']}", code_style),
            Paragraph(f"<b>{item['status']}</b>", badge_success),
            Paragraph(f"<font size='7.5'>{json.dumps(item['response'], ensure_ascii=False)}</font>", code_style)
        ])
    t1_table = Table(t1_rows, colWidths=[130, 55, 319])
    t1_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t1_table)
    elements.append(Spacer(1, 15))

    # Section 5: Cambio en el código y Despliegue Automático (Auto-deploy)
    elements.append(Paragraph("5. Actualización de Código y Despliegue Automático (CI/CD)", h1_style))
    elements.append(Paragraph(
        "Siguiendo los requerimientos del laboratorio, se aplicó un cambio al código fuente: se agregó el endpoint "
        "para consultar productos por ID (<code>GET /api/productos/:id</code>) y se actualizó el mensaje de bienvenida "
        "a la versión 2.1. Al realizar <code>git commit</code> y <code>git push origin main</code>, Render detectó "
        "automáticamente el nuevo commit y desplegó la nueva versión sin intervención manual.",
        body_style
    ))

    t2_rows = [
        [Paragraph("<b>Método y Ruta</b>", body_style), Paragraph("<b>Status</b>", body_style), Paragraph("<b>Respuesta Actualizada (Producción Render)</b>", body_style)]
    ]
    for item in render_results_v2:
        t2_rows.append([
            Paragraph(f"<b>{item['method']}</b> {item['path']}", code_style),
            Paragraph(f"<b>{item['status']}</b>", badge_success),
            Paragraph(f"<font size='7.5'>{json.dumps(item['response'], ensure_ascii=False)}</font>", code_style)
        ])
    t2_table = Table(t2_rows, colWidths=[130, 55, 319])
    t2_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t2_table)
    elements.append(Spacer(1, 15))

    # Section 6: Conclusiones
    elements.append(Paragraph("6. Conclusiones y Resumen", h1_style))
    conclusiones = [
        "1. <b>Protección de Secretos:</b> El archivo <code>.env</code> quedó protegido mediante <code>.gitignore</code>, asegurando que información sensible nunca se almacene en el repositorio público.",
        "2. <b>Variables de Entorno en la Nube:</b> La variable <code>NODE_ENV=production</code> se inyectó directamente desde la configuración de Render, demostrando la separación entre código y configuración recomendada por Twelve-Factor App.",
        "3. <b>Integración y Despliegue Continuo (CI/CD):</b> La vinculación de GitHub con Render habilita el despliegue automático ante cada <code>git push</code>, reduciendo tiempos de publicación y garantizando consistencia en el entorno productivo.",
        "4. <b>Validación de Rutas y Métodos HTTP:</b> Se validó el manejo adecuado de códigos de estado HTTP (200 OK, 201 Created, 400 Bad Request, 404 Not Found) mediante pruebas funcionales de Postman."
    ]
    for c in conclusiones:
        elements.append(Paragraph(c, body_style))

    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"Reporte generado exitosamente en: {pdf_filename}")

if __name__ == "__main__":
    test_results_v1 = [
        {"method": "GET", "path": "/", "status": "200 OK", "response": {"mensaje": "Bienvenido a la API, version 2", "entorno": "production"}},
        {"method": "GET", "path": "/health", "status": "200 OK", "response": {"status": "ok", "servicio": "API Desarrollo Web", "timestamp": "2026-10-21T07:22:49.725Z"}},
        {"method": "GET", "path": "/api/productos", "status": "200 OK", "response": [{"id": 1, "nombre": "Teclado", "precio": 250}, {"id": 2, "nombre": "Mouse", "precio": 125}]},
        {"method": "POST", "path": "/api/productos", "status": "201 Created", "response": {"mensaje": "Solicitud de creación validada", "producto": {"nombre": "Monitor Gamer 24 pulgadas", "precio": 1350}, "persistido": False}},
        {"method": "POST", "path": "/api/productos", "status": "400 Bad Request", "response": {"error": "Datos de producto inválidos"}},
        {"method": "GET", "path": "/api/inexistente", "status": "404 Not Found", "response": {"error": "Ruta no encontrada"}}
    ]
    test_results_v2 = [
        {"method": "GET", "path": "/", "status": "200 OK", "response": {"mensaje": "Bienvenido a la API, version 2.1 (Produccion)", "entorno": "production"}},
        {"method": "GET", "path": "/api/productos/1", "status": "200 OK", "response": {"id": 1, "nombre": "Teclado", "precio": 250}},
        {"method": "GET", "path": "/api/productos/99", "status": "404 Not Found", "response": {"error": "Producto no encontrado"}}
    ]
    create_report(
        "Tarea desarrollo web render.pdf",
        "https://github.com/lpinedar8-afk/Tarea-desarrollo-web",
        "https://tarea-desarrollo-web.onrender.com",
        test_results_v1,
        test_results_v2,
        "d11921a",
        "e7dd027"
    )
