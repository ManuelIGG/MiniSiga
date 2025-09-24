## ==================== modelo.py ====================
import csv
import json
import re
from datetime import datetime


class Estudiante:
    def __init__(self, documento, nombre, apellidos, correo, fecha_nac):
        self.documento = documento
        self.nombre = nombre
        self.apellidos = apellidos
        self.correo = correo
        self.fecha_nac = fecha_nac
        self.cursos = []
        self.notas = {}


    def to_dict(self):
        return {
        'documento': self.documento,
        'nombre': self.nombre,
        'apellidos': self.apellidos,
        'correo': self.correo,
        'fecha_nac': self.fecha_nac,
        'cursos': self.cursos,
        'notas': self.notas
        }


class Curso:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre
        self.estudiantes = []


    def to_dict(self):
        return {
        'codigo': self.codigo,
        'nombre': self.nombre,
        'estudiantes': self.estudiantes
        }


class ModeloSIGA:
    def __init__(self):
        self.estudiantes = {}  # documento -> Estudiante
        self.cursos = {}       # codigo -> Curso
        self.matriculas = []   # [(documento, codigo_curso, nota)]
        
    def crear_estudiante(self, documento, nombre, apellidos, correo, fecha_nac):
        if documento in self.estudiantes:
            raise ValueError("El estudiante ya existe")
        
        # Validaciones
        if not self._validar_documento(documento):
            raise ValueError("Documento inválido")
        if not self._validar_email(correo):
            raise ValueError("Email inválido")
        if not self._validar_fecha(fecha_nac):
            raise ValueError("Fecha inválida")
            
        estudiante = Estudiante(documento, nombre, apellidos, correo, fecha_nac)
        self.estudiantes[documento] = estudiante
        return estudiante
    
    def crear_curso(self, codigo, nombre):
        if codigo in self.cursos:
            raise ValueError("El curso ya existe")
        
        curso = Curso(codigo, nombre)
        self.cursos[codigo] = curso
        return curso
    
    def matricular_estudiante(self, documento, codigo_curso, nota=0.0):
        if documento not in self.estudiantes:
            raise ValueError("Estudiante no encontrado")
        if codigo_curso not in self.cursos:
            raise ValueError("Curso no encontrado")
        
        # Verificar si ya está matriculado
        for matricula in self.matriculas:
            if matricula[0] == documento and matricula[1] == codigo_curso:
                raise ValueError("El estudiante ya está matriculado en este curso")
        
        if not (0 <= nota <= 5):
            raise ValueError("La nota debe estar entre 0 y 5")
            
        self.matriculas.append((documento, codigo_curso, nota))
        self.estudiantes[documento].cursos.append(codigo_curso)
        self.estudiantes[documento].notas[codigo_curso] = nota
        self.cursos[codigo_curso].estudiantes.append(documento)
    
    def actualizar_nota(self, documento, codigo_curso, nueva_nota):
        if not (0 <= nueva_nota <= 5):
            raise ValueError("La nota debe estar entre 0 y 5")
            
        # Actualizar en la lista de matrículas
        for i, (doc, curso, nota) in enumerate(self.matriculas):
            if doc == documento and curso == codigo_curso:
                self.matriculas[i] = (documento, codigo_curso, nueva_nota)
                self.estudiantes[documento].notas[codigo_curso] = nueva_nota
                return True
        
        raise ValueError("Matrícula no encontrada")
    
    def buscar_estudiantes(self, termino=""):
        if not termino:
            return list(self.estudiantes.values())
            
        resultados = []
        for estudiante in self.estudiantes.values():
            if (termino.lower() in estudiante.nombre.lower() or 
                termino.lower() in estudiante.apellidos.lower() or
                termino in estudiante.documento or
                termino.lower() in estudiante.correo.lower()):
                resultados.append(estudiante)
        return sorted(resultados, key=lambda x: x.apellidos)
    
    def obtener_top_estudiantes(self, codigo_curso, n=3):
        estudiantes_curso = []
        for documento, curso, nota in self.matriculas:
            if curso == codigo_curso:
                estudiante = self.estudiantes[documento]
                estudiantes_curso.append((estudiante, nota))
        
        return sorted(estudiantes_curso, key=lambda x: x[1], reverse=True)[:n]
    
    def obtener_estadisticas_aprobados(self, codigo_curso):
        aprobados = 0
        reprobados = 0
        
        for documento, curso, nota in self.matriculas:
            if curso == codigo_curso:
                if nota >= 3.0:
                    aprobados += 1
                else:
                    reprobados += 1
        
        return aprobados, reprobados
    
    def obtener_matriculas_por_curso(self, codigo_curso=""):
        if codigo_curso:
            return [(doc, curso, nota) for doc, curso, nota in self.matriculas if curso == codigo_curso]
        return self.matriculas
    
    def eliminar_estudiante(self, documento):
        if documento in self.estudiantes:
            # Eliminar de cursos
            for codigo_curso in self.estudiantes[documento].cursos:
                if codigo_curso in self.cursos:
                    self.cursos[codigo_curso].estudiantes.remove(documento)
            
            # Eliminar matrículas
            self.matriculas = [m for m in self.matriculas if m[0] != documento]
            
            # Eliminar estudiante
            del self.estudiantes[documento]
            return True
        return False
    
    def eliminar_curso(self, codigo_curso):
        if codigo_curso in self.cursos:
            # Eliminar de estudiantes
            for documento in self.cursos[codigo_curso].estudiantes:
                if documento in self.estudiantes:
                    self.estudiantes[documento].cursos.remove(codigo_curso)
                    if codigo_curso in self.estudiantes[documento].notas:
                        del self.estudiantes[documento].notas[codigo_curso]
            
            # Eliminar matrículas
            self.matriculas = [m for m in self.matriculas if m[1] != codigo_curso]
            
            # Eliminar curso
            del self.cursos[codigo_curso]
            return True
        return False
    
    def cargar_datos_csv(self, archivo_estudiantes, archivo_cursos=None):
        try:
            with open(archivo_estudiantes, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        self.crear_estudiante(
                            row['documento'], row['nombre'], 
                            row['apellidos'], row['correo'], row['fecha_nac']
                        )
                    except (ValueError, KeyError):
                        pass  # Ignorar duplicados o datos inválidos
        except Exception as e:
            raise ValueError(f"Error al cargar CSV: {str(e)}")
    
    def guardar_datos_json(self, archivo):
        datos = {
            'estudiantes': [est.to_dict() for est in self.estudiantes.values()],
            'cursos': [curso.to_dict() for curso in self.cursos.values()],
            'matriculas': self.matriculas
        }
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    
    def cargar_datos_json(self, archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            
        # Limpiar datos actuales
        self.estudiantes = {}
        self.cursos = {}
        self.matriculas = []
        
        # Cargar estudiantes
        for est_data in datos.get('estudiantes', []):
            estudiante = Estudiante(
                est_data['documento'], est_data['nombre'],
                est_data['apellidos'], est_data['correo'], est_data['fecha_nac']
            )
            estudiante.cursos = est_data.get('cursos', [])
            estudiante.notas = est_data.get('notas', {})
            self.estudiantes[estudiante.documento] = estudiante
        
        # Cargar cursos
        for curso_data in datos.get('cursos', []):
            curso = Curso(curso_data['codigo'], curso_data['nombre'])
            curso.estudiantes = curso_data.get('estudiantes', [])
            self.cursos[curso.codigo] = curso
        
        # Cargar matrículas
        self.matriculas = datos.get('matriculas', [])
    
    def _validar_documento(self, documento):
        return len(documento.strip()) > 0 and documento.isdigit()
    
    def _validar_email(self, email):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def _validar_fecha(self, fecha):
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            return True
        except ValueError:
            return False
