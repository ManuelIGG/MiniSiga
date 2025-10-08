## ==================== vista.py ====================
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from datetime import datetime


# ==================== VISTA ====================
class VistaSIGA:
    def __init__(self, root):
        self.root = root
        self.root.title("MiniSIGA - Sistema de Gestión Académica")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Controlador se asignará después
        self.controlador = None
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar peso de filas y columnas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="MiniSIGA", font=('Arial', 20, 'bold'))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Panel izquierdo - Dashboard
        self.crear_dashboard(main_frame)
        
        # Panel derecho - Contenido principal
        self.crear_panel_principal(main_frame)
        
        # Panel inferior - KPIs
        self.crear_panel_kpis(main_frame)
        
    def crear_dashboard(self, parent):
        # Frame para dashboard
        dashboard_frame = ttk.LabelFrame(parent, text="Dashboard", padding="10")
        dashboard_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W), padx=(0, 10))
        
        # Botones de navegación
        ttk.Button(dashboard_frame, text="Gestión de Estudiantes", 
                  command=self.mostrar_gestion_estudiantes).pack(fill=tk.X, pady=5)
        
        ttk.Button(dashboard_frame, text="Gestión de Cursos", 
                  command=self.mostrar_gestion_cursos).pack(fill=tk.X, pady=5)
        
        ttk.Button(dashboard_frame, text="Matrículas y Notas", 
                  command=self.mostrar_matriculas).pack(fill=tk.X, pady=5)
        
        ttk.Button(dashboard_frame, text="Consultas/Reportes", 
                  command=self.mostrar_reportes).pack(fill=tk.X, pady=5)
        
        ttk.Separator(dashboard_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        ttk.Button(dashboard_frame, text="Cargar CSV", 
                  command=self.cargar_csv).pack(fill=tk.X, pady=5)
        
        ttk.Button(dashboard_frame, text="Cargar JSON", 
                  command=self.cargar_json).pack(fill=tk.X, pady=5)
        
        ttk.Button(dashboard_frame, text="Guardar JSON", 
                  command=self.guardar_json).pack(fill=tk.X, pady=5)
        
    def crear_panel_principal(self, parent):
            
        # Notebook para pestañas
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Pestaña de gestión de estudiantes
        self.frame_estudiantes = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_estudiantes, text="Gestión de Estudiantes")
        self.crear_gestion_estudiantes()
        
        # Pestaña de gestión de cursos
        self.frame_cursos = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_cursos, text="Gestión de Cursos")
        self.crear_gestion_cursos()
        
        # Pestaña de matrículas
        self.frame_matriculas = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_matriculas, text="Matrículas y Notas")
        self.crear_matriculas()
        
        # Pestaña de reportes
        self.frame_reportes = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_reportes, text="Consultas/Reportes")
        self.crear_reportes()
        
        # ← AGREGAR ESTA LÍNEA:
        # Pestaña de predicción con IA
        self.crear_panel_prediccion()

## Métodos adicionales para la clase VistaSIGA

def crear_panel_prediccion(self):
    """Crea la pestaña de predicciones con IA"""
    frame = ttk.Frame(self.notebook)
    self.notebook.add(frame, text="🤖 Predicción IA")
    self.frame_prediccion = frame
    
    # ==================== SECCIÓN DE ENTRENAMIENTO ====================
    training_frame = ttk.LabelFrame(frame, text="🎓 Entrenamiento del Modelo", padding="15")
    training_frame.pack(fill=tk.X, padx=10, pady=10)
    
    info_label = ttk.Label(
        training_frame,
        text="El modelo de IA aprende de los datos históricos para predecir el rendimiento académico.",
        wraplength=800,
        justify=tk.LEFT
    )
    info_label.pack(pady=5)
    
    button_frame = ttk.Frame(training_frame)
    button_frame.pack(pady=10)
    
    ttk.Button(
        button_frame,
        text="🚀 Entrenar Modelo",
        command=self.btn_entrenar_modelo,
        width=20
    ).pack(side=tk.LEFT, padx=5)
    
    ttk.Button(
        button_frame,
        text="📁 Cargar Modelo",
        command=self.btn_cargar_modelo,
        width=20
    ).pack(side=tk.LEFT, padx=5)
    
    # ==================== SECCIÓN DE PREDICCIÓN INDIVIDUAL ====================
    pred_frame = ttk.LabelFrame(frame, text="🔮 Predicción Individual", padding="15")
    pred_frame.pack(fill=tk.X, padx=10, pady=10)
    
    # Primera fila
    row1 = ttk.Frame(pred_frame)
    row1.pack(fill=tk.X, pady=5)
    
    ttk.Label(row1, text="Documento Estudiante:").pack(side=tk.LEFT, padx=5)
    self.entry_pred_documento = ttk.Entry(row1, width=15)
    self.entry_pred_documento.pack(side=tk.LEFT, padx=5)
    
    ttk.Label(row1, text="Código Curso:").pack(side=tk.LEFT, padx=(20, 5))
    self.entry_pred_curso = ttk.Entry(row1, width=15)
    self.entry_pred_curso.pack(side=tk.LEFT, padx=5)
    
    ttk.Button(
        row1,
        text="🎯 Predecir",
        command=self.btn_predecir_individual
    ).pack(side=tk.LEFT, padx=10)
    
    # Segunda fila - Predicción de todos los cursos
    row2 = ttk.Frame(pred_frame)
    row2.pack(fill=tk.X, pady=5)
    
    ttk.Label(row2, text="Documento Estudiante:").pack(side=tk.LEFT, padx=5)
    self.entry_pred_batch = ttk.Entry(row2, width=15)
    self.entry_pred_batch.pack(side=tk.LEFT, padx=5)
    
    ttk.Button(
        row2,
        text="📊 Predecir Todos los Cursos",
        command=self.btn_predecir_batch
    ).pack(side=tk.LEFT, padx=10)
    
    # ==================== SECCIÓN DE ANÁLISIS ====================
    analysis_frame = ttk.LabelFrame(frame, text="📈 Análisis Avanzado", padding="15")
    analysis_frame.pack(fill=tk.X, padx=10, pady=10)
    
    btn_row = ttk.Frame(analysis_frame)
    btn_row.pack(pady=5)
    
    ttk.Button(
        btn_row,
        text="⚠️ Estudiantes en Riesgo",
        command=self.btn_estudiantes_riesgo,
        width=25
    ).pack(side=tk.LEFT, padx=5)
    
    ttk.Button(
        btn_row,
        text="💡 Recomendar Cursos",
        command=self.btn_recomendar_cursos,
        width=25
    ).pack(side=tk.LEFT, padx=5)
    
    # Para recomendaciones
    rec_row = ttk.Frame(analysis_frame)
    rec_row.pack(pady=5)
    
    ttk.Label(rec_row, text="Documento para recomendaciones:").pack(side=tk.LEFT, padx=5)
    self.entry_rec_documento = ttk.Entry(rec_row, width=15)
    self.entry_rec_documento.pack(side=tk.LEFT, padx=5)
    
    # ==================== ÁREA DE RESULTADOS ====================
    results_frame = ttk.LabelFrame(frame, text="📋 Resultados de Predicción", padding="10")
    results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Texto con scrollbar
    self.text_prediccion = tk.Text(results_frame, height=20, wrap=tk.WORD, font=('Consolas', 10))
    scrollbar_pred = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.text_prediccion.yview)
    self.text_prediccion.configure(yscrollcommand=scrollbar_pred.set)
    
    self.text_prediccion.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_pred.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Configurar tags para colores
    self.text_prediccion.tag_config('exito', foreground='#27ae60', font=('Consolas', 10, 'bold'))
    self.text_prediccion.tag_config('riesgo', foreground='#e74c3c', font=('Consolas', 10, 'bold'))
    self.text_prediccion.tag_config('advertencia', foreground='#f39c12', font=('Consolas', 10, 'bold'))
    self.text_prediccion.tag_config('titulo', foreground='#2c3e50', font=('Consolas', 12, 'bold'))
    self.text_prediccion.tag_config('subtitulo', foreground='#34495e', font=('Consolas', 11, 'bold'))

# ==================== MÉTODOS DE EVENTOS PARA PREDICCIÓN ====================

