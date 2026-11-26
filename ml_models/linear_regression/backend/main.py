from pathlib import Path
import joblib
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.linear_model import LinearRegression

app = FastAPI(
    title="Linear Regression ML Backend API",
    description="API para estimación de precios inmobiliarios",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "linear_model.joblib"

TRAINING_X = [70, 80, 90, 100, 110, 120, 130, 140, 150]
TRAINING_Y = [
    420_000_000,
    800_000_000,
    900_000_000,
    1_500_000_000,
    1_800_000_000,
    2_100_000_000,
    2_400_000_000,
    2_700_000_000,
    3_000_000_000,
]


def load_or_train_model():
    """Carga el modelo serializado o lo entrena si no existe."""
    if MODEL_PATH.exists():
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            pass

    x = np.array([[m] for m in TRAINING_X])
    y = np.array(TRAINING_Y)
    m = LinearRegression()
    m.fit(x, y)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(m, MODEL_PATH)
    return m


model = load_or_train_model()


class PredictionRequest(BaseModel):
    metros_cuadrados: float = Field(gt=0, description="Superficie en metros cuadrados")


@app.post("/predict")
def predict(request: PredictionRequest):
    global model
    if model is None:
        model = load_or_train_model()

    superficie = np.array([[request.metros_cuadrados]])
    prediction = float(model.predict(superficie)[0])

    return {"precio": prediction}

