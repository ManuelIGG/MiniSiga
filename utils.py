# ==================== utils.py ====================

import csv
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Backend sin interfaz gráfica para generar imágenes


def exportar_pdf_completo(nombre_archivo, controlador):
    """
    Exporta un reporte completo en PDF con:
    - Reporte general de estudiantes
    - Top 3 estudiantes por cada curso
    - Gráficas estadísticas de cada curso
    """
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter,
                           topMargin=0.5*inch, bottomMargin=0.5*inch,
                           leftMargin=0.5*inch, rightMargin=0.5*inch)
    elementos = []
    estilos = getSampleStyleSheet()
    
    # Estilos personalizados
    estilo_titulo = ParagraphStyle(
        'CustomTitle',
        parent=estilos['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    estilo_subtitulo = ParagraphStyle(
        'CustomSubtitle',
        parent=estilos['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    estilo_info = ParagraphStyle(
        'InfoStyle',
        parent=estilos['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=TA_RIGHT
    )
    
    # ==================== PORTADA ====================
    elementos.append(Spacer(1, 1*inch))
    titulo = Paragraph("MiniSIGA - Reporte Académico Completo", estilo_titulo)
    elementos.append(titulo)
    elementos.append(Spacer(1, 0.3*inch))
    
    # Información de generación
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    info_fecha = Paragraph(f"Generado el: {fecha_actual}", estilo_info)
    elementos.append(info_fecha)
    elementos.append(Spacer(1, 0.5*inch))
    
    # Estadísticas generales
    modelo = controlador.modelo
    stats_data = [
        ['ESTADÍSTICAS GENERALES', ''],
        ['Total de Estudiantes:', str(len(modelo.estudiantes))],
        ['Total de Cursos:', str(len(modelo.cursos))],
        ['Total de Matrículas:', str(len(modelo.matriculas))],
    ]
    
    if modelo.matriculas:
        notas = [nota for _, _, nota in modelo.matriculas]
        promedio_general = sum(notas) / len(notas)
        aprobados_total = sum(1 for nota in notas if nota >= 3.0)
        tasa_aprobacion = (aprobados_total / len(notas)) * 100
        
        stats_data.extend([
            ['Promedio General:', f'{promedio_general:.2f}'],
            ['Tasa de Aprobación:', f'{tasa_aprobacion:.1f}%']
        ])
    
    tabla_stats = Table(stats_data, colWidths=[3*inch, 2*inch])
    tabla_stats.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
    ]))
    elementos.append(tabla_stats)
    elementos.append(PageBreak())
    
    # ==================== REPORTE GENERAL DE ESTUDIANTES ====================
    subtitulo = Paragraph("1. Reporte General de Estudiantes", estilo_subtitulo)
    elementos.append(subtitulo)
    elementos.append(Spacer(1, 0.2*inch))
    
    df = controlador.generar_reporte_estudiantes()
    
    if not df.empty:
        # Preparar datos para la tabla
        data = [df.columns.tolist()] + df.values.tolist()
        
        # Ajustar ancho de columnas
        col_widths = [1*inch, 1.5*inch, 1.2*inch, 0.8*inch, 0.6*inch]
        
        tabla = Table(data, colWidths=col_widths, repeatRows=1)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ]))
        elementos.append(tabla)
    else:
        elementos.append(Paragraph("No hay datos disponibles.", estilos['Normal']))
    
    elementos.append(PageBreak())
    
    # ==================== TOP 3 ESTUDIANTES POR CURSO ====================
    subtitulo = Paragraph("2. Top 3 Estudiantes por Curso", estilo_subtitulo)
    elementos.append(subtitulo)
    elementos.append(Spacer(1, 0.2*inch))
    
    for codigo_curso, curso in sorted(modelo.cursos.items()):
        # Título del curso
        titulo_curso = Paragraph(
            f"<b>Curso:</b> {codigo_curso} - {curso.nombre}",
            estilos['Heading3']
        )
        elementos.append(titulo_curso)
        elementos.append(Spacer(1, 0.1*inch))
        
        # Obtener top 3 estudiantes
        top_estudiantes = modelo.obtener_top_estudiantes(codigo_curso, 3)
        
        if top_estudiantes:
            # Crear tabla con el top 3
            data_top = [['Posición', 'Documento', 'Nombre Completo', 'Correo', 'Nota', 'Estado']]
            
            for i, (estudiante, nota) in enumerate(top_estudiantes, 1):
                estado = 'APROBADO' if nota >= 3.0 else 'REPROBADO'
                color_estado = 'green' if nota >= 3.0 else 'red'
                
                data_top.append([
                    str(i),
                    estudiante.documento,
                    f"{estudiante.nombre} {estudiante.apellidos}",
                    estudiante.correo,
                    f"{nota:.2f}",
                    estado
                ])
            
            tabla_top = Table(data_top, colWidths=[0.6*inch, 0.9*inch, 2*inch, 1.8*inch, 0.6*inch, 0.9*inch])
            
            # Estilo de la tabla
            estilo_tabla = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fff3cd')]),
            ]
            
            # Colorear el estado
            for i in range(1, len(data_top)):
                if data_top[i][5] == 'APROBADO':
                    estilo_tabla.append(('TEXTCOLOR', (5, i), (5, i), colors.green))
                else:
                    estilo_tabla.append(('TEXTCOLOR', (5, i), (5, i), colors.red))
                
                # Resaltar al primer lugar
                if i == 1:
                    estilo_tabla.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#ffd700')))
            
            tabla_top.setStyle(TableStyle(estilo_tabla))
            elementos.append(tabla_top)
            
            # Estadísticas del curso
            aprobados, reprobados = modelo.obtener_estadisticas_aprobados(codigo_curso)
            total = aprobados + reprobados
            tasa = (aprobados / total * 100) if total > 0 else 0
            
            info_curso = Paragraph(
                f"<i>Estudiantes: {total} | Aprobados: {aprobados} | Reprobados: {reprobados} | Tasa de Aprobación: {tasa:.1f}%</i>",
                estilos['Normal']
            )
            elementos.append(Spacer(1, 0.05*inch))
            elementos.append(info_curso)
            
        else:
            elementos.append(Paragraph("No hay estudiantes matriculados en este curso.", estilos['Normal']))
        
        elementos.append(Spacer(1, 0.3*inch))
    
    elementos.append(PageBreak())
    
    # ==================== GRÁFICAS ESTADÍSTICAS ====================
    subtitulo = Paragraph("3. Gráficas Estadísticas por Curso", estilo_subtitulo)
    elementos.append(subtitulo)
    elementos.append(Spacer(1, 0.2*inch))
    
    # Crear directorio temporal para gráficas
    temp_dir = "temp_graficas"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    graficas_generadas = 0
    
    for codigo_curso, curso in sorted(modelo.cursos.items()):
        aprobados, reprobados = modelo.obtener_estadisticas_aprobados(codigo_curso)
        
        if aprobados == 0 and reprobados == 0:
            continue
        
        graficas_generadas += 1
        
        # Crear figura con dos subgráficas
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        
        # Gráfico de barras
        categorias = ['Aprobados\n(≥ 3.0)', 'Reprobados\n(< 3.0)']
        valores = [aprobados, reprobados]
        colores_bar = ['#2ecc71', '#e74c3c']
        
        bars = ax1.bar(categorias, valores, color=colores_bar, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax1.set_title(f'Distribución de Estudiantes\n{codigo_curso} - {curso.nombre}', 
                     fontsize=12, fontweight='bold', pad=10)
        ax1.set_ylabel('Cantidad de Estudiantes', fontsize=10, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        ax1.set_ylim(0, max(valores) * 1.2 if max(valores) > 0 else 1)
        
        # Agregar valores en las barras
        for bar, valor in zip(bars, valores):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{valor}', ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        # Gráfico de torta
        if aprobados + reprobados > 0:
            sizes = [aprobados, reprobados]
            labels = [f'Aprobados\n{aprobados}', f'Reprobados\n{reprobados}']
            colors_pie = ['#2ecc71', '#e74c3c']
            explode = (0.05, 0.05)
            
            wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors_pie, 
                                              autopct='%1.1f%%', startangle=90, 
                                              explode=explode, shadow=True)
            ax2.set_title(f'Proporción de Aprobación\n{codigo_curso}', 
                         fontsize=12, fontweight='bold', pad=10)
            
            # Mejorar formato del texto
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
        
        plt.tight_layout()
        
        # Guardar gráfica
        nombre_grafica = f"{temp_dir}/grafica_{codigo_curso}.png"
        plt.savefig(nombre_grafica, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        # Agregar al PDF
        titulo_grafica = Paragraph(f"<b>{codigo_curso} - {curso.nombre}</b>", estilos['Heading4'])
        elementos.append(titulo_grafica)
        
        img = Image(nombre_grafica, width=6.5*inch, height=2.6*inch)
        elementos.append(img)
        
        # Información adicional
        total = aprobados + reprobados
        tasa = (aprobados / total * 100) if total > 0 else 0
        notas_curso = [nota for _, cod, nota in modelo.matriculas if cod == codigo_curso]
        promedio_curso = sum(notas_curso) / len(notas_curso) if notas_curso else 0
        
        info = Paragraph(
            f"<i>Total: {total} estudiantes | Promedio: {promedio_curso:.2f} | Tasa de Aprobación: {tasa:.1f}%</i>",
            estilos['Normal']
        )
        elementos.append(Spacer(1, 0.05*inch))
        elementos.append(info)
        elementos.append(Spacer(1, 0.3*inch))
    
    if graficas_generadas == 0:
        elementos.append(Paragraph("No hay datos suficientes para generar gráficas.", estilos['Normal']))
    
    # Construir PDF
    doc.build(elementos)
    
    # Limpiar archivos temporales
    if os.path.exists(temp_dir):
        for archivo in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, archivo))
        os.rmdir(temp_dir)
    
    print(f"Reporte completo exportado como {nombre_archivo}")


def exportar_pdf(nombre_archivo, dataframe):
    """Exporta un DataFrame de pandas a un PDF en formato tabla (versión simple)."""
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