# Clasificación de condiciones médicas con Random Forest

Proyecto académico de aprendizaje automático que utiliza un clasificador Random Forest para explorar la clasificación de cinco categorías: infarto, neumonía, gripe, ansiedad y gastroenteritis. Incluye la generación de un dataset sintético, el entrenamiento y evaluación del modelo, y una aplicación interactiva construida con Streamlit.

## Datos del proyecto

- **Aprendiz:** Joan Stiven Rios Valderrama
- **Programa:** Análisis y Desarrollo de Software
- **Ficha:** 3494620

> **Aviso:** los datos son sintéticos y esta aplicación no es una herramienta médica. No uses sus predicciones ni recomendaciones para diagnosticar o tratar a una persona.

## Estructura

```text
random_forest/
├── 1.Crear_dataset.py          # Genera el dataset sintético
├── 2.Entrenar_modelo.py        # Entrena, evalúa y guarda el clasificador
├── 3.Predecir_enfermedad.py    # Interfaz de predicción con Streamlit
├── README.md
├── data/
│   └── dataset_medico_ampliado.csv  # 5.000 registros generados
├── models/
│   └── modelo_random_forest_ampliado.pkl  # Modelo entrenado
└── requirements.txt             # Dependencias
```

## Datos y modelo

El dataset contiene 5.000 registros sintéticos, 34 variables de entrada y una columna objetivo llamada `diagnostico`. Las variables representan datos demográficos, signos vitales, factores de riesgo y síntomas. El generador usa una semilla fija para que la creación de datos sea reproducible.

El entrenamiento separa los datos en conjuntos de entrenamiento y prueba (70 % / 30 %) mediante una partición estratificada. El clasificador usa 200 árboles y reporta exactitud, métricas por clase, matriz de confusión e importancia de variables. Al finalizar, guarda el modelo serializado en `models/modelo_random_forest_ampliado.pkl`.

La aplicación permite ingresar valores clínicos simulados y muestra la clase estimada, la distribución de probabilidades del modelo, además de mensajes y recomendaciones predefinidos para cada categoría. Estos resultados son demostrativos y no han sido validados para uso clínico.

## Tecnologías

- Python
- pandas y NumPy para la preparación y generación de datos
- scikit-learn para el entrenamiento y evaluación
- joblib para guardar y cargar el modelo
- Streamlit y Plotly para la interfaz y visualizaciones

## Requisitos

- Python 3
- pip

## Instalación y ejecución

Ejecuta los comandos desde este directorio:

```bash
python -m venv .venv
```

Activa el entorno virtual:

```bash
# Linux o macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Generar los datos y entrenar el modelo

El repositorio incluye un dataset y un modelo entrenado, así que puedes iniciar la aplicación directamente. Si quieres regenerar los datos o entrenar el modelo de nuevo, ejecuta los scripts en este orden:

```bash
python 1.Crear_dataset.py
python 2.Entrenar_modelo.py
```

El primer script reemplaza `data/dataset_medico_ampliado.csv`; el segundo carga ese archivo y reemplaza el modelo guardado.

## Iniciar la aplicación

Desde el directorio del proyecto, ejecuta:

```bash
streamlit run 3.Predecir_enfermedad.py
```

Streamlit mostrará en la terminal la dirección local para abrir la aplicación en el navegador. La aplicación carga el modelo desde `models/modelo_random_forest_ampliado.pkl`; si no existe, primero ejecuta el entrenamiento.
