# ==================== CONTROLADOR ====================
# controlador.py
import pandas as pd

class ControladorSIGA:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
    
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