## ==================== test_tensorflow.py ====================
"""
Script de verificación para probar la implementación de TensorFlow en MiniSIGA.
Ejecutar este script antes de usar el sistema de predicción.
"""

import sys

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas correctamente."""
    print("="*70)
    print("🔍 VERIFICACIÓN DE DEPENDENCIAS - MiniSIGA con TensorFlow")
    print("="*70)
    print()
    
    dependencias = {
        'tensorflow': '2.15.0',
        'sklearn': '1.3.2',
        'numpy': '1.24.3',
        'pandas': '2.1.3',
        'matplotlib': '3.8.2',
        'reportlab': '4.0.7'
    }
    
    errores = []
    
    # Verificar TensorFlow
    print("📦 Verificando TensorFlow...")
    try:
        import tensorflow as tf
        version_tf = tf.__version__
        print(f"   ✅ TensorFlow {version_tf} instalado")
        
        # Verificar GPU
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"   🎮 GPU detectada: {len(gpus)} dispositivo(s)")
        else:
            print(f"   💻 Modo CPU (sin GPU detectada)")
    except ImportError:
        print("   ❌ TensorFlow NO instalado")
        errores.append("tensorflow")
    
    # Verificar scikit-learn
    print("\n📦 Verificando scikit-learn...")
    try:
        import sklearn
        print(f"   ✅ scikit-learn {sklearn.__version__} instalado")
    except ImportError:
        print("   ❌ scikit-learn NO instalado")
        errores.append("scikit-learn")
    
    # Verificar numpy
    print("\n📦 Verificando NumPy...")
    try:
        import numpy as np
        print(f"   ✅ NumPy {np.__version__} instalado")
    except ImportError:
        print("   ❌ NumPy NO instalado")
        errores.append("numpy")
    
    # Verificar pandas
    print("\n📦 Verificando Pandas...")
    try:
        import pandas as pd
        print(f"   ✅ Pandas {pd.__version__} instalado")
    except ImportError:
        print("   ❌ Pandas NO instalado")
        errores.append("pandas")
    
    # Verificar matplotlib
    print("\n📦 Verificando Matplotlib...")
    try:
        import matplotlib
        print(f"   ✅ Matplotlib {matplotlib.__version__} instalado")
    except ImportError:
        print("   ❌ Matplotlib NO instalado")
        errores.append("matplotlib")
    
    # Verificar reportlab
    print("\n📦 Verificando ReportLab...")
    try:
        import reportlab
        print(f"   ✅ ReportLab instalado")
    except ImportError:
        print("   ❌ ReportLab NO instalado")
        errores.append("reportlab")
    
    # Verificar tkinter
    print("\n📦 Verificando Tkinter...")
    try:
        import tkinter
        print(f"   ✅ Tkinter disponible")
    except ImportError:
        print("   ❌ Tkinter NO disponible")
        errores.append("tkinter")
    
    print("\n" + "="*70)
    
    if errores:
        print("❌ FALTAN DEPENDENCIAS\n")
        print("Instala las dependencias faltantes con:")
        print("pip install -r requirements.txt")
        print("\nO individualmente:")
        for dep in errores:
            if dep == "scikit-learn":
                print(f"   pip install {dep}")
            else:
                print(f"   pip install {dep}")
        return False
    else:
        print("✅ TODAS LAS DEPENDENCIAS ESTÁN INSTALADAS CORRECTAMENTE")
        return True


def test_modelo_basico():
    """Prueba básica del modelo de predicción."""
    print("\n" + "="*70)
    print("🧪 PRUEBA DEL MODELO DE PREDICCIÓN")
    print("="*70)
    print()
    
    try:
        # Importar clases necesarias
        from predictor import PredictorAcademico
        from modelo import ModeloSIGA
        
        print("📥 Creando modelo SIGA de prueba...")
        modelo = ModeloSIGA()
        
        # Crear datos de ejemplo
        print("📝 Agregando datos de prueba...")
        
        # Estudiantes
        modelo.crear_estudiante("1001", "Juan", "Pérez", "juan@test.com", "2000-01-01")
        modelo.crear_estudiante("1002", "María", "García", "maria@test.com", "2000-02-02")
        modelo.crear_estudiante("1003", "Pedro", "López", "pedro@test.com", "2000-03-03")
        modelo.crear_estudiante("1004", "Ana", "Martínez", "ana@test.com", "2000-04-04")
        modelo.crear_estudiante("1005", "Luis", "Rodríguez", "luis@test.com", "2000-05-05")
        
        # Cursos
        modelo.crear_curso("MAT101", "Matemáticas I")
        modelo.crear_curso("PROG101", "Programación I")
        
        # Matrículas (mezcla de aprobados y reprobados)
        modelo.matricular_estudiante("1001", "MAT101", 4.5)
        modelo.matricular_estudiante("1001", "PROG101", 4.2)
        modelo.matricular_estudiante("1002", "MAT101", 2.8)
        modelo.matricular_estudiante("1002", "PROG101", 3.5)
        modelo.matricular_estudiante("1003", "MAT101", 4.0)
        modelo.matricular_estudiante("1003", "PROG101", 4.8)
        modelo.matricular_estudiante("1004", "MAT101", 2.5)
        modelo.matricular_estudiante("1004", "PROG101", 2.9)
        modelo.matricular_estudiante("1005", "MAT101", 3.8)
        modelo.matricular_estudiante("1005", "PROG101", 4.1)
        
        print(f"   ✅ Creados {len(modelo.estudiantes)} estudiantes")
        print(f"   ✅ Creados {len(modelo.cursos)} cursos")
        print(f"   ✅ Creadas {len(modelo.matriculas)} matrículas")
        
        # Crear predictor
        print("\n🤖 Inicializando predictor...")
        predictor = PredictorAcademico()
        
        # Entrenar modelo
        print("🚀 Entrenando modelo (esto puede tardar unos segundos)...")
        metricas = predictor.entrenar(modelo, epochs=50, verbose=0)
        
        print(f"\n📊 Métricas de entrenamiento:")
        print(f"   • Precisión: {metricas['val_accuracy']*100:.2f}%")
        print(f"   • Precision: {metricas['val_precision']*100:.2f}%")
        print(f"   • Recall: {metricas['val_recall']*100:.2f}%")
        print(f"   • Épocas: {metricas['epochs_trained']}")
        
        # Realizar predicción de prueba
        print("\n🔮 Realizando predicción de prueba...")
        resultado = predictor.predecir(modelo, "1001", "MAT101")
        
        print(f"\n   Estudiante: Juan Pérez")
        print(f"   Curso: Matemáticas I")
        print(f"   Predicción: {resultado['prediccion']}")
        print(f"   Probabilidad: {resultado['probabilidad_aprobar']*100:.1f}%")
        print(f"   Confianza: {resultado['confianza']*100:.1f}%")
        
        # Guardar modelo
        print("\n💾 Guardando modelo...")
        predictor.guardar_modelo()
        print("   ✅ Modelo guardado en 'modelo_prediccion.h5'")
        
        print("\n" + "="*70)
        print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
        print("="*70)
        print("\n💡 El sistema de predicción está listo para usar en MiniSIGA")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN LA PRUEBA:")
        print(f"   {str(e)}")
        print("\nVerifica que:")
        print("   1. El archivo predictor.py existe en el directorio")
        print("   2. El archivo modelo.py existe en el directorio")
        print("   3. Todas las dependencias están instaladas")
        return False


def main():
    """Función principal."""
    print("\n🚀 INICIANDO VERIFICACIÓN DEL SISTEMA\n")
    
    # Paso 1: Verificar dependencias
    if not verificar_dependencias():
        print("\n⚠️  Instala las dependencias faltantes antes de continuar.")
        return False
    
    # Paso 2: Probar modelo
    print("\n¿Deseas ejecutar una prueba del modelo de predicción? (s/n): ", end='')
    respuesta = input().strip().lower()
    
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        if not test_modelo_basico():
            print("\n⚠️  La prueba del modelo falló. Revisa los errores anteriores.")
            return False
    else:
        print("\n⏭️  Prueba del modelo omitida.")
    
    print("\n" + "="*70)
    print("🎉 ¡VERIFICACIÓN COMPLETADA!")
    print("="*70)
    print("\n✅ El sistema está listo para ejecutar MiniSIGA con predicción IA")
    print("\n📝 Próximos pasos:")
    print("   1. Ejecuta: python main.py")
    print("   2. Ve a la pestaña '🤖 Predicción IA'")
    print("   3. Entrena el modelo con tus datos reales")
    print("   4. ¡Comienza a predecir el rendimiento académico!")
    print("\n📖 Para más información, consulta: INSTRUCCIONES_TENSORFLOW.md")
    print()
    
    return True


if __name__ == "__main__":
    try:
        exito = main()
        sys.exit(0 if exito else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificación interrumpida por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        sys.exit(1)