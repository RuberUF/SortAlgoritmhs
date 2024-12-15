from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io
from django.http import FileResponse, JsonResponse
import json

def generar_pdf(datos_ordenados_por_algoritmo):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ])
    
    data_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    for idx, (algoritmo, data) in enumerate(datos_ordenados_por_algoritmo.items()):
        datos_ordenados = data['datos']
        tiempo = data['tiempo']

        title = Table([[f'Algoritmo de Ordenamiento: {algoritmo}']], style=title_style)
        elements.append(title)

        subtitle = Table([[f'Tiempo de Ordenamiento: {tiempo} ms']], style=title_style)
        elements.append(subtitle)

        table_data = [['#', 'Dato Ordenado']]
        for i, dato in enumerate(datos_ordenados, start=1):
            table_data.append([i, dato])
        
        table = Table(table_data)
        table.setStyle(data_style)
        elements.append(table)

        img_path = 'MyApp/static/MyApp/images/anime_girl_render_14_by_nunnallyrey.png'
        img = Image(img_path)
        img.drawHeight = 1.5 * inch
        img.drawWidth = 1.5 * inch
        img.hAlign = 'CENTER'
        elements.append(img)

        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    buffer.seek(0)
    return buffer

def descargar_pdf(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        datos_ordenados_por_algoritmo = data.get('datos_ordenados_por_algoritmo')

        buffer = generar_pdf(datos_ordenados_por_algoritmo)
        return FileResponse(buffer, as_attachment=True, filename='datos_ordenados.pdf')
    return JsonResponse({'error': 'Método de solicitud no válido'}, status=400)
