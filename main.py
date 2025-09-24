# ==================== main.py ====================
import tkinter as tk
from modelo import ModeloSIGA
from controlador import ControladorSIGA
from vista import VistaSIGA
from utils import verificar_dependencias


class MiniSIGA:
    def __init__(self):
        self.root = tk.Tk()
        self.modelo = ModeloSIGA()
        self.vista = VistaSIGA(self.root)
        self.controlador = ControladorSIGA(self.modelo, self.vista)
        self.vista.establecer_controlador(self.controlador)
        self.cargar_datos_ejemplo()

    def cargar_datos_ejemplo(self):
        """Carga algunos datos de ejemplo para demostrar funcionalidad"""
        try:
            # Crear estudiantes de ejemplo
            self.modelo.crear_estudiante("12345678", "Juan Carlos", "Pérez García", "juan.perez@email.com", "2000-05-15")
            self.modelo.crear_estudiante("87654321", "María Elena", "González López", "maria.gonzalez@email.com", "1999-08-22")
            self.modelo.crear_estudiante("11111111", "Carlos Alberto", "Martínez Silva", "carlos.martinez@email.com", "2001-03-10")
            self.modelo.crear_estudiante("22222222", "Ana Sofía", "Rodríguez Herrera", "ana.rodriguez@email.com", "2000-12-05")
            self.modelo.crear_estudiante("33333333", "Luis Fernando", "Fernández Castro", "luis.fernandez@email.com", "1998-09-18")
            self.modelo.crear_estudiante("44444444", "Isabella", "García Ruiz", "isabella.garcia@email.com", "2002-01-30")
            self.modelo.crear_estudiante("55555555", "Diego Andrés", "López Morales", "diego.lopez@email.com", "1999-11-12")

            # Crear cursos de ejemplo
            self.modelo.crear_curso("PROG101", "Fundamentos de Programación")
            self.modelo.crear_curso("MAT201", "Matemáticas Discretas")
            self.modelo.crear_curso("BD301", "Bases de Datos")
            self.modelo.crear_curso("WEB401", "Desarrollo Web")
            self.modelo.crear_curso("ALG501", "Algoritmos y Estructuras de Datos")
            self.modelo.crear_curso("ING601", "Ingeniería de Software")

            # Crear matrículas de ejemplo
            self.modelo.matricular_estudiante("12345678", "PROG101", 4.5)
            self.modelo.matricular_estudiante("12345678", "MAT201", 3.8)
            self.modelo.matricular_estudiante("12345678", "WEB401", 4.2)

            self.modelo.matricular_estudiante("87654321", "PROG101", 4.8)
            self.modelo.matricular_estudiante("87654321", "BD301", 4.7)
            self.modelo.matricular_estudiante("87654321", "ALG501", 4.3)

            self.modelo.matricular_estudiante("11111111", "PROG101", 2.8)
            self.modelo.matricular_estudiante("11111111", "WEB401", 3.5)
            self.modelo.matricular_estudiante("11111111", "MAT201", 2.5)

            self.modelo.matricular_estudiante("22222222", "MAT201", 4.0)
            self.modelo.matricular_estudiante("22222222", "BD301", 3.2)
            self.modelo.matricular_estudiante("22222222", "ING601", 4.1)

            self.modelo.matricular_estudiante("33333333", "PROG101", 4.9)
            self.modelo.matricular_estudiante("33333333", "WEB401", 4.6)
            self.modelo.matricular_estudiante("33333333", "ALG501", 4.4)

            self.modelo.matricular_estudiante("44444444", "BD301", 3.7)
            self.modelo.matricular_estudiante("44444444", "ING601", 3.9)
            self.modelo.matricular_estudiante("44444444", "MAT201", 3.3)

            self.modelo.matricular_estudiante("55555555", "PROG101", 3.1)
            self.modelo.matricular_estudiante("55555555", "ALG501", 2.9)
            self.modelo.matricular_estudiante("55555555", "WEB401", 3.4)

            # Actualizar vista
            self.vista.refrescar_todas_las_tablas()

        except Exception as e:
            print(f"Error cargando datos de ejemplo: {e}")

    def ejecutar(self):
        self.root.mainloop()


# ==================== PUNTO DE ENTRADA ====================
if __name__ == "__main__":
    print("MiniSIGA - Sistema de Gestión Académica")
    print("=" * 40)

    if not verificar_dependencias():
        input("Presiona Enter para salir...")
        exit(1)

    try:
        app = MiniSIGA()
        app.ejecutar()
    except Exception as e:
        print(f"Error fatal: {str(e)}")
        input("Presiona Enter para salir...")

    print("Aplicación finalizada.")
