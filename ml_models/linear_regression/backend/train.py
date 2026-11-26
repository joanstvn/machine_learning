import joblib
from pathlib import Path
import numpy as np
from sklearn.linear_model import LinearRegression

# Predecir precios de viviendas segun la superficie en m2

# Datos de entrenamiento
x = np.array([[70], [80], [90], [100], [110], [120], [130], [140], [150]])
y = np.array([420000000, 800000000,900000000, 1500000000, 1800000000, 2100000000, 2400000000, 2700000000, 3000000000])

# Entrenar el modelo de regresión lineal
model = LinearRegression()
model.fit(x, y)

# Guardar (serializar) el modelo entrenado en un archivo 
BASE_DIR = Path(__file__).resolve().parent 
MODEL_PATH = BASE_DIR / "model/linear_model.joblib"

joblib.dump(model, MODEL_PATH)