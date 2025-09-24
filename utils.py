# ==================== utils.py ====================

import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def exportar_pdf(nombre_archivo, dataframe):
    """Exporta un DataFrame de pandas a un PDF en formato tabla."""
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter)
    elementos = []

    estilos = getSampleStyleSheet()
    titulo = Paragraph("Reporte Académico - MiniSIGA", estilos['Heading1'])
    elementos.append(titulo)

    if dataframe.empty:
        elementos.append(Paragraph("No hay datos para mostrar.", estilos['Normal']))
    else:
        # Convertir DataFrame a lista de listas
        data = [dataframe.columns.tolist()] + dataframe.values.tolist()

        tabla = Table(data)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elementos.append(tabla)

    doc.build(elementos)
    print(f"PDF exportado como {nombre_archivo}")


def crear_archivo_csv_ejemplo():
    """Crea un archivo CSV de ejemplo con un estudiante de prueba."""
    datos_ejemplo = [
        ['documento', 'nombre', 'apellidos', 'correo', 'fecha_nac'],
        ['98765432', 'Andrea', 'Castillo Vega',
         'andrea.castillo@email.com', '2001-07-20'],
    ]
    with open('estudiantes_ejemplo.csv', 'w', newline='', encoding='utf-8') as archivo:
        writer = csv.writer(archivo)
        writer.writerows(datos_ejemplo)
    print("Archivo 'estudiantes_ejemplo.csv' creado exitosamente.")


def verificar_dependencias():
    """Verifica que las librerías externas estén instaladas."""
    dependencias = [
        'tkinter',
        'csv',
        'json',
        'datetime',
        're',
        'matplotlib',
        'numpy'
    ]
    faltantes = []
    for dep in dependencias:
        try:
            __import__(dep)
        except ImportError:
            faltantes.append(dep)

    if faltantes:
        print("Error: Faltan las siguientes dependencias:")
        for dep in faltantes:
            print(f"  - {dep}")
        print("\nInstala las dependencias faltantes con:")
        print("pip install matplotlib numpy")
        return False

    return True
