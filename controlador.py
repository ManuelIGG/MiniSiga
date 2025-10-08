# controlador.py
import pandas as pd
from predictor import PredictorAcademico, AnalizadorRendimiento


class ControladorSIGA:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self.predictor = PredictorAcademico()
        self.analizador = AnalizadorRendimiento()
    
    def generar_reporte_estudiantes(self):
        data = []
        for est in self.modelo.estudiantes.values():
            for curso_cod in est.cursos:
                data.append({
                    "Documento": est.documento,
                    "Nombre": f"{est.nombre} {est.apellidos}",
                    "Correo": est.correo,
                    "Curso": curso_cod,
                    "Nota": est.notas.get(curso_cod, 0.0)
                })
        df = pd.DataFrame(data)
        return df
    
    # ==================== MÉTODOS DE PREDICCIÓN ====================
    
    def entrenar_modelo_prediccion(self):
        """Entrena el modelo de predicción con los datos actuales."""
        try:
            if len(self.modelo.matriculas) < 10:
                self.vista.mostrar_error(
                    "Error de Entrenamiento",
                    "Se necesitan al menos 10 matrículas para entrenar el modelo.\n"
                    f"Actualmente hay {len(self.modelo.matriculas)} matrículas."
                )
                return False
            
            # Entrenar modelo
            metricas = self.predictor.entrenar(self.modelo, epochs=150, verbose=1)
            
            # Guardar modelo
            self.predictor.guardar_modelo()
            
            # Mostrar resultados
            mensaje = (
                f"✅ Modelo entrenado exitosamente!\n\n"
                f"📊 Métricas de Validación:\n"
                f"  • Precisión: {metricas['val_accuracy']*100:.2f}%\n"
                f"  • Precision: {metricas['val_precision']*100:.2f}%\n"
                f"  • Recall: {metricas['val_recall']*100:.2f}%\n"
                f"  • Épocas: {metricas['epochs_trained']}\n\n"
                f"💾 Modelo guardado correctamente."
            )
            
            self.vista.mostrar_mensaje("Entrenamiento Completado", mensaje)
            return True
            
        except Exception as e:
            self.vista.mostrar_error("Error", f"Error al entrenar el modelo:\n{str(e)}")
            return False
    
    def cargar_modelo_prediccion(self):
        """Carga un modelo previamente entrenado."""
        try:
            self.predictor.cargar_modelo()
            self.vista.mostrar_mensaje("Éxito", "Modelo cargado correctamente")
            return True
        except FileNotFoundError:
            self.vista.mostrar_error(
                "Error",
                "No se encontró un modelo guardado.\n"
                "Primero debe entrenar el modelo."
            )
            return False
        except Exception as e:
            self.vista.mostrar_error("Error", f"Error al cargar el modelo:\n{str(e)}")
            return False
    
    def predecir_estudiante(self, documento, codigo_curso):
        """Realiza una predicción para un estudiante en un curso específico."""
        try:
            if not self.predictor.modelo_entrenado:
                self.vista.mostrar_error(
                    "Error",
                    "Primero debe entrenar o cargar un modelo de predicción."
                )
                return None
            
            resultado = self.predictor.predecir(self.modelo, documento, codigo_curso)
            return resultado
            
        except ValueError as e:
            self.vista.mostrar_error("Error", str(e))
            return None
        except Exception as e:
            self.vista.mostrar_error("Error", f"Error en la predicción:\n{str(e)}")
            return None
    
    def predecir_todos_cursos_estudiante(self, documento):
        """Predice el rendimiento de un estudiante en todos sus cursos."""
        try:
            if not self.predictor.modelo_entrenado:
                self.vista.mostrar_error(
                    "Error",
                    "Primero debe entrenar o cargar un modelo de predicción."
                )
                return None
            
            predicciones = self.predictor.predecir_batch(self.modelo, documento)
            return predicciones
            
        except Exception as e:
            self.vista.mostrar_error("Error", f"Error en la predicción:\n{str(e)}")
            return None
    
    def obtener_estudiantes_riesgo(self, umbral=0.4):
        """Identifica estudiantes en riesgo de reprobar."""
        try:
            if not self.predictor.modelo_entrenado:
                return []
            
            estudiantes_riesgo = self.analizador.identificar_estudiantes_riesgo(
                self.modelo, self.predictor, umbral
            )
            return estudiantes_riesgo
            
        except Exception as e:
            print(f"Error obteniendo estudiantes en riesgo: {e}")
            return []
    
    def recomendar_cursos_estudiante(self, documento):
        """Recomienda cursos para un estudiante basándose en IA."""
        try:
            if not self.predictor.modelo_entrenado:
                self.vista.mostrar_error(
                    "Error",
                    "Primero debe entrenar o cargar un modelo de predicción."
                )
                return None
            
            recomendaciones = self.analizador.recomendar_cursos(
                self.modelo, self.predictor, documento
            )
            return recomendaciones
            
        except Exception as e:
            self.vista.mostrar_error("Error", f"Error generando recomendaciones:\n{str(e)}")
            return None
    
    # ==================== MÉTODOS EXISTENTES ====================
        
    def crear_estudiante(self, documento, nombre, apellidos, correo, fecha_nac):
        try:
            estudiante = self.modelo.crear_estudiante(documento, nombre, apellidos, correo, fecha_nac)
            self.vista.mostrar_mensaje("Éxito", f"Estudiante {nombre} {apellidos} creado correctamente")
            self.vista.refrescar_tabla_estudiantes()
            return True
        except ValueError as e:
            self.vista.mostrar_error("Error", str(e))
            return False
    
    def crear_curso(self, codigo, nombre):
        try:
            curso = self.modelo.crear_curso(codigo, nombre)
            self.vista.mostrar_mensaje("Éxito", f"Curso {nombre} creado correctamente")
            self.vista.refrescar_tabla_cursos()
            return True
        except ValueError as e:
            self.vista.mostrar_error("Error", str(e))
            return False
    
    def matricular_estudiante(self, documento, codigo_curso, nota):
        try:
            self.modelo.matricular_estudiante(documento, codigo_curso, float(nota))
            self.vista.mostrar_mensaje("Éxito", "Estudiante matriculado correctamente")
            self.vista.refrescar_tabla_cursos()
            self.vista.refrescar_tabla_matriculas()
            return True
        except ValueError as e:
            self.vista.mostrar_error("Error", str(e))
            return False
    
    def actualizar_nota(self, documento, codigo_curso, nueva_nota):
        try:
            self.modelo.actualizar_nota(documento, codigo_curso, float(nueva_nota))
            self.vista.mostrar_mensaje("Éxito", "Nota actualizada correctamente")
            self.vista.refrescar_tabla_matriculas()
            self.vista.refrescar_tabla_cursos()
            return True
        except ValueError as e:
            self.vista.mostrar_error("Error", str(e))
            return False
    
    def buscar_estudiantes(self, termino):
        return self.modelo.buscar_estudiantes(termino)
    
    def eliminar_estudiante(self, documento):
        if self.modelo.eliminar_estudiante(documento):
            self.vista.mostrar_mensaje("Éxito", "Estudiante eliminado correctamente")
            self.vista.refrescar_tabla_estudiantes()
            self.vista.refrescar_tabla_cursos()
            self.vista.refrescar_tabla_matriculas()
        else:
            self.vista.mostrar_error("Error", "Estudiante no encontrado")
    
    def eliminar_curso(self, codigo_curso):
        if self.modelo.eliminar_curso(codigo_curso):
            self.vista.mostrar_mensaje("Éxito", "Curso eliminado correctamente")
            self.vista.refrescar_tabla_cursos()
            self.vista.refrescar_tabla_matriculas()
        else:
            self.vista.mostrar_error("Error", "Curso no encontrado")
    
    def cargar_csv(self, archivo):
        try:
            self.modelo.cargar_datos_csv(archivo)
            self.vista.mostrar_mensaje("Éxito", "Datos cargados desde CSV")
            self.vista.refrescar_tabla_estudiantes()
        except Exception as e:
            self.vista.mostrar_error("Error", f"Error al cargar CSV: {str(e)}")
    
    def guardar_json(self, archivo):
        try:
            self.modelo.guardar_datos_json(archivo)
            self.vista.mostrar_mensaje("Éxito", "Datos guardados en JSON")
        except Exception as e:
            self.vista.mostrar_error("Error", f"Error al guardar JSON: {str(e)}")
    
    def cargar_json(self, archivo):
        try:
            self.modelo.cargar_datos_json(archivo)
            self.vista.mostrar_mensaje("Éxito", "Datos cargados desde JSON")
            self.vista.refrescar_todas_las_tablas()
        except Exception as e:
            self.vista.mostrar_error("Error", f"Error al cargar JSON: {str(e)}")