def btn_entrenar_modelo(self):
    """Entrena el modelo de predicción con IA"""
    if self.controlador:
        # Ventana de confirmación
        respuesta = messagebox.askyesno(
            "Entrenar Modelo",
            "¿Desea entrenar un nuevo modelo de predicción?\n\n"
            "Este proceso puede tardar unos minutos y utilizará\n"
            "todos los datos actuales del sistema.\n\n"
            f"Matrículas disponibles: {len(self.controlador.modelo.matriculas)}"
        )
        
        if respuesta:
            # Ventana de progreso
            ventana_progreso = tk.Toplevel(self.root)
            ventana_progreso.title("Entrenando Modelo...")
            ventana_progreso.geometry("400x200")
            ventana_progreso.transient(self.root)
            ventana_progreso.grab_set()
            
            # Centrar ventana
            ventana_progreso.update_idletasks()
            x = (ventana_progreso.winfo_screenwidth() // 2) - 200
            y = (ventana_progreso.winfo_screenheight() // 2) - 100
            ventana_progreso.geometry(f"400x200+{x}+{y}")
            
            frame = ttk.Frame(ventana_progreso, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(
                frame,
                text="🤖 Entrenando Red Neuronal...",
                font=('Arial', 14, 'bold')
            ).pack(pady=10)
            
            ttk.Label(
                frame,
                text="Procesando datos históricos\ny optimizando parámetros...",
                justify=tk.CENTER
            ).pack(pady=10)
            
            progress = ttk.Progressbar(frame, mode='indeterminate', length=300)
            progress.pack(pady=20)
            progress.start(10)
            
            ventana_progreso.update()
            
            # Entrenar modelo
            exito = self.controlador.entrenar_modelo_prediccion()
            
            progress.stop()
            ventana_progreso.destroy()

def btn_cargar_modelo(self):
    """Carga un modelo previamente entrenado"""
    if self.controlador:
        self.controlador.cargar_modelo_prediccion()

def btn_predecir_individual(self):
    """Realiza una predicción individual para un estudiante en un curso"""
    if not self.controlador:
        return
    
    documento = self.entry_pred_documento.get().strip()
    codigo_curso = self.entry_pred_curso.get().strip()
    
    if not documento or not codigo_curso:
        self.mostrar_error("Error", "Debe ingresar documento y código de curso")
        return
    
    resultado = self.controlador.predecir_estudiante(documento, codigo_curso)
    
    if resultado:
        self._mostrar_resultado_prediccion_individual(documento, codigo_curso, resultado)

def _mostrar_resultado_prediccion_individual(self, documento, codigo_curso, resultado):
    """Muestra el resultado de una predicción individual en el área de texto"""
    self.text_prediccion.delete(1.0, tk.END)
    
    # Obtener datos del estudiante
    estudiante = self.controlador.modelo.estudiantes.get(documento)
    curso = self.controlador.modelo.cursos.get(codigo_curso)
    
    # Título
    self.text_prediccion.insert(tk.END, "🎯 PREDICCIÓN INDIVIDUAL\n", 'titulo')
    self.text_prediccion.insert(tk.END, "="*70 + "\n\n")
    
    # Datos del estudiante
    self.text_prediccion.insert(tk.END, "👤 ESTUDIANTE:\n", 'subtitulo')
    self.text_prediccion.insert(tk.END, f"   Documento: {documento}\n")
    self.text_prediccion.insert(tk.END, f"   Nombre: {estudiante.nombre} {estudiante.apellidos}\n")
    self.text_prediccion.insert(tk.END, f"   Correo: {estudiante.correo}\n\n")
    
    # Datos del curso
    self.text_prediccion.insert(tk.END, "📚 CURSO:\n", 'subtitulo')
    self.text_prediccion.insert(tk.END, f"   Código: {codigo_curso}\n")
    self.text_prediccion.insert(tk.END, f"   Nombre: {curso.nombre}\n\n")
    
    # Resultado de la predicción
    self.text_prediccion.insert(tk.END, "🔮 RESULTADO DE LA PREDICCIÓN:\n", 'subtitulo')
    self.text_prediccion.insert(tk.END, "-"*70 + "\n")
    
    prediccion = resultado['prediccion']
    probabilidad = resultado['probabilidad_aprobar'] * 100
    confianza = resultado['confianza'] * 100
    
    # Colorear según la predicción
    if prediccion == "APROBARÁ":
        self.text_prediccion.insert(tk.END, f"   Estado Predicho: {prediccion} ✅\n", 'exito')
    else:
        self.text_prediccion.insert(tk.END, f"   Estado Predicho: {prediccion} ❌\n", 'riesgo')
    
    self.text_prediccion.insert(tk.END, f"   Probabilidad de Aprobar: {probabilidad:.2f}%\n")
    self.text_prediccion.insert(tk.END, f"   Confianza del Modelo: {confianza:.2f}%\n\n")
    
    # Features utilizadas
    self.text_prediccion.insert(tk.END, "📊 FACTORES ANALIZADOS:\n", 'subtitulo')
    features = resultado['features']
    self.text_prediccion.insert(tk.END, f"   • Promedio del Estudiante: {features['promedio_estudiante']:.2f}\n")
    self.text_prediccion.insert(tk.END, f"   • Cursos Matriculados: {features['num_cursos']}\n")
    self.text_prediccion.insert(tk.END, f"   • Promedio del Curso: {features['promedio_curso']:.2f}\n")
    self.text_prediccion.insert(tk.END, f"   • Tasa de Aprobación del Curso: {features['tasa_aprobacion_curso']*100:.1f}%\n\n")
    
    # Recomendaciones
    self.text_prediccion.insert(tk.END, "💡 RECOMENDACIONES:\n", 'subtitulo')
    if probabilidad < 50:
        self.text_prediccion.insert(tk.END, "   ⚠️  ALTO RIESGO DE REPROBAR\n", 'riesgo')
        self.text_prediccion.insert(tk.END, "   • Considere tutorías adicionales\n")
        self.text_prediccion.insert(tk.END, "   • Revise los horarios de estudio\n")
        self.text_prediccion.insert(tk.END, "   • Busque apoyo del profesor\n")
    elif probabilidad < 70:
        self.text_prediccion.insert(tk.END, "   ⚠️  RIESGO MODERADO\n", 'advertencia')
        self.text_prediccion.insert(tk.END, "   • Mantenga un estudio constante\n")
        self.text_prediccion.insert(tk.END, "   • Participe activamente en clase\n")
    else:
        self.text_prediccion.insert(tk.END, "   ✅ BUEN PRONÓSTICO\n", 'exito')
        self.text_prediccion.insert(tk.END, "   • Continúe con el buen trabajo\n")
        self.text_prediccion.insert(tk.END, "   • Mantenga el ritmo de estudio\n")

def btn_predecir_batch(self):
    """Predice el rendimiento en todos los cursos de un estudiante"""
    if not self.controlador:
        return
    
    documento = self.entry_pred_batch.get().strip()
    
    if not documento:
        self.mostrar_error("Error", "Debe ingresar un documento de estudiante")
        return
    
    predicciones = self.controlador.predecir_todos_cursos_estudiante(documento)
    
    if predicciones:
        self._mostrar_resultados_batch(documento, predicciones)

def _mostrar_resultados_batch(self, documento, predicciones):
    """Muestra los resultados de predicción de todos los cursos"""
    self.text_prediccion.delete(1.0, tk.END)
    
    estudiante = self.controlador.modelo.estudiantes.get(documento)
    
    # Título
    self.text_prediccion.insert(tk.END, "📊 ANÁLISIS COMPLETO DEL ESTUDIANTE\n", 'titulo')
    self.text_prediccion.insert(tk.END, "="*70 + "\n\n")
    
    # Datos del estudiante
    self.text_prediccion.insert(tk.END, "👤 ESTUDIANTE:\n", 'subtitulo')
    self.text_prediccion.insert(tk.END, f"   {estudiante.nombre} {estudiante.apellidos}\n")
    self.text_prediccion.insert(tk.END, f"   Documento: {documento}\n")
    self.text_prediccion.insert(tk.END, f"   Total de cursos: {len(predicciones)}\n\n")
    
    # Estadísticas generales
    prob_promedio = sum(p['probabilidad_aprobar'] for p in predicciones) / len(predicciones)
    cursos_riesgo = sum(1 for p in predicciones if p['probabilidad_aprobar'] < 0.5)
    
    self.text_prediccion.insert(tk.END, "📈 ESTADÍSTICAS GENERALES:\n", 'subtitulo')
    self.text_prediccion.insert(tk.END, f"   Probabilidad Promedio de Éxito: {prob_promedio*100:.2f}%\n")
    self.text_prediccion.insert(tk.END, f"   Cursos en Riesgo: {cursos_riesgo}/{len(predicciones)}\n\n")
    
    # Detalle por curso
    self.text_prediccion.insert(tk.END, "📚 PREDICCIÓN POR CURSO:\n", 'subtitulo')
    self.text_prediccion.insert(tk.END, "-"*70 + "\n\n")
    
    # Ordenar por probabilidad (menor a mayor para ver riesgos primero)
    predicciones_ordenadas = sorted(predicciones, key=lambda x: x['probabilidad_aprobar'])
    
    for i, pred in enumerate(predicciones_ordenadas, 1):
        curso = pred['curso']
        nombre_curso = pred['nombre_curso']
        prob = pred['probabilidad_aprobar'] * 100
        prediccion = pred['prediccion']
        
        self.text_prediccion.insert(tk.END, f"{i}. {curso} - {nombre_curso}\n")
        
        if prediccion == "APROBARÁ":
            self.text_prediccion.insert(tk.END, f"   ✅ {prediccion} ({prob:.1f}%)\n", 'exito')
        else:
            self.text_prediccion.insert(tk.END, f"   ❌ {prediccion} ({prob:.1f}%)\n", 'riesgo')
        
        # Barra de progreso visual
        barras = int(prob / 5)
        self.text_prediccion.insert(tk.END, f"   [{'█' * barras}{'░' * (20-barras)}]\n\n")

def btn_estudiantes_riesgo(self):
    """Identifica y muestra estudiantes en riesgo de reprobar"""
    if not self.controlador:
        return
    
    estudiantes_riesgo = self.controlador.obtener_estudiantes_riesgo(umbral=0.5)
    
    if not estudiantes_riesgo:
        self.text_prediccion.delete(1.0, tk.END)
        self.text_prediccion.insert(tk.END, "✅ ¡Excelente! No hay estudiantes en riesgo alto.\n", 'exito')
        return
    
    self._mostrar_estudiantes_riesgo(estudiantes_riesgo)

def _mostrar_estudiantes_riesgo(self, estudiantes_riesgo):
    """Muestra el reporte de estudiantes en riesgo"""
    self.text_prediccion.delete(1.0, tk.END)
    
    # Título
    self.text_prediccion.insert(tk.END, "⚠️  ALERTA: ESTUDIANTES EN RIESGO\n", 'titulo')
    self.text_prediccion.insert(tk.END, "="*70 + "\n\n")
    
    self.text_prediccion.insert(tk.END, f"Total de estudiantes en riesgo: {len(estudiantes_riesgo)}\n\n", 'riesgo')
    
    # Agrupar por nivel de riesgo
    riesgo_alto = [e for e in estudiantes_riesgo if e['probabilidad_aprobar'] < 0.3]
    riesgo_medio = [e for e in estudiantes_riesgo if 0.3 <= e['probabilidad_aprobar'] < 0.5]
    
    # RIESGO ALTO
    if riesgo_alto:
        self.text_prediccion.insert(tk.END, "🚨 RIESGO ALTO (< 30%):\n", 'riesgo')
        self.text_prediccion.insert(tk.END, "-"*70 + "\n")
        
        for est in riesgo_alto:
            self.text_prediccion.insert(tk.END, f"\n📌 {est['nombre']}\n")
            self.text_prediccion.insert(tk.END, f"   Documento: {est['documento']}\n")
            self.text_prediccion.insert(tk.END, f"   Curso: {est['curso']} - {est['nombre_curso']}\n")
            self.text_prediccion.insert(tk.END, f"   Probabilidad de aprobar: {est['probabilidad_aprobar']*100:.1f}%\n", 'riesgo')
            self.text_prediccion.insert(tk.END, f"   Nota actual: {est['promedio_actual']:.2f}\n")
        
        self.text_prediccion.insert(tk.END, "\n")
    
    # RIESGO MEDIO
    if riesgo_medio:
        self.text_prediccion.insert(tk.END, "⚠️  RIESGO MEDIO (30% - 50%):\n", 'advertencia')
        self.text_prediccion.insert(tk.END, "-"*70 + "\n")
        
        for est in riesgo_medio:
            self.text_prediccion.insert(tk.END, f"\n📌 {est['nombre']}\n")
            self.text_prediccion.insert(tk.END, f"   Documento: {est['documento']}\n")
            self.text_prediccion.insert(tk.END, f"   Curso: {est['curso']} - {est['nombre_curso']}\n")
            self.text_prediccion.insert(tk.END, f"   Probabilidad de aprobar: {est['probabilidad_aprobar']*100:.1f}%\n", 'advertencia')
            self.text_prediccion.insert(tk.END, f"   Nota actual: {est['promedio_actual']:.2f}\n")
    
    # Recomendaciones
    self.text_prediccion.insert(tk.END, "\n\n💡 ACCIONES RECOMENDADAS:\n", 'subtitulo')
    self.text_prediccion.insert(tk.END, "   • Contactar a los estudiantes en riesgo alto prioritariamente\n")
    self.text_prediccion.insert(tk.END, "   • Ofrecer tutorías o asesorías académicas\n")
    self.text_prediccion.insert(tk.END, "   • Revisar estrategias pedagógicas en cursos con alta reprobación\n")
    self.text_prediccion.insert(tk.END, "   • Implementar sistemas de seguimiento continuo\n")

def btn_recomendar_cursos(self):
    """Genera recomendaciones de cursos para un estudiante"""
    if not self.controlador:
        return
    
    documento = self.entry_rec_documento.get().strip()
    
    if not documento:
        self.mostrar_error("Error", "Debe ingresar un documento de estudiante")
        return
    
    recomendaciones = self.controlador.recomendar_cursos_estudiante(documento)
    
    if recomendaciones is not None:
        self._mostrar_recomendaciones_cursos(documento, recomendaciones)

def _mostrar_recomendaciones_cursos(self, documento, recomendaciones):
    """Muestra las recomendaciones de cursos"""
    self.text_prediccion.delete(1.0, tk.END)
    
    estudiante = self.controlador.modelo.estudiantes.get(documento)
    
    # Título
    self.text_prediccion.insert(tk.END, "💡 RECOMENDACIÓN DE CURSOS\n", 'titulo')
    self.text_prediccion.insert(tk.END, "="*70 + "\n\n")
    
    # Datos del estudiante
    self.text_prediccion.insert(tk.END, "👤 ESTUDIANTE:\n", 'subtitulo')
    self.text_prediccion.insert(tk.END, f"   {estudiante.nombre} {estudiante.apellidos}\n")
    self.text_prediccion.insert(tk.END, f"   Documento: {documento}\n\n")
    
    if not recomendaciones:
        self.text_prediccion.insert(tk.END, "ℹ️  No hay cursos disponibles para recomendar.\n")
        self.text_prediccion.insert(tk.END, "   El estudiante ya está matriculado en todos los cursos.\n")
        return
    
    self.text_prediccion.insert(tk.END, f"📚 Cursos disponibles: {len(recomendaciones)}\n\n")
    
    # Clasificar por nivel de dificultad
    faciles = [r for r in recomendaciones if r['nivel_dificultad'] == 'Fácil']
    medios = [r for r in recomendaciones if r['nivel_dificultad'] == 'Medio']
    dificiles = [r for r in recomendaciones if r['nivel_dificultad'] == 'Difícil']
    
    # CURSOS FÁCILES
    if faciles:
        self.text_prediccion.insert(tk.END, "✅ CURSOS RECOMENDADOS (Alta probabilidad de éxito):\n", 'exito')
        self.text_prediccion.insert(tk.END, "-"*70 + "\n")
        
        for i, rec in enumerate(faciles[:5], 1):  # Top 5
            prob = rec['probabilidad_exito'] * 100
            self.text_prediccion.insert(tk.END, f"\n{i}. {rec['curso']} - {rec['nombre']}\n")
            self.text_prediccion.insert(tk.END, f"   Probabilidad de éxito: {prob:.1f}%\n", 'exito')
            self.text_prediccion.insert(tk.END, f"   Nivel: {rec['nivel_dificultad']}\n")
            barras = int(prob / 5)
            self.text_prediccion.insert(tk.END, f"   [{'█' * barras}{'░' * (20-barras)}]\n")
        
        self.text_prediccion.insert(tk.END, "\n")
    
    # CURSOS MEDIOS
    if medios:
        self.text_prediccion.insert(tk.END, "⚠️  CURSOS MODERADOS:\n", 'advertencia')
        self.text_prediccion.insert(tk.END, "-"*70 + "\n")
        
        for i, rec in enumerate(medios[:3], 1):  # Top 3
            prob = rec['probabilidad_exito'] * 100
            self.text_prediccion.insert(tk.END, f"\n{i}. {rec['curso']} - {rec['nombre']}\n")
            self.text_prediccion.insert(tk.END, f"   Probabilidad de éxito: {prob:.1f}%\n", 'advertencia')
            self.text_prediccion.insert(tk.END, f"   Nivel: {rec['nivel_dificultad']}\n")
        
        self.text_prediccion.insert(tk.END, "\n")
    
    # CURSOS DIFÍCILES
    if dificiles:
        self.text_prediccion.insert(tk.END, "⛔ CURSOS DESAFIANTES (Requieren preparación adicional):\n", 'riesgo')
        self.text_prediccion.insert(tk.END, "-"*70 + "\n")
        
        for i, rec in enumerate(dificiles[:3], 1):  # Top 3
            prob = rec['probabilidad_exito'] * 100
            self.text_prediccion.insert(tk.END, f"\n{i}. {rec['curso']} - {rec['nombre']}\n")
            self.text_prediccion.insert(tk.END, f"   Probabilidad de éxito: {prob:.1f}%\n", 'riesgo')
            self.text_prediccion.insert(tk.END, f"   Nivel: {rec['nivel_dificultad']}\n")
    
    # Consejos finales
    self.text_prediccion.insert(tk.END, "\n\n💡 CONSEJOS:\n", 'subtitulo')
    self.text_prediccion.insert(tk.END, "   • Comience con cursos de alta probabilidad de éxito\n")
    self.text_prediccion.insert(tk.END, "   • Equilibre la carga académica con cursos de diferente dificultad\n")
    self.text_prediccion.insert(tk.END, "   • Considere prerequisitos y secuencia recomendada\n")
    self.text_prediccion.insert(tk.END, "   • Consulte con su asesor académico antes de matricular\n")
        
    def crear_gestion_estudiantes(self):
        frame = self.frame_estudiantes
        
        # Formulario para nuevo estudiante
        form_frame = ttk.LabelFrame(frame, text="Nuevo Estudiante", padding="10")
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Documento:").grid(row=0, column=0, sticky=tk.W)
        self.entry_documento = ttk.Entry(form_frame, width=15)
        self.entry_documento.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.entry_nombre = ttk.Entry(form_frame, width=20)
        self.entry_nombre.grid(row=0, column=3, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Apellidos:").grid(row=1, column=0, sticky=tk.W)
        self.entry_apellidos = ttk.Entry(form_frame, width=20)
        self.entry_apellidos.grid(row=1, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Correo:").grid(row=1, column=2, sticky=tk.W, padx=(10, 0))
        self.entry_correo = ttk.Entry(form_frame, width=25)
        self.entry_correo.grid(row=1, column=3, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Fecha Nac. (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W)
        self.entry_fecha = ttk.Entry(form_frame, width=15)
        self.entry_fecha.grid(row=2, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Button(form_frame, text="Crear Estudiante", 
                  command=self.btn_crear_estudiante).grid(row=2, column=2, columnspan=2, pady=10)
        
        # Configurar pesos de columnas
        for i in range(4):
            form_frame.columnconfigure(i, weight=1)
        
        # Búsqueda y controles
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(control_frame, text="Buscar:").pack(side=tk.LEFT)
        self.entry_buscar = ttk.Entry(control_frame)
        self.entry_buscar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.entry_buscar.bind('<KeyRelease>', self.on_search)
        
        ttk.Button(control_frame, text="Eliminar Seleccionado", 
                  command=self.btn_eliminar_estudiante).pack(side=tk.RIGHT, padx=5)
        
        # Tabla de estudiantes
        self.crear_tabla_estudiantes(frame)
    
    def crear_gestion_cursos(self):
        frame = self.frame_cursos
        
        # Formulario para nuevo curso
        form_frame = ttk.LabelFrame(frame, text="Nuevo Curso", padding="10")
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Código:").grid(row=0, column=0, sticky=tk.W)
        self.entry_cod_curso = ttk.Entry(form_frame, width=15)
        self.entry_cod_curso.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.entry_nom_curso = ttk.Entry(form_frame, width=30)
        self.entry_nom_curso.grid(row=0, column=3, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Button(form_frame, text="Crear Curso", 
                  command=self.btn_crear_curso).grid(row=0, column=4, padx=10)
        
        ttk.Button(form_frame, text="Eliminar Curso Seleccionado", 
                  command=self.btn_eliminar_curso).grid(row=0, column=5, padx=5)
        
        # Configurar pesos
        for i in range(6):
            form_frame.columnconfigure(i, weight=1)
        
        # Tabla de cursos
        self.crear_tabla_cursos(frame)
        
    def crear_tabla_estudiantes(self, parent):
        # Frame para tabla
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ('documento', 'nombre', 'apellidos', 'correo', 'fecha_nac')
        self.tree_estudiantes = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar encabezados
        self.tree_estudiantes.heading('documento', text='Documento')
        self.tree_estudiantes.heading('nombre', text='Nombre')
        self.tree_estudiantes.heading('apellidos', text='Apellidos')
        self.tree_estudiantes.heading('correo', text='Correo')
        self.tree_estudiantes.heading('fecha_nac', text='Fecha Nac.')
        
        # Configurar anchos de columna
        self.tree_estudiantes.column('documento', width=100)
        self.tree_estudiantes.column('nombre', width=150)
        self.tree_estudiantes.column('apellidos', width=150)
        self.tree_estudiantes.column('correo', width=200)
        self.tree_estudiantes.column('fecha_nac', width=100)
        
        # Scrollbar
        scrollbar_est = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_estudiantes.yview)
        self.tree_estudiantes.configure(yscrollcommand=scrollbar_est.set)
        
        # Empaquetar
        self.tree_estudiantes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_est.pack(side=tk.RIGHT, fill=tk.Y)
    
    def crear_tabla_cursos(self, parent):
        # Frame para tabla
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ('codigo', 'nombre', 'estudiantes', 'promedio')
        self.tree_cursos = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar encabezados
        self.tree_cursos.heading('codigo', text='Código')
        self.tree_cursos.heading('nombre', text='Nombre')
        self.tree_cursos.heading('estudiantes', text='Estudiantes')
        self.tree_cursos.heading('promedio', text='Promedio')
        
        # Configurar anchos de columna
        self.tree_cursos.column('codigo', width=100)
        self.tree_cursos.column('nombre', width=300)
        self.tree_cursos.column('estudiantes', width=100)
        self.tree_cursos.column('promedio', width=100)
        
        # Scrollbar
        scrollbar_cur = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_cursos.yview)
        self.tree_cursos.configure(yscrollcommand=scrollbar_cur.set)
        
        # Empaquetar
        self.tree_cursos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_cur.pack(side=tk.RIGHT, fill=tk.Y)
        
    def crear_matriculas(self):
        frame = self.frame_matriculas
        
        # Formulario para matrícula
        form_frame = ttk.LabelFrame(frame, text="Nueva Matrícula", padding="10")
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Documento Estudiante:").grid(row=0, column=0, sticky=tk.W)
        self.entry_doc_matricula = ttk.Entry(form_frame, width=15)
        self.entry_doc_matricula.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Código Curso:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.entry_curso = ttk.Entry(form_frame, width=15)
        self.entry_curso.grid(row=0, column=3, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Nota (0-5):").grid(row=0, column=4, sticky=tk.W, padx=(10, 0))
        self.entry_nota = ttk.Entry(form_frame, width=10)
        self.entry_nota.grid(row=0, column=5, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Button(form_frame, text="Matricular", 
                  command=self.btn_matricular).grid(row=0, column=6, padx=10)
        
        # Configurar pesos
        for i in range(7):
            form_frame.columnconfigure(i, weight=1)
        
        # Actualizar nota
        update_frame = ttk.LabelFrame(frame, text="Actualizar Nota", padding="10")
        update_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(update_frame, text="Documento:").grid(row=0, column=0, sticky=tk.W)
        self.entry_doc_update = ttk.Entry(update_frame, width=15)
        self.entry_doc_update.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(update_frame, text="Código Curso:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.entry_curso_update = ttk.Entry(update_frame, width=15)
        self.entry_curso_update.grid(row=0, column=3, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(update_frame, text="Nueva Nota:").grid(row=0, column=4, sticky=tk.W, padx=(10, 0))
        self.entry_nueva_nota = ttk.Entry(update_frame, width=10)
        self.entry_nueva_nota.grid(row=0, column=5, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Button(update_frame, text="Actualizar Nota", 
                  command=self.btn_actualizar_nota).grid(row=0, column=6, padx=10)
        
        # Configurar pesos
        for i in range(7):
            update_frame.columnconfigure(i, weight=1)
        
        # Filtros
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Filtrar por curso:").pack(side=tk.LEFT)
        self.entry_filtro_curso = ttk.Entry(filter_frame, width=15)
        self.entry_filtro_curso.pack(side=tk.LEFT, padx=5)
        self.entry_filtro_curso.bind('<KeyRelease>', self.on_filter_matriculas)
        
        ttk.Button(filter_frame, text="Mostrar Todas", 
                  command=self.mostrar_todas_matriculas).pack(side=tk.LEFT, padx=10)
        
        # Tabla de matrículas
        self.crear_tabla_matriculas(frame)
    
    def crear_tabla_matriculas(self, parent):
        # Frame para tabla
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ('documento', 'nombre_estudiante', 'codigo_curso', 'nombre_curso', 'nota')
        self.tree_matriculas = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        # Configurar encabezados
        self.tree_matriculas.heading('documento', text='Documento')
        self.tree_matriculas.heading('nombre_estudiante', text='Nombre Estudiante')
        self.tree_matriculas.heading('codigo_curso', text='Código Curso')
        self.tree_matriculas.heading('nombre_curso', text='Nombre Curso')
        self.tree_matriculas.heading('nota', text='Nota')
        
        # Configurar anchos de columna
        self.tree_matriculas.column('documento', width=100)
        self.tree_matriculas.column('nombre_estudiante', width=200)
        self.tree_matriculas.column('codigo_curso', width=100)
        self.tree_matriculas.column('nombre_curso', width=200)
        self.tree_matriculas.column('nota', width=80)
        
        # Scrollbar
        scrollbar_mat = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_matriculas.yview)
        self.tree_matriculas.configure(yscrollcommand=scrollbar_mat.set)
        
        # Empaquetar
        self.tree_matriculas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_mat.pack(side=tk.RIGHT, fill=tk.Y)
        
    def crear_reportes(self):
        frame = self.frame_reportes
        
        # Controles de búsqueda y filtros
        control_frame = ttk.LabelFrame(frame, text="Consultas", padding="10")
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Primera fila de controles
        ttk.Label(control_frame, text="Buscar estudiante:").grid(row=0, column=0, sticky=tk.W)
        self.entry_buscar_reporte = ttk.Entry(control_frame, width=20)
        self.entry_buscar_reporte.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Button(control_frame, text="Buscar", 
                   command=self.btn_buscar_reporte).grid(row=0, column=2, padx=5)
        
        # Segunda fila de controles
        ttk.Label(control_frame, text="Código curso para reportes:").grid(row=1, column=0, sticky=tk.W)
        self.entry_curso_grafico = ttk.Entry(control_frame, width=15)
        self.entry_curso_grafico.grid(row=1, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Button(control_frame, text="Top 3 Estudiantes", 
                   command=self.btn_top_estudiantes).grid(row=1, column=2, padx=5)
        
        ttk.Button(control_frame, text="Gráfico Aprobados/Reprobados", 
                   command=self.btn_grafico_aprobados).grid(row=1, column=3, padx=5)
        
        # Nueva fila para exportar reportes
        export_frame = ttk.Frame(control_frame)
        export_frame.grid(row=2, column=0, columnspan=4, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Label(export_frame, text="Exportar reporte:").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(export_frame, text="📄 Reporte Simple (PDF)", 
                   command=self.btn_exportar_pdf_simple).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(export_frame, text="📊 Reporte Completo (PDF)", 
                   command=self.btn_exportar_pdf_completo).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(export_frame, text="📑 Exportar CSV", 
                   command=self.btn_exportar_csv).pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="Estadísticas Generales", 
                   command=self.btn_estadisticas_generales).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Área de resultados
        results_frame = ttk.LabelFrame(frame, text="Resultados", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.text_resultados = tk.Text(results_frame, height=20, wrap=tk.WORD)
        
        # Scrollbar para texto
        scrollbar_text = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.text_resultados.yview)
        self.text_resultados.configure(yscrollcommand=scrollbar_text.set)
        
        # Empaquetar texto y scrollbar
        self.text_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_text.pack(side=tk.RIGHT, fill=tk.Y)

    # ==================== MÉTODOS DE EXPORTACIÓN ====================
    def btn_exportar_pdf_simple(self):
        """Exporta un reporte simple en PDF con solo la tabla de estudiantes"""
        if self.controlador:
            df = self.controlador.generar_reporte_estudiantes()
            if df.empty:
                self.mostrar_error("Error", "No hay datos para exportar.")
                return
            archivo = filedialog.asksaveasfilename(
                title="Guardar reporte simple en PDF",
                filetypes=[("Archivo PDF", "*.pdf")],
                defaultextension=".pdf",
                initialfile=f"Reporte_Simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            if archivo:
                try:
                    from utils import exportar_pdf
                    exportar_pdf(archivo, df)
                    self.mostrar_mensaje("Éxito", "Reporte simple exportado correctamente.")
                except Exception as e:
                    self.mostrar_error("Error", f"Error al exportar:\n{str(e)}")

    def btn_exportar_pdf_completo(self):
        """Exporta un reporte completo en PDF con top 3 y gráficas"""
        if self.controlador:
            if not self.controlador.modelo.estudiantes:
                self.mostrar_error("Error", "No hay datos para exportar.")
                return
            
            archivo = filedialog.asksaveasfilename(
                title="Guardar reporte completo en PDF",
                filetypes=[("Archivo PDF", "*.pdf")],
                defaultextension=".pdf",
                initialfile=f"Reporte_Completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            
            if archivo:
                try:
                    from utils import exportar_pdf_completo
                    
                    # Ventana de progreso
                    ventana_progreso = tk.Toplevel(self.root)
                    ventana_progreso.title("Generando reporte...")
                    ventana_progreso.geometry("400x150")
                    ventana_progreso.transient(self.root)
                    ventana_progreso.grab_set()
                    
                    # Centrar ventana
                    ventana_progreso.update_idletasks()
                    x = (ventana_progreso.winfo_screenwidth() // 2) - (400 // 2)
                    y = (ventana_progreso.winfo_screenheight() // 2) - (150 // 2)
                    ventana_progreso.geometry(f"400x150+{x}+{y}")
                    
                    frame_progreso = ttk.Frame(ventana_progreso, padding="20")
                    frame_progreso.pack(fill=tk.BOTH, expand=True)
                    
                    ttk.Label(frame_progreso, 
                             text="Generando reporte completo...", 
                             font=('Arial', 12, 'bold')).pack(pady=10)
                    ttk.Label(frame_progreso, 
                             text="Esto puede tardar unos momentos.\nGenerando gráficas y tablas...",
                             justify=tk.CENTER).pack(pady=10)
                    
                    progress = ttk.Progressbar(frame_progreso, mode='indeterminate', length=300)
                    progress.pack(pady=10)
                    progress.start(10)
                    
                    ventana_progreso.update()
                    
                    # Generar reporte
                    exportar_pdf_completo(archivo, self.controlador)
                    
                    progress.stop()
                    ventana_progreso.destroy()
                    
                    self.mostrar_mensaje("Éxito", 
                        f"✅ Reporte completo exportado exitosamente.\n\n"
                        f"📋 El reporte incluye:\n"
                        f"  • Estadísticas generales\n"
                        f"  • Listado completo de estudiantes\n"
                        f"  • Top 3 estudiantes por curso\n"
                        f"  • Gráficas estadísticas de cada curso\n\n"
                        f"📁 Archivo: {os.path.basename(archivo)}")
                    
                except Exception as e:
                    if 'ventana_progreso' in locals():
                        ventana_progreso.destroy()
                    self.mostrar_error("Error", f"Error al generar el reporte:\n{str(e)}")

    def btn_exportar_csv(self):
        """Exporta el reporte a CSV"""
        if self.controlador:
            df = self.controlador.generar_reporte_estudiantes()
            if df.empty:
                self.mostrar_error("Error", "No hay datos para exportar.")
                return
            archivo = filedialog.asksaveasfilename(
                title="Guardar reporte en CSV",
                filetypes=[("Archivos CSV", "*.csv")],
                defaultextension=".csv",
                initialfile=f"Reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            if archivo:
                try:
                    df.to_csv(archivo, index=False, encoding="utf-8-sig")
                    self.mostrar_mensaje("Éxito", "Reporte exportado en CSV correctamente.")
                except Exception as e:
                    self.mostrar_error("Error", f"Error al exportar CSV:\n{str(e)}")
        
    def crear_panel_kpis(self, parent):
        kpi_frame = ttk.LabelFrame(parent, text="Estadísticas Generales", padding="10")
        kpi_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.lbl_total_estudiantes = ttk.Label(kpi_frame, text="Total Estudiantes: 0", font=('Arial', 12, 'bold'))
        self.lbl_total_estudiantes.grid(row=0, column=0, padx=20)
        
        self.lbl_total_cursos = ttk.Label(kpi_frame, text="Total Cursos: 0", font=('Arial', 12, 'bold'))
        self.lbl_total_cursos.grid(row=0, column=1, padx=20)
        
        self.lbl_total_matriculas = ttk.Label(kpi_frame, text="Total Matrículas: 0", font=('Arial', 12, 'bold'))
        self.lbl_total_matriculas.grid(row=0, column=2, padx=20)
        
        self.lbl_promedio_general = ttk.Label(kpi_frame, text="Promedio General: 0.00", font=('Arial', 12, 'bold'))
        self.lbl_promedio_general.grid(row=0, column=3, padx=20)

    # ==================== MÉTODOS DE EVENTOS ====================
    def btn_crear_estudiante(self):
        if self.controlador:
            documento = self.entry_documento.get().strip()
            nombre = self.entry_nombre.get().strip()
            apellidos = self.entry_apellidos.get().strip()
            correo = self.entry_correo.get().strip()
            fecha = self.entry_fecha.get().strip()
            
            if self.controlador.crear_estudiante(documento, nombre, apellidos, correo, fecha):
                # Limpiar campos
                self.entry_documento.delete(0, tk.END)
                self.entry_nombre.delete(0, tk.END)
                self.entry_apellidos.delete(0, tk.END)
                self.entry_correo.delete(0, tk.END)
                self.entry_fecha.delete(0, tk.END)
                self.actualizar_kpis()
    
    def btn_crear_curso(self):
        if self.controlador:
            codigo = self.entry_cod_curso.get().strip()
            nombre = self.entry_nom_curso.get().strip()
            
            if self.controlador.crear_curso(codigo, nombre):
                self.entry_cod_curso.delete(0, tk.END)
                self.entry_nom_curso.delete(0, tk.END)
                self.actualizar_kpis()
    
    def btn_matricular(self):
        if self.controlador:
            documento = self.entry_doc_matricula.get().strip()
            curso = self.entry_curso.get().strip()
            nota = self.entry_nota.get().strip()
            
            if self.controlador.matricular_estudiante(documento, curso, nota):
                self.entry_doc_matricula.delete(0, tk.END)
                self.entry_curso.delete(0, tk.END)
                self.entry_nota.delete(0, tk.END)
                self.actualizar_kpis()
    
    def btn_actualizar_nota(self):
        if self.controlador:
            documento = self.entry_doc_update.get().strip()
            curso = self.entry_curso_update.get().strip()
            nueva_nota = self.entry_nueva_nota.get().strip()
            
            if self.controlador.actualizar_nota(documento, curso, nueva_nota):
                self.entry_doc_update.delete(0, tk.END)
                self.entry_curso_update.delete(0, tk.END)
                self.entry_nueva_nota.delete(0, tk.END)
                self.actualizar_kpis()
    
    def btn_eliminar_estudiante(self):
        selected = self.tree_estudiantes.selection()
        if selected and self.controlador:
            item = self.tree_estudiantes.item(selected[0])
            documento = item['values'][0]
            
            if messagebox.askyesno("Confirmar", f"¿Eliminar estudiante con documento {documento}?"):
                self.controlador.eliminar_estudiante(documento)
                self.actualizar_kpis()
    
    def btn_eliminar_curso(self):
        selected = self.tree_cursos.selection()
        if selected and self.controlador:
            item = self.tree_cursos.item(selected[0])
            codigo_curso = item['values'][0]
            
            if messagebox.askyesno("Confirmar", f"¿Eliminar curso {codigo_curso}?"):
                self.controlador.eliminar_curso(codigo_curso)
                self.actualizar_kpis()
    
    def btn_buscar_reporte(self):
        if self.controlador:
            termino = self.entry_buscar_reporte.get().strip()
            estudiantes = self.controlador.buscar_estudiantes(termino)
            
            self.text_resultados.delete(1.0, tk.END)
            self.text_resultados.insert(tk.END, f"Resultados de búsqueda para: '{termino}'\n")
            self.text_resultados.insert(tk.END, "="*60 + "\n\n")
            
            if estudiantes:
                for est in estudiantes:
                    self.text_resultados.insert(tk.END, f"Documento: {est.documento}\n")
                    self.text_resultados.insert(tk.END, f"Nombre: {est.nombre} {est.apellidos}\n")
                    self.text_resultados.insert(tk.END, f"Correo: {est.correo}\n")
                    self.text_resultados.insert(tk.END, f"Fecha Nacimiento: {est.fecha_nac}\n")
                    self.text_resultados.insert(tk.END, f"Cursos matriculados: {len(est.cursos)}\n")
                    
                    if est.cursos:
                        self.text_resultados.insert(tk.END, "Detalle de cursos y notas:\n")
                        for curso_cod in est.cursos:
                            curso_nombre = self.controlador.modelo.cursos.get(curso_cod, {}).nombre if curso_cod in self.controlador.modelo.cursos else "N/A"
                            nota = est.notas.get(curso_cod, 0.0)
                            estado = "APROBADO" if nota >= 3.0 else "REPROBADO"
                            self.text_resultados.insert(tk.END, f"  - {curso_cod} ({curso_nombre}): {nota} - {estado}\n")
                    
                    self.text_resultados.insert(tk.END, "-"*40 + "\n\n")
            else:
                self.text_resultados.insert(tk.END, "No se encontraron estudiantes con ese criterio.\n")
    
    def btn_top_estudiantes(self):
        if self.controlador:
            curso = self.entry_curso_grafico.get().strip()
            if not curso:
                self.mostrar_error("Error", "Por favor ingrese un código de curso")
                return
                
            top_estudiantes = self.controlador.modelo.obtener_top_estudiantes(curso)
            
            self.text_resultados.delete(1.0, tk.END)
            self.text_resultados.insert(tk.END, f"Top 3 estudiantes en el curso: {curso}\n")
            self.text_resultados.insert(tk.END, "="*60 + "\n\n")
            
            if top_estudiantes:
                curso_nombre = self.controlador.modelo.cursos.get(curso, {}).nombre if curso in self.controlador.modelo.cursos else "N/A"
                self.text_resultados.insert(tk.END, f"Curso: {curso} - {curso_nombre}\n\n")
                
                for i, (estudiante, nota) in enumerate(top_estudiantes, 1):
                    self.text_resultados.insert(tk.END, f"{i}. {estudiante.nombre} {estudiante.apellidos}\n")
                    self.text_resultados.insert(tk.END, f"   Documento: {estudiante.documento}\n")
                    self.text_resultados.insert(tk.END, f"   Correo: {estudiante.correo}\n")
                    self.text_resultados.insert(tk.END, f"   Nota: {nota:.2f}\n")
                    self.text_resultados.insert(tk.END, f"   Estado: {'APROBADO' if nota >= 3.0 else 'REPROBADO'}\n\n")
            else:
                self.text_resultados.insert(tk.END, f"No hay estudiantes matriculados en el curso {curso}.\n")
    
    def btn_grafico_aprobados(self):
        if self.controlador:
            curso = self.entry_curso_grafico.get().strip()
            if not curso:
                self.mostrar_error("Error", "Por favor ingrese un código de curso")
                return
                
            aprobados, reprobados = self.controlador.modelo.obtener_estadisticas_aprobados(curso)
            
            if aprobados == 0 and reprobados == 0:
                self.mostrar_error("Error", f"No hay estudiantes matriculados en el curso {curso}")
                return
            
            # Crear ventana para gráfico
            ventana_grafico = tk.Toplevel(self.root)
            ventana_grafico.title(f"Estadísticas del curso: {curso}")
            ventana_grafico.geometry("700x500")
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Gráfico de barras
            categorias = ['Aprobados\n(≥ 3.0)', 'Reprobados\n(< 3.0)']
            valores = [aprobados, reprobados]
            colores = ['#2ecc71', '#e74c3c']
            
            bars = ax1.bar(categorias, valores, color=colores, alpha=0.8, edgecolor='black')
            ax1.set_title(f'Distribución Aprobados/Reprobados\nCurso: {curso}', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Cantidad de Estudiantes', fontsize=12)
            ax1.grid(axis='y', alpha=0.3)
            
            # Agregar valores en las barras
            for bar, valor in zip(bars, valores):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{valor}', ha='center', va='bottom', fontweight='bold', fontsize=12)
            
            # Gráfico de torta
            if aprobados + reprobados > 0:
                sizes = [aprobados, reprobados]
                labels = [f'Aprobados\n({aprobados})', f'Reprobados\n({reprobados})']
                colors = ['#2ecc71', '#e74c3c']
                explode = (0.05, 0.05)
                
                wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                                  startangle=90, explode=explode, shadow=True)
                ax2.set_title(f'Proporción de Estudiantes\nCurso: {curso}', fontsize=14, fontweight='bold')
                
                # Mejorar el formato del texto
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, ventana_grafico)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Agregar información adicional
            info_frame = ttk.Frame(ventana_grafico)
            info_frame.pack(fill=tk.X, padx=10, pady=5)
            
            total = aprobados + reprobados
            porcentaje_aprobacion = (aprobados / total * 100) if total > 0 else 0
            
            info_text = f"Total estudiantes: {total} | Tasa de aprobación: {porcentaje_aprobacion:.1f}%"
            ttk.Label(info_frame, text=info_text, font=('Arial', 10, 'bold')).pack()
    
    def btn_estadisticas_generales(self):
        if self.controlador:
            modelo = self.controlador.modelo
            
            self.text_resultados.delete(1.0, tk.END)
            self.text_resultados.insert(tk.END, "ESTADÍSTICAS GENERALES DEL SISTEMA\n")
            self.text_resultados.insert(tk.END, "="*60 + "\n\n")
            
            # Estadísticas básicas
            total_estudiantes = len(modelo.estudiantes)
            total_cursos = len(modelo.cursos)
            total_matriculas = len(modelo.matriculas)
            
            self.text_resultados.insert(tk.END, f"Total de estudiantes: {total_estudiantes}\n")
            self.text_resultados.insert(tk.END, f"Total de cursos: {total_cursos}\n")
            self.text_resultados.insert(tk.END, f"Total de matrículas: {total_matriculas}\n\n")
            
            if total_matriculas > 0:
                # Promedio general
                notas = [nota for _, _, nota in modelo.matriculas]
                promedio_general = sum(notas) / len(notas)
                self.text_resultados.insert(tk.END, f"Promedio general: {promedio_general:.2f}\n")
                
                # Distribución de notas
                aprobados_total = sum(1 for nota in notas if nota >= 3.0)
                reprobados_total = len(notas) - aprobados_total
                tasa_aprobacion = (aprobados_total / len(notas)) * 100
                
                self.text_resultados.insert(tk.END, f"Estudiantes aprobados (≥3.0): {aprobados_total}\n")
                self.text_resultados.insert(tk.END, f"Estudiantes reprobados (<3.0): {reprobados_total}\n")
                self.text_resultados.insert(tk.END, f"Tasa de aprobación general: {tasa_aprobacion:.1f}%\n\n")
                
                # Estadísticas por curso
                self.text_resultados.insert(tk.END, "ESTADÍSTICAS POR CURSO:\n")
                self.text_resultados.insert(tk.END, "-" * 40 + "\n")
                
                for codigo_curso, curso in modelo.cursos.items():
                    matriculas_curso = [m for m in modelo.matriculas if m[1] == codigo_curso]
                    if matriculas_curso:
                        notas_curso = [nota for _, _, nota in matriculas_curso]
                        promedio_curso = sum(notas_curso) / len(notas_curso)
                        aprobados_curso = sum(1 for nota in notas_curso if nota >= 3.0)
                        
                        self.text_resultados.insert(tk.END, f"\n{codigo_curso} - {curso.nombre}:\n")
                        self.text_resultados.insert(tk.END, f"  Estudiantes matriculados: {len(matriculas_curso)}\n")
                        self.text_resultados.insert(tk.END, f"  Promedio del curso: {promedio_curso:.2f}\n")
                        self.text_resultados.insert(tk.END, f"  Aprobados: {aprobados_curso}/{len(matriculas_curso)}\n")
                        self.text_resultados.insert(tk.END, f"  Tasa de aprobación: {(aprobados_curso/len(matriculas_curso)*100):.1f}%\n")
            else:
                self.text_resultados.insert(tk.END, "No hay matrículas registradas en el sistema.\n")
    
    def on_search(self, event):
        """Búsqueda en tiempo real de estudiantes"""
        if self.controlador:
            termino = self.entry_buscar.get()
            estudiantes = self.controlador.buscar_estudiantes(termino)
            self.actualizar_tabla_estudiantes(estudiantes)
    
    def on_filter_matriculas(self, event):
        """Filtrar matrículas por curso"""
        curso = self.entry_filtro_curso.get().strip()
        self.actualizar_tabla_matriculas(curso)
    
    def mostrar_todas_matriculas(self):
        """Mostrar todas las matrículas"""
        self.entry_filtro_curso.delete(0, tk.END)
        self.actualizar_tabla_matriculas()
    
    def cargar_csv(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV de estudiantes",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if archivo and self.controlador:
            self.controlador.cargar_csv(archivo)
            self.actualizar_kpis()
    
    def cargar_json(self):
        archivo = filedialog.askopenfilename(
            title="Cargar datos desde JSON",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        if archivo and self.controlador:
            self.controlador.cargar_json(archivo)
            self.actualizar_kpis()
    
    def guardar_json(self):
        archivo = filedialog.asksaveasfilename(
            title="Guardar como JSON",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
            defaultextension=".json"
        )
        if archivo and self.controlador:
            self.controlador.guardar_json(archivo)
    
    def mostrar_gestion_estudiantes(self):
        self.notebook.select(self.frame_estudiantes)
    
    def mostrar_gestion_cursos(self):
        self.notebook.select(self.frame_cursos)
    
    def mostrar_matriculas(self):
        self.notebook.select(self.frame_matriculas)
    
    def mostrar_reportes(self):
        self.notebook.select(self.frame_reportes)

    # ==================== MÉTODOS DE ACTUALIZACIÓN ====================
    def refrescar_tabla_estudiantes(self):
        if self.controlador:
            estudiantes = list(self.controlador.modelo.estudiantes.values())
            self.actualizar_tabla_estudiantes(estudiantes)
    
    def refrescar_tabla_cursos(self):
        if self.controlador:
            cursos = list(self.controlador.modelo.cursos.values())
            self.actualizar_tabla_cursos(cursos)
    
    def refrescar_tabla_matriculas(self):
        self.actualizar_tabla_matriculas()
    
    def refrescar_todas_las_tablas(self):
        self.refrescar_tabla_estudiantes()
        self.refrescar_tabla_cursos()
        self.refrescar_tabla_matriculas()
        self.actualizar_kpis()
    
    def actualizar_tabla_estudiantes(self, estudiantes=None):
        # Limpiar tabla
        for item in self.tree_estudiantes.get_children():
            self.tree_estudiantes.delete(item)
        
        # Agregar estudiantes
        if estudiantes is None and self.controlador:
            estudiantes = list(self.controlador.modelo.estudiantes.values())
        
        if estudiantes:
            for estudiante in estudiantes:
                self.tree_estudiantes.insert('', 'end', values=(
                    estudiante.documento,
                    estudiante.nombre,
                    estudiante.apellidos,
                    estudiante.correo,
                    estudiante.fecha_nac
                ))
    
    def actualizar_tabla_cursos(self, cursos=None):
        # Limpiar tabla
        for item in self.tree_cursos.get_children():
            self.tree_cursos.delete(item)
        
        # Agregar cursos
        if cursos is None and self.controlador:
            cursos = list(self.controlador.modelo.cursos.values())
        
        if cursos and self.controlador:
            for curso in cursos:
                # Calcular estadísticas del curso
                estudiantes_inscritos = len(curso.estudiantes)
                
                # Calcular promedio
                notas = [nota for doc, cod_curso, nota in self.controlador.modelo.matriculas if cod_curso == curso.codigo]
                promedio = sum(notas) / len(notas) if notas else 0.0
                
                self.tree_cursos.insert('', 'end', values=(
                    curso.codigo,
                    curso.nombre,
                    estudiantes_inscritos,
                    f"{promedio:.2f}"
                ))
    
    def actualizar_tabla_matriculas(self, filtro_curso=""):
        # Limpiar tabla
        for item in self.tree_matriculas.get_children():
            self.tree_matriculas.delete(item)
        
        if self.controlador:
            matriculas = self.controlador.modelo.obtener_matriculas_por_curso(filtro_curso)
            
            for documento, codigo_curso, nota in matriculas:
                estudiante = self.controlador.modelo.estudiantes.get(documento)
                curso = self.controlador.modelo.cursos.get(codigo_curso)
                
                if estudiante and curso:
                    self.tree_matriculas.insert('', 'end', values=(
                        documento,
                        f"{estudiante.nombre} {estudiante.apellidos}",
                        codigo_curso,
                        curso.nombre,
                        f"{nota:.2f}"
                    ))
    
    def actualizar_kpis(self):
        if self.controlador:
            modelo = self.controlador.modelo
            self.lbl_total_estudiantes.config(text=f"Total Estudiantes: {len(modelo.estudiantes)}")
            self.lbl_total_cursos.config(text=f"Total Cursos: {len(modelo.cursos)}")
            self.lbl_total_matriculas.config(text=f"Total Matrículas: {len(modelo.matriculas)}")
            
            # Calcular promedio general
            if modelo.matriculas:
                notas = [nota for _, _, nota in modelo.matriculas]
                promedio_general = sum(notas) / len(notas)
                self.lbl_promedio_general.config(text=f"Promedio General: {promedio_general:.2f}")
            else:
                self.lbl_promedio_general.config(text="Promedio General: 0.00")
    
    def mostrar_mensaje(self, titulo, mensaje):
        messagebox.showinfo(titulo, mensaje)
    
    def mostrar_error(self, titulo, mensaje):
        messagebox.showerror(titulo, mensaje)
    
    def establecer_controlador(self, controlador):
        self.controlador = controlador
## ==================== vista.py ====================
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from datetime import datetime


# ==================== VISTA ====================
class VistaSIGA:
    def __init__(self, root):
        self.root = root
        self.root.title("MiniSIGA - Sistema de Gestión Académica")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Controlador se asignará después
        self.controlador = None
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar peso de filas y columnas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="MiniSIGA", font=('Arial', 20, 'bold'))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Panel izquierdo - Dashboard
        self.crear_dashboard(main_frame)
        
        # Panel derecho - Contenido principal
        self.crear_panel_principal(main_frame)
        
        # Panel inferior - KPIs
        self.crear_panel_kpis(main_frame)
        
    def crear_dashboard(self, parent):
        # Frame para dashboard
        dashboard_frame = ttk.LabelFrame(parent, text="Dashboard", padding="10")
        dashboard_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W), padx=(0, 10))
        
        # Botones de navegación
        ttk.Button(dashboard_frame, text="Gestión de Estudiantes", 
                  command=self.mostrar_gestion_estudiantes).pack(fill=tk.X, pady=5)
        
        ttk.Button(dashboard_frame, text="Gestión de Cursos", 
                  command=self.mostrar_gestion_cursos).pack(fill=tk.X, pady=5)
        
        ttk.Button(dashboard_frame, text="Matrículas y Notas", 
                  command=self.mostrar_matriculas).pack(fill=tk.X, pady=5)
        
        ttk.Button(dashboard_frame, text="Consultas/Reportes", 
                  command=self.mostrar_reportes).pack(fill=tk.X, pady=5)
        
        ttk.Button(dashboard_frame, text="🤖 Predicción IA", 
                  command=self.mostrar_prediccion).pack(fill=tk.X, pady=5)
        
        ttk.Separator(dashboard_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        ttk.Button(dashboard_frame, text="Cargar CSV", 
                  command=self.cargar_csv).pack(fill=tk.X, pady=5)
        
        ttk.Button(dashboard_frame, text="Cargar JSON", 
                  command=self.cargar_json).pack(fill=tk.X, pady=5)
        
        ttk.Button(dashboard_frame, text="Guardar JSON", 
                  command=self.guardar_json).pack(fill=tk.X, pady=5)
        
    def crear_panel_principal(self, parent):
        # Notebook para pestañas
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Pestaña de gestión de estudiantes
        self.frame_estudiantes = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_estudiantes, text="Gestión de Estudiantes")
        self.crear_gestion_estudiantes()
        
        # Pestaña de gestión de cursos
        self.frame_cursos = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_cursos, text="Gestión de Cursos")
        self.crear_gestion_cursos()
        
        # Pestaña de matrículas
        self.frame_matriculas = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_matriculas, text="Matrículas y Notas")
        self.crear_matriculas()
        
        # Pestaña de reportes
        self.frame_reportes = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_reportes, text="Consultas/Reportes")
        self.crear_reportes()
        
        # Pestaña de predicción con IA
        self.frame_prediccion = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_prediccion, text="🤖 Predicción IA")
        self.crear_panel_prediccion()
        
    def crear_gestion_estudiantes(self):
        frame = self.frame_estudiantes
        
        # Formulario para nuevo estudiante
        form_frame = ttk.LabelFrame(frame, text="Nuevo Estudiante", padding="10")
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Campos del formulario
        ttk.Label(form_frame, text="Documento:").grid(row=0, column=0, sticky=tk.W)
        self.entry_documento = ttk.Entry(form_frame, width=15)
        self.entry_documento.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.entry_nombre = ttk.Entry(form_frame, width=20)
        self.entry_nombre.grid(row=0, column=3, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Apellidos:").grid(row=1, column=0, sticky=tk.W)
        self.entry_apellidos = ttk.Entry(form_frame, width=20)
        self.entry_apellidos.grid(row=1, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Correo:").grid(row=1, column=2, sticky=tk.W, padx=(10, 0))
        self.entry_correo = ttk.Entry(form_frame, width=25)
        self.entry_correo.grid(row=1, column=3, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Fecha Nac. (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W)
        self.entry_fecha = ttk.Entry(form_frame, width=15)
        self.entry_fecha.grid(row=2, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Button(form_frame, text="Crear Estudiante", 
                  command=self.btn_crear_estudiante).grid(row=2, column=2, columnspan=2, pady=10)
        
        # Configurar pesos de columnas
        for i in range(4):
            form_frame.columnconfigure(i, weight=1)
        
        # Búsqueda y controles
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(control_frame, text="Buscar:").pack(side=tk.LEFT)
        self.entry_buscar = ttk.Entry(control_frame)
        self.entry_buscar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.entry_buscar.bind('<KeyRelease>', self.on_search)
        
        ttk.Button(control_frame, text="Eliminar Seleccionado", 
                  command=self.btn_eliminar_estudiante).pack(side=tk.RIGHT, padx=5)
        
        # Tabla de estudiantes
        self.crear_tabla_estudiantes(frame)
    
    def crear_gestion_cursos(self):
        frame = self.frame_cursos
        
        # Formulario para nuevo curso
        form_frame = ttk.LabelFrame(frame, text="Nuevo Curso", padding="10")
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Código:").grid(row=0, column=0, sticky=tk.W)
        self.entry_cod_curso = ttk.Entry(form_frame, width=15)
        self.entry_cod_curso.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.entry_nom_curso = ttk.Entry(form_frame, width=30)
        self.entry_nom_curso.grid(row=0, column=3, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Button(form_frame, text="Crear Curso", 
                  command=self.btn_crear_curso).grid(row=0, column=4, padx=10)
        
        ttk.Button(form_frame, text="Eliminar Curso Seleccionado", 
                  command=self.btn_eliminar_curso).grid(row=0, column=5, padx=5)
        
        # Configurar pesos
        for i in range(6):
            form_frame.columnconfigure(i, weight=1)
        
        # Tabla de cursos
        self.crear_tabla_cursos(frame)
        
    def crear_tabla_estudiantes(self, parent):
        # Frame para tabla
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ('documento', 'nombre', 'apellidos', 'correo', 'fecha_nac')
        self.tree_estudiantes = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar encabezados
        self.tree_estudiantes.heading('documento', text='Documento')
        self.tree_estudiantes.heading('nombre', text='Nombre')
        self.tree_estudiantes.heading('apellidos', text='Apellidos')
        self.tree_estudiantes.heading('correo', text='Correo')
        self.tree_estudiantes.heading('fecha_nac', text='Fecha Nac.')
        
        # Configurar anchos de columna
        self.tree_estudiantes.column('documento', width=100)
        self.tree_estudiantes.column('nombre', width=150)
        self.tree_estudiantes.column('apellidos', width=150)
        self.tree_estudiantes.column('correo', width=200)
        self.tree_estudiantes.column('fecha_nac', width=100)
        
        # Scrollbar
        scrollbar_est = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_estudiantes.yview)
        self.tree_estudiantes.configure(yscrollcommand=scrollbar_est.set)
        
        # Empaquetar
        self.tree_estudiantes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_est.pack(side=tk.RIGHT, fill=tk.Y)
    
    def crear_tabla_cursos(self, parent):
        # Frame para tabla
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ('codigo', 'nombre', 'estudiantes', 'promedio')
        self.tree_cursos = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar encabezados
        self.tree_cursos.heading('codigo', text='Código')
        self.tree_cursos.heading('nombre', text='Nombre')
        self.tree_cursos.heading('estudiantes', text='Estudiantes')
        self.tree_cursos.heading('promedio', text='Promedio')
        
        # Configurar anchos de columna
        self.tree_cursos.column('codigo', width=100)
        self.tree_cursos.column('nombre', width=300)
        self.tree_cursos.column('estudiantes', width=100)
        self.tree_cursos.column('promedio', width=100)
        
        # Scrollbar
        scrollbar_cur = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_cursos.yview)
        self.tree_cursos.configure(yscrollcommand=scrollbar_cur.set)
        
        # Empaquetar
        self.tree_cursos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_cur.pack(side=tk.RIGHT, fill=tk.Y)
        
    def crear_matriculas(self):
        frame = self.frame_matriculas
        
        # Formulario para matrícula
        form_frame = ttk.LabelFrame(frame, text="Nueva Matrícula", padding="10")
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(form_frame, text="Documento Estudiante:").grid(row=0, column=0, sticky=tk.W)
        self.entry_doc_matricula = ttk.Entry(form_frame, width=15)
        self.entry_doc_matricula.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Código Curso:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.entry_curso = ttk.Entry(form_frame, width=15)
        self.entry_curso.grid(row=0, column=3, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(form_frame, text="Nota (0-5):").grid(row=0, column=4, sticky=tk.W, padx=(10, 0))
        self.entry_nota = ttk.Entry(form_frame, width=10)
        self.entry_nota.grid(row=0, column=5, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Button(form_frame, text="Matricular", 
                  command=self.btn_matricular).grid(row=0, column=6, padx=10)
        
        # Configurar pesos
        for i in range(7):
            form_frame.columnconfigure(i, weight=1)
        
        # Actualizar nota
        update_frame = ttk.LabelFrame(frame, text="Actualizar Nota", padding="10")
        update_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(update_frame, text="Documento:").grid(row=0, column=0, sticky=tk.W)
        self.entry_doc_update = ttk.Entry(update_frame, width=15)
        self.entry_doc_update.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(update_frame, text="Código Curso:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.entry_curso_update = ttk.Entry(update_frame, width=15)
        self.entry_curso_update.grid(row=0, column=3, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Label(update_frame, text="Nueva Nota:").grid(row=0, column=4, sticky=tk.W, padx=(10, 0))
        self.entry_nueva_nota = ttk.Entry(update_frame, width=10)
        self.entry_nueva_nota.grid(row=0, column=5, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Button(update_frame, text="Actualizar Nota", 
                  command=self.btn_actualizar_nota).grid(row=0, column=6, padx=10)
        
        # Configurar pesos
        for i in range(7):
            update_frame.columnconfigure(i, weight=1)
        
        # Filtros
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Filtrar por curso:").pack(side=tk.LEFT)
        self.entry_filtro_curso = ttk.Entry(filter_frame, width=15)
        self.entry_filtro_curso.pack(side=tk.LEFT, padx=5)
        self.entry_filtro_curso.bind('<KeyRelease>', self.on_filter_matriculas)
        
        ttk.Button(filter_frame, text="Mostrar Todas", 
                  command=self.mostrar_todas_matriculas).pack(side=tk.LEFT, padx=10)
        
        # Tabla de matrículas
        self.crear_tabla_matriculas(frame)
    
    def crear_tabla_matriculas(self, parent):
        # Frame para tabla
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview
        columns = ('documento', 'nombre_estudiante', 'codigo_curso', 'nombre_curso', 'nota')
        self.tree_matriculas = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        # Configurar encabezados
        self.tree_matriculas.heading('documento', text='Documento')
        self.tree_matriculas.heading('nombre_estudiante', text='Nombre Estudiante')
        self.tree_matriculas.heading('codigo_curso', text='Código Curso')
        self.tree_matriculas.heading('nombre_curso', text='Nombre Curso')
        self.tree_matriculas.heading('nota', text='Nota')
        
        # Configurar anchos de columna
        self.tree_matriculas.column('documento', width=100)
        self.tree_matriculas.column('nombre_estudiante', width=200)
        self.tree_matriculas.column('codigo_curso', width=100)
        self.tree_matriculas.column('nombre_curso', width=200)
        self.tree_matriculas.column('nota', width=80)
        
        # Scrollbar
        scrollbar_mat = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree_matriculas.yview)
        self.tree_matriculas.configure(yscrollcommand=scrollbar_mat.set)
        
        # Empaquetar
        self.tree_matriculas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_mat.pack(side=tk.RIGHT, fill=tk.Y)
        
    def crear_reportes(self):
        frame = self.frame_reportes
        
        # Controles de búsqueda y filtros
        control_frame = ttk.LabelFrame(frame, text="Consultas", padding="10")
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Primera fila de controles
        ttk.Label(control_frame, text="Buscar estudiante:").grid(row=0, column=0, sticky=tk.W)
        self.entry_buscar_reporte = ttk.Entry(control_frame, width=20)
        self.entry_buscar_reporte.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Button(control_frame, text="Buscar", 
                   command=self.btn_buscar_reporte).grid(row=0, column=2, padx=5)
        
        # Segunda fila de controles
        ttk.Label(control_frame, text="Código curso para reportes:").grid(row=1, column=0, sticky=tk.W)
        self.entry_curso_grafico = ttk.Entry(control_frame, width=15)
        self.entry_curso_grafico.grid(row=1, column=1, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Button(control_frame, text="Top 3 Estudiantes", 
                   command=self.btn_top_estudiantes).grid(row=1, column=2, padx=5)
        
        ttk.Button(control_frame, text="Gráfico Aprobados/Reprobados", 
                   command=self.btn_grafico_aprobados).grid(row=1, column=3, padx=5)
        
        # Nueva fila para exportar reportes
        export_frame = ttk.Frame(control_frame)
        export_frame.grid(row=2, column=0, columnspan=4, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Label(export_frame, text="Exportar reporte:").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(export_frame, text="📄 Reporte Simple (PDF)", 
                   command=self.btn_exportar_pdf_simple).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(export_frame, text="📊 Reporte Completo (PDF)", 
                   command=self.btn_exportar_pdf_completo).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(export_frame, text="📑 Exportar CSV", 
                   command=self.btn_exportar_csv).pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="Estadísticas Generales", 
                   command=self.btn_estadisticas_generales).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Área de resultados
        results_frame = ttk.LabelFrame(frame, text="Resultados", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.text_resultados = tk.Text(results_frame, height=20, wrap=tk.WORD)
        
        # Scrollbar para texto
        scrollbar_text = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.text_resultados.yview)
        self.text_resultados.configure(yscrollcommand=scrollbar_text.set)
        
        # Empaquetar texto y scrollbar
        self.text_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_text.pack(side=tk.RIGHT, fill=tk.Y)

    # ==================== PANEL DE PREDICCIÓN IA ====================
    def crear_panel_prediccion(self):
        """Crea la pestaña de predicciones con IA"""
        frame = self.frame_prediccion
        
        # ==================== SECCIÓN DE ENTRENAMIENTO ====================
        training_frame = ttk.LabelFrame(frame, text="🎓 Entrenamiento del Modelo", padding="15")
        training_frame.pack(fill=tk.X, padx=10, pady=10)
        
        info_label = ttk.Label(
            training_frame,
            text="El modelo de IA aprende de los datos históricos para predecir el rendimiento académico.",
            wraplength=800,
            justify=tk.LEFT
        )
        info_label.pack(pady=5)
        
        button_frame = ttk.Frame(training_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(
            button_frame,
            text="🚀 Entrenar Modelo",
            command=self.btn_entrenar_modelo,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="📁 Cargar Modelo",
            command=self.btn_cargar_modelo,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        # ==================== SECCIÓN DE PREDICCIÓN INDIVIDUAL ====================
        pred_frame = ttk.LabelFrame(frame, text="🔮 Predicción Individual", padding="15")
        pred_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Primera fila
        row1 = ttk.Frame(pred_frame)
        row1.pack(fill=tk.X, pady=5)
        
        ttk.Label(row1, text="Documento Estudiante:").pack(side=tk.LEFT, padx=5)
        self.entry_pred_documento = ttk.Entry(row1, width=15)
        self.entry_pred_documento.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row1, text="Código Curso:").pack(side=tk.LEFT, padx=(20, 5))
        self.entry_pred_curso = ttk.Entry(row1, width=15)
        self.entry_pred_curso.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            row1,
            text="🎯 Predecir",
            command=self.btn_predecir_individual
        ).pack(side=tk.LEFT, padx=10)
        
        # Segunda fila - Predicción de todos los cursos
        row2 = ttk.Frame(pred_frame)
        row2.pack(fill=tk.X, pady=5)
        
        ttk.Label(row2, text="Documento Estudiante:").pack(side=tk.LEFT, padx=5)
        self.entry_pred_batch = ttk.Entry(row2, width=15)
        self.entry_pred_batch.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            row2,
            text="📊 Predecir Todos los Cursos",
            command=self.btn_predecir_batch
        ).pack(side=tk.LEFT, padx=10)
        
        # ==================== SECCIÓN DE ANÁLISIS ====================
        analysis_frame = ttk.LabelFrame(frame, text="📈 Análisis Avanzado", padding="15")
        analysis_frame.pack(fill=tk.X, padx=10, pady=10)
        
        btn_row = ttk.Frame(analysis_frame)
        btn_row.pack(pady=5)
        
        ttk.Button(
            btn_row,
            text="⚠️ Estudiantes en Riesgo",
            command=self.btn_estudiantes_riesgo,
            width=25
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_row,
            text="💡 Recomendar Cursos",
            command=self.btn_recomendar_cursos,
            width=25
        ).pack(side=tk.LEFT, padx=5)
        
        # Para recomendaciones
        rec_row = ttk.Frame(analysis_frame)
        rec_row.pack(pady=5)
        
        ttk.Label(rec_row, text="Documento para recomendaciones:").pack(side=tk.LEFT, padx=5)
        self.entry_rec_documento = ttk.Entry(rec_row, width=15)
        self.entry_rec_documento.pack(side=tk.LEFT, padx=5)
        
        # ==================== ÁREA DE RESULTADOS ====================
        results_frame = ttk.LabelFrame(frame, text="📋 Resultados de Predicción", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Texto con scrollbar
        self.text_prediccion = tk.Text(results_frame, height=20, wrap=tk.WORD, font=('Consolas', 10))
        scrollbar_pred = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.text_prediccion.yview)
        self.text_prediccion.configure(yscrollcommand=scrollbar_pred.set)
        
        self.text_prediccion.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_pred.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar tags para colores
        self.text_prediccion.tag_config('exito', foreground='#27ae60', font=('Consolas', 10, 'bold'))
        self.text_prediccion.tag_config('riesgo', foreground='#e74c3c', font=('Consolas', 10, 'bold'))
        self.text_prediccion.tag_config('advertencia', foreground='#f39c12', font=('Consolas', 10, 'bold'))
        self.text_prediccion.tag_config('titulo', foreground='#2c3e50', font=('Consolas', 12, 'bold'))
        self.text_prediccion.tag_config('subtitulo', foreground='#34495e', font=('Consolas', 11, 'bold'))

    # ==================== MÉTODOS DE EXPORTACIÓN ====================
    def btn_exportar_pdf_simple(self):
        """Exporta un reporte simple en PDF con solo la tabla de estudiantes"""
        if self.controlador:
            df = self.controlador.generar_reporte_estudiantes()
            if df.empty:
                self.mostrar_error("Error", "No hay datos para exportar.")
                return
            archivo = filedialog.asksaveasfilename(
                title="Guardar reporte simple en PDF",
                filetypes=[("Archivo PDF", "*.pdf")],
                defaultextension=".pdf",
                initialfile=f"Reporte_Simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            if archivo:
                try:
                    from utils import exportar_pdf
                    exportar_pdf(archivo, df)
                    self.mostrar_mensaje("Éxito", "Reporte simple exportado correctamente.")
                except Exception as e:
                    self.mostrar_error("Error", f"Error al exportar:\n{str(e)}")

    def btn_exportar_pdf_completo(self):
        """Exporta un reporte completo en PDF con top 3 y gráficas"""
        if self.controlador:
            if not self.controlador.modelo.estudiantes:
                self.mostrar_error("Error", "No hay datos para exportar.")
                return
            
            archivo = filedialog.asksaveasfilename(
                title="Guardar reporte completo en PDF",
                filetypes=[("Archivo PDF", "*.pdf")],
                defaultextension=".pdf",
                initialfile=f"Reporte_Completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            
            if archivo:
                try:
                    from utils import exportar_pdf_completo
                    
                    # Ventana de progreso
                    ventana_progreso = tk.Toplevel(self.root)
                    ventana_progreso.title("Generando reporte...")
                    ventana_progreso.geometry("400x150")
                    ventana_progreso.transient(self.root)
                    ventana_progreso.grab_set()
                    
                    # Centrar ventana
                    ventana_progreso.update_idletasks()
                    x = (ventana_progreso.winfo_screenwidth() // 2) - (400 // 2)
                    y = (ventana_progreso.winfo_screenheight() // 2) - (150 // 2)
                    ventana_progreso.geometry(f"400x150+{x}+{y}")
                    
                    frame_progreso = ttk.Frame(ventana_progreso, padding="20")
                    frame_progreso.pack(fill=tk.BOTH, expand=True)
                    
                    ttk.Label(frame_progreso, 
                             text="Generando reporte completo...", 
                             font=('Arial', 12, 'bold')).pack(pady=10)
                    ttk.Label(frame_progreso, 
                             text="Esto puede tardar unos momentos.\nGenerando gráficas y tablas...",
                             justify=tk.CENTER).pack(pady=10)
                    
                    progress = ttk.Progressbar(frame_progreso, mode='indeterminate', length=300)
                    progress.pack(pady=10)
                    progress.start(10)
                    
                    ventana_progreso.update()
                    
                    # Generar reporte
                    exportar_pdf_completo(archivo, self.controlador)
                    
                    progress.stop()
                    ventana_progreso.destroy()
                    
                    self.mostrar_mensaje("Éxito", 
                        f"✅ Reporte completo exportado exitosamente.\n\n"
                        f"📋 El reporte incluye:\n"
                        f"  • Estadísticas generales\n"
                        f"  • Listado completo de estudiantes\n"
                        f"  • Top 3 estudiantes por curso\n"
                        f"  • Gráficas estadísticas de cada curso\n\n"
                        f"📁 Archivo: {os.path.basename(archivo)}")
                    
                except Exception as e:
                    if 'ventana_progreso' in locals():
                        ventana_progreso.destroy()
                    self.mostrar_error("Error", f"Error al generar el reporte:\n{str(e)}")

    def btn_exportar_csv(self):
        """Exporta el reporte a CSV"""
        if self.controlador:
            df = self.controlador.generar_reporte_estudiantes()
            if df.empty:
                self.mostrar_error("Error", "No hay datos para exportar.")
                return
            archivo = filedialog.asksaveasfilename(
                title="Guardar reporte en CSV",
                filetypes=[("Archivos CSV", "*.csv")],
                defaultextension=".csv",
                initialfile=f"Reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            if archivo:
                try:
                    df.to_csv(archivo, index=False, encoding="utf-8-sig")
                    self.mostrar_mensaje("Éxito", "Reporte exportado en CSV correctamente.")
                except Exception as e:
                    self.mostrar_error("Error", f"Error al exportar CSV:\n{str(e)}")
        
    def crear_panel_kpis(self, parent):
        kpi_frame = ttk.LabelFrame(parent, text="Estadísticas Generales", padding="10")
        kpi_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.lbl_total_estudiantes = ttk.Label(kpi_frame, text="Total Estudiantes: 0", font=('Arial', 12, 'bold'))
        self.lbl_total_estudiantes.grid(row=0, column=0, padx=20)
        
        self.lbl_total_cursos = ttk.Label(kpi_frame, text="Total Cursos: 0", font=('Arial', 12, 'bold'))
        self.lbl_total_cursos.grid(row=0, column=1, padx=20)
        
        self.lbl_total_matriculas = ttk.Label(kpi_frame, text="Total Matrículas: 0", font=('Arial', 12, 'bold'))
        self.lbl_total_matriculas.grid(row=0, column=2, padx=20)
        
        self.lbl_promedio_general = ttk.Label(kpi_frame, text="Promedio General: 0.00", font=('Arial', 12, 'bold'))
        self.lbl_promedio_general.grid(row=0, column=3, padx=20)

    # ==================== MÉTODOS DE EVENTOS ====================
    def btn_crear_estudiante(self):
        if self.controlador:
            documento = self.entry_documento.get().strip()
            nombre = self.entry_nombre.get().strip()
            apellidos = self.entry_apellidos.get().strip()
            correo = self.entry_correo.get().strip()
            fecha = self.entry_fecha.get().strip()
            
            if self.controlador.crear_estudiante(documento, nombre, apellidos, correo, fecha):
                # Limpiar campos
                self.entry_documento.delete(0, tk.END)
                self.entry_nombre.delete(0, tk.END)
                self.entry_apellidos.delete(0, tk.END)
                self.entry_correo.delete(0, tk.END)
                self.entry_fecha.delete(0, tk.END)
                self.actualizar_kpis()
    
    def btn_crear_curso(self):
        if self.controlador:
            codigo = self.entry_cod_curso.get().strip()
            nombre = self.entry_nom_curso.get().strip()
            
            if self.controlador.crear_curso(codigo, nombre):
                self.entry_cod_curso.delete(0, tk.END)
                self.entry_nom_curso.delete(0, tk.END)
                self.actualizar_kpis()
    
    def btn_matricular(self):
        if self.controlador:
            documento = self.entry_doc_matricula.get().strip()
            curso = self.entry_curso.get().strip()
            nota = self.entry_nota.get().strip()
            
            if self.controlador.matricular_estudiante(documento, curso, nota):
                self.entry_doc_matricula.delete(0, tk.END)
                self.entry_curso.delete(0, tk.END)
                self.entry_nota.delete(0, tk.END)
                self.actualizar_kpis()
    
    def btn_actualizar_nota(self):
        if self.controlador:
            documento = self.entry_doc_update.get().strip()
            curso = self.entry_curso_update.get().strip()
            nueva_nota = self.entry_nueva_nota.get().strip()
            
            if self.controlador.actualizar_nota(documento, curso, nueva_nota):
                self.entry_doc_update.delete(0, tk.END)
                self.entry_curso_update.delete(0, tk.END)
                self.entry_nueva_nota.delete(0, tk.END)
                self.actualizar_kpis()
    
    def btn_eliminar_estudiante(self):
        selected = self.tree_estudiantes.selection()
        if selected and self.controlador:
            item = self.tree_estudiantes.item(selected[0])
            documento = item['values'][0]
            
            if messagebox.askyesno("Confirmar", f"¿Eliminar estudiante con documento {documento}?"):
                self.controlador.eliminar_estudiante(documento)
                self.actualizar_kpis()
    
    def btn_eliminar_curso(self):
        selected = self.tree_cursos.selection()
        if selected and self.controlador:
            item = self.tree_cursos.item(selected[0])
            codigo_curso = item['values'][0]
            
            if messagebox.askyesno("Confirmar", f"¿Eliminar curso {codigo_curso}?"):
                self.controlador.eliminar_curso(codigo_curso)
                self.actualizar_kpis()
    
    def btn_buscar_reporte(self):
        if self.controlador:
            termino = self.entry_buscar_reporte.get().strip()
            estudiantes = self.controlador.buscar_estudiantes(termino)
            
            self.text_resultados.delete(1.0, tk.END)
            self.text_resultados.insert(tk.END, f"Resultados de búsqueda para: '{termino}'\n")
            self.text_resultados.insert(tk.END, "="*60 + "\n\n")
            
            if estudiantes:
                for est in estudiantes:
                    self.text_resultados.insert(tk.END, f"Documento: {est.documento}\n")
                    self.text_resultados.insert(tk.END, f"Nombre: {est.nombre} {est.apellidos}\n")
                    self.text_resultados.insert(tk.END, f"Correo: {est.correo}\n")
                    self.text_resultados.insert(tk.END, f"Fecha Nacimiento: {est.fecha_nac}\n")
                    self.text_resultados.insert(tk.END, f"Cursos matriculados: {len(est.cursos)}\n")
                    
                    if est.cursos:
                        self.text_resultados.insert(tk.END, "Detalle de cursos y notas:\n")
                        for curso_cod in est.cursos:
                            curso_nombre = self.controlador.modelo.cursos.get(curso_cod, {}).nombre if curso_cod in self.controlador.modelo.cursos else "N/A"
                            nota = est.notas.get(curso_cod, 0.0)
                            estado = "APROBADO" if nota >= 3.0 else "REPROBADO"
                            self.text_resultados.insert(tk.END, f"  - {curso_cod} ({curso_nombre}): {nota} - {estado}\n")
                    
                    self.text_resultados.insert(tk.END, "-"*40 + "\n\n")
            else:
                self.text_resultados.insert(tk.END, "No se encontraron estudiantes con ese criterio.\n")
    
    def btn_top_estudiantes(self):
        if self.controlador:
            curso = self.entry_curso_grafico.get().strip()
            if not curso:
                self.mostrar_error("Error", "Por favor ingrese un código de curso")
                return
                
            top_estudiantes = self.controlador.modelo.obtener_top_estudiantes(curso)
            
            self.text_resultados.delete(1.0, tk.END)
            self.text_resultados.insert(tk.END, f"Top 3 estudiantes en el curso: {curso}\n")
            self.text_resultados.insert(tk.END, "="*60 + "\n\n")
            
            if top_estudiantes:
                curso_nombre = self.controlador.modelo.cursos.get(curso, {}).nombre if curso in self.controlador.modelo.cursos else "N/A"
                self.text_resultados.insert(tk.END, f"Curso: {curso} - {curso_nombre}\n\n")
                
                for i, (estudiante, nota) in enumerate(top_estudiantes, 1):
                    self.text_resultados.insert(tk.END, f"{i}. {estudiante.nombre} {estudiante.apellidos}\n")
                    self.text_resultados.insert(tk.END, f"   Documento: {estudiante.documento}\n")
                    self.text_resultados.insert(tk.END, f"   Correo: {estudiante.correo}\n")
                    self.text_resultados.insert(tk.END, f"   Nota: {nota:.2f}\n")
                    self.text_resultados.insert(tk.END, f"   Estado: {'APROBADO' if nota >= 3.0 else 'REPROBADO'}\n\n")
            else:
                self.text_resultados.insert(tk.END, f"No hay estudiantes matriculados en el curso {curso}.\n")
    
    def btn_grafico_aprobados(self):
        if self.controlador:
            curso = self.entry_curso_grafico.get().strip()
            if not curso:
                self.mostrar_error("Error", "Por favor ingrese un código de curso")
                return
                
            aprobados, reprobados = self.controlador.modelo.obtener_estadisticas_aprobados(curso)
            
            if aprobados == 0 and reprobados == 0:
                self.mostrar_error("Error", f"No hay estudiantes matriculados en el curso {curso}")
                return
            
            # Crear ventana para gráfico
            ventana_grafico = tk.Toplevel(self.root)
            ventana_grafico.title(f"Estadísticas del curso: {curso}")
            ventana_grafico.geometry("700x500")
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            
            # Gráfico de barras
            categorias = ['Aprobados\n(≥ 3.0)', 'Reprobados\n(< 3.0)']
            valores = [aprobados, reprobados]
            colores = ['#2ecc71', '#e74c3c']
            
            bars = ax1.bar(categorias, valores, color=colores, alpha=0.8, edgecolor='black')
            ax1.set_title(f'Distribución Aprobados/Reprobados\nCurso: {curso}', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Cantidad de Estudiantes', fontsize=12)
            ax1.grid(axis='y', alpha=0.3)
            
            # Agregar valores en las barras
            for bar, valor in zip(bars, valores):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{valor}', ha='center', va='bottom', fontweight='bold', fontsize=12)
            
            # Gráfico de torta
            if aprobados + reprobados > 0:
                sizes = [aprobados, reprobados]
                labels = [f'Aprobados\n({aprobados})', f'Reprobados\n({reprobados})']
                colors = ['#2ecc71', '#e74c3c']
                explode = (0.05, 0.05)
                
                wedges, texts, autotexts = ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                                  startangle=90, explode=explode, shadow=True)
                ax2.set_title(f'Proporción de Estudiantes\nCurso: {curso}', fontsize=14, fontweight='bold')
                
                # Mejorar el formato del texto
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, ventana_grafico)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Agregar información adicional
            info_frame = ttk.Frame(ventana_grafico)
            info_frame.pack(fill=tk.X, padx=10, pady=5)
            
            total = aprobados + reprobados
            porcentaje_aprobacion = (aprobados / total * 100) if total > 0 else 0
            
            info_text = f"Total estudiantes: {total} | Tasa de aprobación: {porcentaje_aprobacion:.1f}%"
            ttk.Label(info_frame, text=info_text, font=('Arial', 10, 'bold')).pack()
    
    def btn_estadisticas_generales(self):
        if self.controlador:
            modelo = self.controlador.modelo
            
            self.text_resultados.delete(1.0, tk.END)
            self.text_resultados.insert(tk.END, "ESTADÍSTICAS GENERALES DEL SISTEMA\n")
            self.text_resultados.insert(tk.END, "="*60 + "\n\n")
            
            # Estadísticas básicas
            total_estudiantes = len(modelo.estudiantes)
            total_cursos = len(modelo.cursos)
            total_matriculas = len(modelo.matriculas)
            
            self.text_resultados.insert(tk.END, f"Total de estudiantes: {total_estudiantes}\n")
            self.text_resultados.insert(tk.END, f"Total de cursos: {total_cursos}\n")
            self.text_resultados.insert(tk.END, f"Total de matrículas: {total_matriculas}\n\n")
            
            if total_matriculas > 0:
                # Promedio general
                notas = [nota for _, _, nota in modelo.matriculas]
                promedio_general = sum(notas) / len(notas)
                self.text_resultados.insert(tk.END, f"Promedio general: {promedio_general:.2f}\n")
                
                # Distribución de notas
                aprobados_total = sum(1 for nota in notas if nota >= 3.0)
                reprobados_total = len(notas) - aprobados_total
                tasa_aprobacion = (aprobados_total / len(notas)) * 100
                
                self.text_resultados.insert(tk.END, f"Estudiantes aprobados (≥3.0): {aprobados_total}\n")
                self.text_resultados.insert(tk.END, f"Estudiantes reprobados (<3.0): {reprobados_total}\n")
                self.text_resultados.insert(tk.END, f"Tasa de aprobación general: {tasa_aprobacion:.1f}%\n\n")
                
                # Estadísticas por curso
                self.text_resultados.insert(tk.END, "ESTADÍSTICAS POR CURSO:\n")
                self.text_resultados.insert(tk.END, "-" * 40 + "\n")
                
                for codigo_curso, curso in modelo.cursos.items():
                    matriculas_curso = [m for m in modelo.matriculas if m[1] == codigo_curso]
                    if matriculas_curso:
                        notas_curso = [nota for _, _, nota in matriculas_curso]
                        promedio_curso = sum(notas_curso) / len(notas_curso)
                        aprobados_curso = sum(1 for nota in notas_curso if nota >= 3.0)
                        
                        self.text_resultados.insert(tk.END, f"\n{codigo_curso} - {curso.nombre}:\n")
                        self.text_resultados.insert(tk.END, f"  Estudiantes matriculados: {len(matriculas_curso)}\n")
                        self.text_resultados.insert(tk.END, f"  Promedio del curso: {promedio_curso:.2f}\n")
                        self.text_resultados.insert(tk.END, f"  Aprobados: {aprobados_curso}/{len(matriculas_curso)}\n")
                        self.text_resultados.insert(tk.END, f"  Tasa de aprobación: {(aprobados_curso/len(matriculas_curso)*100):.1f}%\n")
            else:
                self.text_resultados.insert(tk.END, "No hay matrículas registradas en el sistema.\n")
    
    def on_search(self, event):
        """Búsqueda en tiempo real de estudiantes"""
        if self.controlador:
            termino = self.entry_buscar.get()
            estudiantes = self.controlador.buscar_estudiantes(termino)
            self.actualizar_tabla_estudiantes(estudiantes)
    
    def on_filter_matriculas(self, event):
        """Filtrar matrículas por curso"""
        curso = self.entry_filtro_curso.get().strip()
        self.actualizar_tabla_matriculas(curso)
    
    def mostrar_todas_matriculas(self):
        """Mostrar todas las matrículas"""
        self.entry_filtro_curso.delete(0, tk.END)
        self.actualizar_tabla_matriculas()
    
    def cargar_csv(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV de estudiantes",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if archivo and self.controlador:
            self.controlador.cargar_csv(archivo)
            self.actualizar_kpis()
    
    def cargar_json(self):
        archivo = filedialog.askopenfilename(
            title="Cargar datos desde JSON",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        if archivo and self.controlador:
            self.controlador.cargar_json(archivo)
            self.actualizar_kpis()
    
    def guardar_json(self):
        archivo = filedialog.asksaveasfilename(
            title="Guardar como JSON",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
            defaultextension=".json"
        )
        if archivo and self.controlador:
            self.controlador.guardar_json(archivo)

    # ==================== MÉTODOS DE NAVEGACIÓN ====================
    def mostrar_gestion_estudiantes(self):
        """Muestra la pestaña de gestión de estudiantes"""
        self.notebook.select(self.frame_estudiantes)
    
    def mostrar_gestion_cursos(self):
        """Muestra la pestaña de gestión de cursos"""
        self.notebook.select(self.frame_cursos)
    
    def mostrar_matriculas(self):
        """Muestra la pestaña de matrículas y notas"""
        self.notebook.select(self.frame_matriculas)
    
    def mostrar_reportes(self):
        """Muestra la pestaña de reportes"""
        self.notebook.select(self.frame_reportes)
    
    def mostrar_prediccion(self):
        """Muestra la pestaña de predicción IA"""
        if hasattr(self, 'frame_prediccion'):
            self.notebook.select(self.frame_prediccion)

    # ==================== MÉTODOS DE ACTUALIZACIÓN ====================
    def refrescar_tabla_estudiantes(self):
        if self.controlador:
            estudiantes = list(self.controlador.modelo.estudiantes.values())
            self.actualizar_tabla_estudiantes(estudiantes)
    
    def refrescar_tabla_cursos(self):
        if self.controlador:
            cursos = list(self.controlador.modelo.cursos.values())
            self.actualizar_tabla_cursos(cursos)
    
    def refrescar_tabla_matriculas(self):
        self.actualizar_tabla_matriculas()
    
    def refrescar_todas_las_tablas(self):
        self.refrescar_tabla_estudiantes()
        self.refrescar_tabla_cursos()
        self.refrescar_tabla_matriculas()
        self.actualizar_kpis()
    
    def actualizar_tabla_estudiantes(self, estudiantes=None):
        # Limpiar tabla
        for item in self.tree_estudiantes.get_children():
            self.tree_estudiantes.delete(item)
        
        # Agregar estudiantes
        if estudiantes is None and self.controlador:
            estudiantes = list(self.controlador.modelo.estudiantes.values())
        
        if estudiantes:
            for estudiante in estudiantes:
                self.tree_estudiantes.insert('', 'end', values=(
                    estudiante.documento,
                    estudiante.nombre,
                    estudiante.apellidos,
                    estudiante.correo,
                    estudiante.fecha_nac
                ))
    
    def actualizar_tabla_cursos(self, cursos=None):
        # Limpiar tabla
        for item in self.tree_cursos.get_children():
            self.tree_cursos.delete(item)
        
        # Agregar cursos
        if cursos is None and self.controlador:
            cursos = list(self.controlador.modelo.cursos.values())
        
        if cursos and self.controlador:
            for curso in cursos:
                # Calcular estadísticas del curso
                estudiantes_inscritos = len(curso.estudiantes)
                
                # Calcular promedio
                notas = [nota for doc, cod_curso, nota in self.controlador.modelo.matriculas if cod_curso == curso.codigo]
                promedio = sum(notas) / len(notas) if notas else 0.0
                
                self.tree_cursos.insert('', 'end', values=(
                    curso.codigo,
                    curso.nombre,
                    estudiantes_inscritos,
                    f"{promedio:.2f}"
                ))
    
    def actualizar_tabla_matriculas(self, filtro_curso=""):
        # Limpiar tabla
        for item in self.tree_matriculas.get_children():
            self.tree_matriculas.delete(item)
        
        if self.controlador:
            matriculas = self.controlador.modelo.obtener_matriculas_por_curso(filtro_curso)
            
            for documento, codigo_curso, nota in matriculas:
                estudiante = self.controlador.modelo.estudiantes.get(documento)
                curso = self.controlador.modelo.cursos.get(codigo_curso)
                
                if estudiante and curso:
                    self.tree_matriculas.insert('', 'end', values=(
                        documento,
                        f"{estudiante.nombre} {estudiante.apellidos}",
                        codigo_curso,
                        curso.nombre,
                        f"{nota:.2f}"
                    ))
    
    def actualizar_kpis(self):
        if self.controlador:
            modelo = self.controlador.modelo
            self.lbl_total_estudiantes.config(text=f"Total Estudiantes: {len(modelo.estudiantes)}")
            self.lbl_total_cursos.config(text=f"Total Cursos: {len(modelo.cursos)}")
            self.lbl_total_matriculas.config(text=f"Total Matrículas: {len(modelo.matriculas)}")
            
            # Calcular promedio general
            if modelo.matriculas:
                notas = [nota for _, _, nota in modelo.matriculas]
                promedio_general = sum(notas) / len(notas)
                self.lbl_promedio_general.config(text=f"Promedio General: {promedio_general:.2f}")
            else:
                self.lbl_promedio_general.config(text="Promedio General: 0.00")
    
    def mostrar_mensaje(self, titulo, mensaje):
        messagebox.showinfo(titulo, mensaje)
    
    def mostrar_error(self, titulo, mensaje):
        messagebox.showerror(titulo, mensaje)
    
    def establecer_controlador(self, controlador):
        self.controlador = controlador
        self.actualizar_kpis()

    # ==================== MÉTODOS DE EVENTOS PARA PREDICCIÓN ====================
# ==================== MÉTODOS DE EVENTOS PARA PREDICCIÓN IA ====================
    
    def btn_entrenar_modelo(self):
        """Entrena el modelo de predicción con IA"""
        if self.controlador:
            # Ventana de confirmación
            respuesta = messagebox.askyesno(
                "Entrenar Modelo",
                "¿Desea entrenar un nuevo modelo de predicción?\n\n"
                "Este proceso puede tardar unos minutos y utilizará\n"
                "todos los datos actuales del sistema.\n\n"
                f"Matrículas disponibles: {len(self.controlador.modelo.matriculas)}"
            )
            
            if respuesta:
                # Ventana de progreso
                ventana_progreso = tk.Toplevel(self.root)
                ventana_progreso.title("Entrenando Modelo...")
                ventana_progreso.geometry("400x200")
                ventana_progreso.transient(self.root)
                ventana_progreso.grab_set()
                
                # Centrar ventana
                ventana_progreso.update_idletasks()
                x = (ventana_progreso.winfo_screenwidth() // 2) - 200
                y = (ventana_progreso.winfo_screenheight() // 2) - 100
                ventana_progreso.geometry(f"400x200+{x}+{y}")
                
                frame = ttk.Frame(ventana_progreso, padding="20")
                frame.pack(fill=tk.BOTH, expand=True)
                
                ttk.Label(
                    frame,
                    text="🤖 Entrenando Red Neuronal...",
                    font=('Arial', 14, 'bold')
                ).pack(pady=10)
                
                ttk.Label(
                    frame,
                    text="Procesando datos históricos\ny optimizando parámetros...",
                    justify=tk.CENTER
                ).pack(pady=10)
                
                progress = ttk.Progressbar(frame, mode='indeterminate', length=300)
                progress.pack(pady=20)
                progress.start(10)
                
                ventana_progreso.update()
                
                # Entrenar modelo
                exito = self.controlador.entrenar_modelo_prediccion()
                
                progress.stop()
                ventana_progreso.destroy()
                
                if exito:
                    self.mostrar_mensaje(
                        "Éxito",
                        "✅ Modelo entrenado exitosamente\n\n"
                        "El modelo está listo para realizar predicciones."
                    )
                else:
                    self.mostrar_error(
                        "Error",
                        "No se pudo entrenar el modelo.\n"
                        "Verifique que haya suficientes datos (mínimo 10 matrículas)."
                    )

    def btn_cargar_modelo(self):
        """Carga un modelo previamente entrenado"""
        if self.controlador:
            archivo = filedialog.askopenfilename(
                title="Cargar modelo entrenado",
                filetypes=[
                    ("Modelo TensorFlow", "*.h5"),
                    ("Todos los archivos", "*.*")
                ]
            )
            if archivo:
                exito = self.controlador.cargar_modelo_prediccion(archivo)
                if exito:
                    self.mostrar_mensaje(
                        "Éxito",
                        "✅ Modelo cargado correctamente"
                    )
                else:
                    self.mostrar_error(
                        "Error",
                        "No se pudo cargar el modelo"
                    )

    def btn_predecir_individual(self):
        """Realiza una predicción individual para un estudiante en un curso"""
        if not self.controlador:
            return
        
        documento = self.entry_pred_documento.get().strip()
        codigo_curso = self.entry_pred_curso.get().strip()
        
        if not documento or not codigo_curso:
            self.mostrar_error("Error", "Debe ingresar documento y código de curso")
            return
        
        resultado = self.controlador.predecir_estudiante(documento, codigo_curso)
        
        if resultado:
            self._mostrar_resultado_prediccion_individual(documento, codigo_curso, resultado)

    def _mostrar_resultado_prediccion_individual(self, documento, codigo_curso, resultado):
        """Muestra el resultado de una predicción individual en el área de texto"""
        self.text_prediccion.delete(1.0, tk.END)
        
        # Obtener datos del estudiante
        estudiante = self.controlador.modelo.estudiantes.get(documento)
        curso = self.controlador.modelo.cursos.get(codigo_curso)
        
        # Título
        self.text_prediccion.insert(tk.END, "🎯 PREDICCIÓN INDIVIDUAL\n", 'titulo')
        self.text_prediccion.insert(tk.END, "="*70 + "\n\n")
        
        # Datos del estudiante
        self.text_prediccion.insert(tk.END, "👤 ESTUDIANTE:\n", 'subtitulo')
        self.text_prediccion.insert(tk.END, f"   Documento: {documento}\n")
        self.text_prediccion.insert(tk.END, f"   Nombre: {estudiante.nombre} {estudiante.apellidos}\n")
        self.text_prediccion.insert(tk.END, f"   Correo: {estudiante.correo}\n\n")
        
        # Datos del curso
        self.text_prediccion.insert(tk.END, "📚 CURSO:\n", 'subtitulo')
        self.text_prediccion.insert(tk.END, f"   Código: {codigo_curso}\n")
        self.text_prediccion.insert(tk.END, f"   Nombre: {curso.nombre}\n\n")
        
        # Resultado de la predicción
        self.text_prediccion.insert(tk.END, "🔮 RESULTADO DE LA PREDICCIÓN:\n", 'subtitulo')
        self.text_prediccion.insert(tk.END, "-"*70 + "\n")
        
        prediccion = resultado['prediccion']
        probabilidad = resultado['probabilidad_aprobar'] * 100
        confianza = resultado['confianza'] * 100
        
        # Colorear según la predicción
        if prediccion == "APROBARÁ":
            self.text_prediccion.insert(tk.END, f"   Estado Predicho: {prediccion} ✅\n", 'exito')
        else:
            self.text_prediccion.insert(tk.END, f"   Estado Predicho: {prediccion} ❌\n", 'riesgo')
        
        self.text_prediccion.insert(tk.END, f"   Probabilidad de Aprobar: {probabilidad:.2f}%\n")
        self.text_prediccion.insert(tk.END, f"   Confianza del Modelo: {confianza:.2f}%\n\n")
        
        # Features utilizadas
        self.text_prediccion.insert(tk.END, "📊 FACTORES ANALIZADOS:\n", 'subtitulo')
        features = resultado['features']
        self.text_prediccion.insert(tk.END, f"   • Promedio del Estudiante: {features['promedio_estudiante']:.2f}\n")
        self.text_prediccion.insert(tk.END, f"   • Cursos Matriculados: {features['num_cursos']}\n")
        self.text_prediccion.insert(tk.END, f"   • Promedio del Curso: {features['promedio_curso']:.2f}\n")
        self.text_prediccion.insert(tk.END, f"   • Tasa de Aprobación del Curso: {features['tasa_aprobacion_curso']*100:.1f}%\n\n")
        
        # Recomendaciones
        self.text_prediccion.insert(tk.END, "💡 RECOMENDACIONES:\n", 'subtitulo')
        if probabilidad < 50:
            self.text_prediccion.insert(tk.END, "   ⚠️  ALTO RIESGO DE REPROBAR\n", 'riesgo')
            self.text_prediccion.insert(tk.END, "   • Considere tutorías adicionales\n")
            self.text_prediccion.insert(tk.END, "   • Revise los horarios de estudio\n")
            self.text_prediccion.insert(tk.END, "   • Busque apoyo del profesor\n")
        elif probabilidad < 70:
            self.text_prediccion.insert(tk.END, "   ⚠️  RIESGO MODERADO\n", 'advertencia')
            self.text_prediccion.insert(tk.END, "   • Mantenga un estudio constante\n")
            self.text_prediccion.insert(tk.END, "   • Participe activamente en clase\n")
        else:
            self.text_prediccion.insert(tk.END, "   ✅ BUEN PRONÓSTICO\n", 'exito')
            self.text_prediccion.insert(tk.END, "   • Continúe con el buen trabajo\n")
            self.text_prediccion.insert(tk.END, "   • Mantenga el ritmo de estudio\n")

    def btn_predecir_batch(self):
        """Predice el rendimiento en todos los cursos de un estudiante"""
        if not self.controlador:
            return
        
        documento = self.entry_pred_batch.get().strip()
        
        if not documento:
            self.mostrar_error("Error", "Debe ingresar un documento de estudiante")
            return
        
        predicciones = self.controlador.predecir_todos_cursos_estudiante(documento)
        
        if predicciones:
            self._mostrar_resultados_batch(documento, predicciones)

    def _mostrar_resultados_batch(self, documento, predicciones):
        """Muestra los resultados de predicción de todos los cursos"""
        self.text_prediccion.delete(1.0, tk.END)
        
        estudiante = self.controlador.modelo.estudiantes.get(documento)
        
        # Título
        self.text_prediccion.insert(tk.END, "📊 ANÁLISIS COMPLETO DEL ESTUDIANTE\n", 'titulo')
        self.text_prediccion.insert(tk.END, "="*70 + "\n\n")
        
        # Datos del estudiante
        self.text_prediccion.insert(tk.END, "👤 ESTUDIANTE:\n", 'subtitulo')
        self.text_prediccion.insert(tk.END, f"   {estudiante.nombre} {estudiante.apellidos}\n")
        self.text_prediccion.insert(tk.END, f"   Documento: {documento}\n")
        self.text_prediccion.insert(tk.END, f"   Total de cursos: {len(predicciones)}\n\n")
        
        # Estadísticas generales
        prob_promedio = sum(p['probabilidad_aprobar'] for p in predicciones) / len(predicciones)
        cursos_riesgo = sum(1 for p in predicciones if p['probabilidad_aprobar'] < 0.5)
        
        self.text_prediccion.insert(tk.END, "📈 ESTADÍSTICAS GENERALES:\n", 'subtitulo')
        self.text_prediccion.insert(tk.END, f"   Probabilidad Promedio de Éxito: {prob_promedio*100:.2f}%\n")
        self.text_prediccion.insert(tk.END, f"   Cursos en Riesgo: {cursos_riesgo}/{len(predicciones)}\n\n")
        
        # Detalle por curso
        self.text_prediccion.insert(tk.END, "📚 PREDICCIÓN POR CURSO:\n", 'subtitulo')
        self.text_prediccion.insert(tk.END, "-"*70 + "\n\n")
        
        # Ordenar por probabilidad (menor a mayor para ver riesgos primero)
        predicciones_ordenadas = sorted(predicciones, key=lambda x: x['probabilidad_aprobar'])
        
        for i, pred in enumerate(predicciones_ordenadas, 1):
            curso = pred['curso']
            nombre_curso = pred['nombre_curso']
            prob = pred['probabilidad_aprobar'] * 100
            prediccion = pred['prediccion']
            
            self.text_prediccion.insert(tk.END, f"{i}. {curso} - {nombre_curso}\n")
            
            if prediccion == "APROBARÁ":
                self.text_prediccion.insert(tk.END, f"   ✅ {prediccion} ({prob:.1f}%)\n", 'exito')
            else:
                self.text_prediccion.insert(tk.END, f"   ❌ {prediccion} ({prob:.1f}%)\n", 'riesgo')
            
            # Barra de progreso visual
            barras = int(prob / 5)
            self.text_prediccion.insert(tk.END, f"   [{'█' * barras}{'░' * (20-barras)}]\n\n")

    def btn_estudiantes_riesgo(self):
        """Identifica y muestra estudiantes en riesgo de reprobar"""
        if not self.controlador:
            return
        
        estudiantes_riesgo = self.controlador.obtener_estudiantes_riesgo(umbral=0.5)
        
        if not estudiantes_riesgo:
            self.text_prediccion.delete(1.0, tk.END)
            self.text_prediccion.insert(tk.END, "✅ ¡Excelente! No hay estudiantes en riesgo alto.\n", 'exito')
            return
        
        self._mostrar_estudiantes_riesgo(estudiantes_riesgo)

    def _mostrar_estudiantes_riesgo(self, estudiantes_riesgo):
        """Muestra el reporte de estudiantes en riesgo"""
        self.text_prediccion.delete(1.0, tk.END)
        
        # Título
        self.text_prediccion.insert(tk.END, "⚠️  ALERTA: ESTUDIANTES EN RIESGO\n", 'titulo')
        self.text_prediccion.insert(tk.END, "="*70 + "\n\n")
        
        self.text_prediccion.insert(tk.END, f"Total de estudiantes en riesgo: {len(estudiantes_riesgo)}\n\n", 'riesgo')
        
        # Agrupar por nivel de riesgo
        riesgo_alto = [e for e in estudiantes_riesgo if e['probabilidad_aprobar'] < 0.3]
        riesgo_medio = [e for e in estudiantes_riesgo if 0.3 <= e['probabilidad_aprobar'] < 0.5]
        
        # RIESGO ALTO
        if riesgo_alto:
            self.text_prediccion.insert(tk.END, "🚨 RIESGO ALTO (< 30%):\n", 'riesgo')
            self.text_prediccion.insert(tk.END, "-"*70 + "\n")
            
            for est in riesgo_alto:
                self.text_prediccion.insert(tk.END, f"\n📌 {est['nombre']}\n")
                self.text_prediccion.insert(tk.END, f"   Documento: {est['documento']}\n")
                self.text_prediccion.insert(tk.END, f"   Curso: {est['curso']} - {est['nombre_curso']}\n")
                self.text_prediccion.insert(tk.END, f"   Probabilidad de aprobar: {est['probabilidad_aprobar']*100:.1f}%\n", 'riesgo')
                self.text_prediccion.insert(tk.END, f"   Nota actual: {est['promedio_actual']:.2f}\n")
            
            self.text_prediccion.insert(tk.END, "\n")
        
        # RIESGO MEDIO
        if riesgo_medio:
            self.text_prediccion.insert(tk.END, "⚠️  RIESGO MEDIO (30% - 50%):\n", 'advertencia')
            self.text_prediccion.insert(tk.END, "-"*70 + "\n")
            
            for est in riesgo_medio:
                self.text_prediccion.insert(tk.END, f"\n📌 {est['nombre']}\n")
                self.text_prediccion.insert(tk.END, f"   Documento: {est['documento']}\n")
                self.text_prediccion.insert(tk.END, f"   Curso: {est['curso']} - {est['nombre_curso']}\n")
                self.text_prediccion.insert(tk.END, f"   Probabilidad de aprobar: {est['probabilidad_aprobar']*100:.1f}%\n", 'advertencia')
                self.text_prediccion.insert(tk.END, f"   Nota actual: {est['promedio_actual']:.2f}\n")
        
        # Recomendaciones
        self.text_prediccion.insert(tk.END, "\n\n💡 ACCIONES RECOMENDADAS:\n", 'subtitulo')
        self.text_prediccion.insert(tk.END, "   • Contactar a los estudiantes en riesgo alto prioritariamente\n")
        self.text_prediccion.insert(tk.END, "   • Ofrecer tutorías o asesorías académicas\n")
        self.text_prediccion.insert(tk.END, "   • Revisar estrategias pedagógicas en cursos con alta reprobación\n")
        self.text_prediccion.insert(tk.END, "   • Implementar sistemas de seguimiento continuo\n")

    def btn_recomendar_cursos(self):
        """Genera recomendaciones de cursos para un estudiante"""
        if not self.controlador:
            return
        
        documento = self.entry_rec_documento.get().strip()
        
        if not documento:
            self.mostrar_error("Error", "Debe ingresar un documento de estudiante")
            return
        
        recomendaciones = self.controlador.recomendar_cursos_estudiante(documento)
        
        if recomendaciones is not None:
            self._mostrar_recomendaciones_cursos(documento, recomendaciones)

    def _mostrar_recomendaciones_cursos(self, documento, recomendaciones):
        """Muestra las recomendaciones de cursos"""
        self.text_prediccion.delete(1.0, tk.END)
        
        estudiante = self.controlador.modelo.estudiantes.get(documento)
        
        # Título
        self.text_prediccion.insert(tk.END, "💡 RECOMENDACIÓN DE CURSOS\n", 'titulo')
        self.text_prediccion.insert(tk.END, "="*70 + "\n\n")
        
        # Datos del estudiante
        self.text_prediccion.insert(tk.END, "👤 ESTUDIANTE:\n", 'subtitulo')
        self.text_prediccion.insert(tk.END, f"   {estudiante.nombre} {estudiante.apellidos}\n")
        self.text_prediccion.insert(tk.END, f"   Documento: {documento}\n\n")
        
        if not recomendaciones:
            self.text_prediccion.insert(tk.END, "ℹ️  No hay cursos disponibles para recomendar.\n")
            self.text_prediccion.insert(tk.END, "   El estudiante ya está matriculado en todos los cursos.\n")
            return
        
        self.text_prediccion.insert(tk.END, f"📚 Cursos disponibles: {len(recomendaciones)}\n\n")
        
        # Clasificar por nivel de dificultad
        faciles = [r for r in recomendaciones if r['nivel_dificultad'] == 'Fácil']
        medios = [r for r in recomendaciones if r['nivel_dificultad'] == 'Medio']
        dificiles = [r for r in recomendaciones if r['nivel_dificultad'] == 'Difícil']
        
        # CURSOS FÁCILES
        if faciles:
            self.text_prediccion.insert(tk.END, "✅ CURSOS RECOMENDADOS (Alta probabilidad de éxito):\n", 'exito')
            self.text_prediccion.insert(tk.END, "-"*70 + "\n")
            
            for i, rec in enumerate(faciles[:5], 1):  # Top 5
                prob = rec['probabilidad_exito'] * 100
                self.text_prediccion.insert(tk.END, f"\n{i}. {rec['curso']} - {rec['nombre']}\n")
                self.text_prediccion.insert(tk.END, f"   Probabilidad de éxito: {prob:.1f}%\n", 'exito')
                self.text_prediccion.insert(tk.END, f"   Nivel: {rec['nivel_dificultad']}\n")
                barras = int(prob / 5)
                self.text_prediccion.insert(tk.END, f"   [{'█' * barras}{'░' * (20-barras)}]\n")
            
            self.text_prediccion.insert(tk.END, "\n")
        
        # CURSOS MEDIOS
        if medios:
            self.text_prediccion.insert(tk.END, "⚠️  CURSOS MODERADOS:\n", 'advertencia')
            self.text_prediccion.insert(tk.END, "-"*70 + "\n")
            
            for i, rec in enumerate(medios[:3], 1):  # Top 3
                prob = rec['probabilidad_exito'] * 100
                self.text_prediccion.insert(tk.END, f"\n{i}. {rec['curso']} - {rec['nombre']}\n")
                self.text_prediccion.insert(tk.END, f"   Probabilidad de éxito: {prob:.1f}%\n", 'advertencia')
                self.text_prediccion.insert(tk.END, f"   Nivel: {rec['nivel_dificultad']}\n")
            
            self.text_prediccion.insert(tk.END, "\n")
        
        # CURSOS DIFÍCILES
        if dificiles:
            self.text_prediccion.insert(tk.END, "⛔ CURSOS DESAFIANTES (Requieren preparación adicional):\n", 'riesgo')
            self.text_prediccion.insert(tk.END, "-"*70 + "\n")
            
            for i, rec in enumerate(dificiles[:3], 1):  # Top 3
                prob = rec['probabilidad_exito'] * 100
                self.text_prediccion.insert(tk.END, f"\n{i}. {rec['curso']} - {rec['nombre']}\n")
                self.text_prediccion.insert(tk.END, f"   Probabilidad de éxito: {prob:.1f}%\n", 'riesgo')
                self.text_prediccion.insert(tk.END, f"   Nivel: {rec['nivel_dificultad']}\n")
        
        # Consejos finales
        self.text_prediccion.insert(tk.END, "\n\n💡 CONSEJOS:\n", 'subtitulo')
        self.text_prediccion.insert(tk.END, "   • Comience con cursos de alta probabilidad de éxito\n")
        self.text_prediccion.insert(tk.END, "   • Equilibre la carga académica con cursos de diferente dificultad\n")
        self.text_prediccion.insert(tk.END, "   • Considere prerequisitos y secuencia recomendada\n")
        self.text_prediccion.insert(tk.END, "   • Consulte con su asesor académico antes de matricular\n")