## ==================== predictor.py ====================
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
import os


class PredictorAcademico:
    """
    Sistema de predicción académica usando TensorFlow.
    Predice si un estudiante aprobará un curso basándose en:
    - Promedio histórico del estudiante
    - Número de cursos matriculados
    - Promedio del curso
    - Tasa de aprobación del curso
    """
    
    def __init__(self):
        self.modelo = None
        self.scaler = StandardScaler()
        self.modelo_entrenado = False
        self.ruta_modelo = "modelo_prediccion.h5"
        self.ruta_scaler = "scaler.pkl"
        
    def preparar_datos(self, modelo_siga):
        """
        Prepara los datos de entrenamiento desde el modelo SIGA.
        
        Features:
        - Promedio histórico del estudiante
        - Número de cursos del estudiante
        - Promedio del curso
        - Tasa de aprobación del curso
        - Número de estudiantes en el curso
        
        Target:
        - 1 si aprobó (nota >= 3.0), 0 si reprobó
        """
        X = []  # Features
        y = []  # Target (aprobado/reprobado)
        
        for documento, codigo_curso, nota in modelo_siga.matriculas:
            estudiante = modelo_siga.estudiantes.get(documento)
            if not estudiante:
                continue
            
            # Feature 1: Promedio histórico del estudiante (excluyendo el curso actual)
            notas_estudiante = [n for c, n in estudiante.notas.items() if c != codigo_curso]
            promedio_estudiante = np.mean(notas_estudiante) if notas_estudiante else 2.5
            
            # Feature 2: Número de cursos del estudiante
            num_cursos_estudiante = len(estudiante.cursos)
            
            # Feature 3: Promedio del curso
            notas_curso = [n for d, c, n in modelo_siga.matriculas if c == codigo_curso]
            promedio_curso = np.mean(notas_curso) if notas_curso else 3.0
            
            # Feature 4: Tasa de aprobación del curso
            aprobados, reprobados = modelo_siga.obtener_estadisticas_aprobados(codigo_curso)
            total_curso = aprobados + reprobados
            tasa_aprobacion = aprobados / total_curso if total_curso > 0 else 0.5
            
            # Feature 5: Número de estudiantes en el curso
            num_estudiantes_curso = total_curso
            
            # Crear vector de features
            features = [
                promedio_estudiante,
                num_cursos_estudiante,
                promedio_curso,
                tasa_aprobacion,
                num_estudiantes_curso
            ]
            
            # Target: 1 si aprobó, 0 si reprobó
            target = 1 if nota >= 3.0 else 0
            
            X.append(features)
            y.append(target)
        
        return np.array(X), np.array(y)
    
    def construir_modelo(self):
        """Construye la arquitectura de la red neuronal."""
        modelo = keras.Sequential([
            keras.layers.Dense(16, activation='relu', input_shape=(5,)),
            keras.layers.Dropout(0.3),
            keras.layers.Dense(8, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(4, activation='relu'),
            keras.layers.Dense(1, activation='sigmoid')
        ])
        
        modelo.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )
        
        return modelo
    
    def entrenar(self, modelo_siga, epochs=100, verbose=0):
        """
        Entrena el modelo con los datos del sistema SIGA.
        
        Returns:
            dict: Historial de entrenamiento y métricas
        """
        # Preparar datos
        X, y = self.preparar_datos(modelo_siga)
        
        if len(X) < 10:
            raise ValueError("No hay suficientes datos para entrenar (mínimo 10 matrículas)")
        
        # Normalizar features
        X_scaled = self.scaler.fit_transform(X)
        
        # Dividir en entrenamiento y validación
        X_train, X_val, y_train, y_val = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Construir modelo
        self.modelo = self.construir_modelo()
        
        # Callbacks para mejor entrenamiento
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=15,
            restore_best_weights=True
        )
        
        reduce_lr = keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=0.00001
        )
        
        # Entrenar
        history = self.modelo.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=min(32, len(X_train) // 2),
            callbacks=[early_stopping, reduce_lr],
            verbose=verbose
        )
        
        self.modelo_entrenado = True
        
        # Evaluar en conjunto de validación
        loss, accuracy, precision, recall = self.modelo.evaluate(X_val, y_val, verbose=0)
        
        return {
            'history': history.history,
            'val_loss': loss,
            'val_accuracy': accuracy,
            'val_precision': precision,
            'val_recall': recall,
            'epochs_trained': len(history.history['loss'])
        }
    
    def predecir(self, modelo_siga, documento, codigo_curso):
        """
        Predice la probabilidad de que un estudiante apruebe un curso.
        
        Returns:
            dict: Probabilidad, predicción y confianza
        """
        if not self.modelo_entrenado:
            raise ValueError("El modelo no ha sido entrenado")
        
        estudiante = modelo_siga.estudiantes.get(documento)
        if not estudiante:
            raise ValueError("Estudiante no encontrado")
        
        if codigo_curso not in modelo_siga.cursos:
            raise ValueError("Curso no encontrado")
        
        # Calcular features para la predicción
        notas_estudiante = list(estudiante.notas.values())
        promedio_estudiante = np.mean(notas_estudiante) if notas_estudiante else 2.5
        num_cursos_estudiante = len(estudiante.cursos)
        
        notas_curso = [n for d, c, n in modelo_siga.matriculas if c == codigo_curso]
        promedio_curso = np.mean(notas_curso) if notas_curso else 3.0
        
        aprobados, reprobados = modelo_siga.obtener_estadisticas_aprobados(codigo_curso)
        total_curso = aprobados + reprobados
        tasa_aprobacion = aprobados / total_curso if total_curso > 0 else 0.5
        num_estudiantes_curso = total_curso
        
        # Crear vector de features
        features = np.array([[
            promedio_estudiante,
            num_cursos_estudiante,
            promedio_curso,
            tasa_aprobacion,
            num_estudiantes_curso
        ]])
        
        # Normalizar
        features_scaled = self.scaler.transform(features)
        
        # Predecir
        probabilidad = self.modelo.predict(features_scaled, verbose=0)[0][0]
        prediccion = "APROBARÁ" if probabilidad >= 0.5 else "REPROBARÁ"
        confianza = probabilidad if probabilidad >= 0.5 else (1 - probabilidad)
        
        return {
            'probabilidad_aprobar': float(probabilidad),
            'prediccion': prediccion,
            'confianza': float(confianza),
            'features': {
                'promedio_estudiante': promedio_estudiante,
                'num_cursos': num_cursos_estudiante,
                'promedio_curso': promedio_curso,
                'tasa_aprobacion_curso': tasa_aprobacion
            }
        }
    
    def predecir_batch(self, modelo_siga, documento):
        """
        Predice el rendimiento de un estudiante en todos sus cursos actuales.
        
        Returns:
            list: Lista de predicciones para cada curso
        """
        estudiante = modelo_siga.estudiantes.get(documento)
        if not estudiante:
            raise ValueError("Estudiante no encontrado")
        
        predicciones = []
        for codigo_curso in estudiante.cursos:
            try:
                prediccion = self.predecir(modelo_siga, documento, codigo_curso)
                prediccion['curso'] = codigo_curso
                prediccion['nombre_curso'] = modelo_siga.cursos[codigo_curso].nombre
                predicciones.append(prediccion)
            except Exception as e:
                print(f"Error prediciendo curso {codigo_curso}: {e}")
        
        return predicciones
    
    def guardar_modelo(self):
        """Guarda el modelo entrenado y el scaler."""
        if not self.modelo_entrenado:
            raise ValueError("No hay modelo entrenado para guardar")
        
        self.modelo.save(self.ruta_modelo)
        with open(self.ruta_scaler, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        print(f"Modelo guardado en {self.ruta_modelo}")
    
    def cargar_modelo(self):
        """Carga un modelo previamente entrenado."""
        if not os.path.exists(self.ruta_modelo) or not os.path.exists(self.ruta_scaler):
            raise FileNotFoundError("No se encontraron archivos del modelo")
        
        self.modelo = keras.models.load_model(self.ruta_modelo)
        with open(self.ruta_scaler, 'rb') as f:
            self.scaler = pickle.load(f)
        
        self.modelo_entrenado = True
        print("Modelo cargado exitosamente")
    
    def obtener_importancia_features(self):
        """
        Retorna información sobre las features utilizadas.
        """
        return {
            'features': [
                'Promedio Histórico del Estudiante',
                'Número de Cursos Matriculados',
                'Promedio del Curso',
                'Tasa de Aprobación del Curso',
                'Número de Estudiantes en el Curso'
            ],
            'descripcion': 'Features utilizadas para predecir el rendimiento académico'
        }


class AnalizadorRendimiento:
    """Clase auxiliar para análisis avanzado de rendimiento."""
    
    @staticmethod
    def identificar_estudiantes_riesgo(modelo_siga, predictor, umbral=0.4):
        """
        Identifica estudiantes en riesgo de reprobar sus cursos.
        
        Args:
            umbral: Probabilidad mínima de aprobar (por debajo = riesgo)
        
        Returns:
            list: Estudiantes en riesgo con sus predicciones
        """
        estudiantes_riesgo = []
        
        for documento, estudiante in modelo_siga.estudiantes.items():
            for codigo_curso in estudiante.cursos:
                try:
                    pred = predictor.predecir(modelo_siga, documento, codigo_curso)
                    if pred['probabilidad_aprobar'] < umbral:
                        estudiantes_riesgo.append({
                            'documento': documento,
                            'nombre': f"{estudiante.nombre} {estudiante.apellidos}",
                            'curso': codigo_curso,
                            'nombre_curso': modelo_siga.cursos[codigo_curso].nombre,
                            'probabilidad_aprobar': pred['probabilidad_aprobar'],
                            'promedio_actual': estudiante.notas.get(codigo_curso, 0.0)
                        })
                except Exception:
                    pass
        
        return sorted(estudiantes_riesgo, key=lambda x: x['probabilidad_aprobar'])
    
    @staticmethod
    def recomendar_cursos(modelo_siga, predictor, documento):
        """
        Recomienda cursos para un estudiante basándose en sus probabilidades de éxito.
        
        Returns:
            list: Cursos recomendados ordenados por probabilidad de éxito
        """
        estudiante = modelo_siga.estudiantes.get(documento)
        if not estudiante:
            return []
        
        # Cursos no matriculados
        cursos_disponibles = [c for c in modelo_siga.cursos.keys() 
                             if c not in estudiante.cursos]
        
        recomendaciones = []
        for codigo_curso in cursos_disponibles:
            try:
                pred = predictor.predecir(modelo_siga, documento, codigo_curso)
                recomendaciones.append({
                    'curso': codigo_curso,
                    'nombre': modelo_siga.cursos[codigo_curso].nombre,
                    'probabilidad_exito': pred['probabilidad_aprobar'],
                    'nivel_dificultad': 'Fácil' if pred['probabilidad_aprobar'] > 0.7 
                                       else 'Medio' if pred['probabilidad_aprobar'] > 0.5 
                                       else 'Difícil'
                })
            except Exception:
                pass
        
        return sorted(recomendaciones, key=lambda x: x['probabilidad_exito'], reverse=True)