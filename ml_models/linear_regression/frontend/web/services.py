import json
import math
import os
import urllib.request
import urllib.error
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOCAL_MODEL_PATH = BASE_DIR.parent / 'backend' / 'model' / 'linear_model.joblib'
BACKEND_API_URL = os.environ.get('BACKEND_API_URL', 'http://127.0.0.1:8001').rstrip('/')

PROFILE = {
    'name': 'Joan Stiven Rios Valderrama',
    'program': 'Análisis y Desarrollo de Software',
    'ficha': '3494620',
    'eyebrow': 'Proyecto de Machine Learning',
    'subtitle': 'Predicción de precios de vivienda con regresión lineal',
}

# Datos reales de entrenamiento registrados en backend/train.py
RAW_TRAINING_X = [70, 80, 90, 100, 110, 120, 130, 140, 150]
RAW_TRAINING_Y = [
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

TRAINING_DATA = [
    {'metros': x, 'precio': y}
    for x, y in zip(RAW_TRAINING_X, RAW_TRAINING_Y)
]

SVG_CONFIG = {
    'x_min': 70,
    'x_max': 160,
    'y_min': 420_000_000,
    'y_max': 3_200_000_000,
    'svg_x_start': 56.0,
    'svg_x_end': 320.0,
    'svg_y_start': 296.0,
    'svg_y_end': 80.0,
}


def map_to_svg(metros: float, precio: float) -> tuple[str, str]:
    """Mapea metros y precio a coordenadas (cx, cy) para el SVG.
    Devuelve strings con punto decimal para evitar localización es-co."""
    x_span = SVG_CONFIG['x_max'] - SVG_CONFIG['x_min']
    y_span = SVG_CONFIG['y_max'] - SVG_CONFIG['y_min']
    svg_w = SVG_CONFIG['svg_x_end'] - SVG_CONFIG['svg_x_start']
    svg_h = SVG_CONFIG['svg_y_start'] - SVG_CONFIG['svg_y_end']

    cx = SVG_CONFIG['svg_x_start'] + ((metros - SVG_CONFIG['x_min']) / x_span) * svg_w
    cy = SVG_CONFIG['svg_y_start'] - ((precio - SVG_CONFIG['y_min']) / y_span) * svg_h
    return f"{cx:.1f}", f"{cy:.1f}"


def format_currency_cop(value: float) -> str:
    """Formatea valores monetarios en COP."""
    rounded = int(round(value))
    formatted = f"{rounded:,}".replace(',', '.')
    return f"$ {formatted} COP"


def format_area_m2(value: float) -> str:
    """Formatea la superficie."""
    if value == int(value):
        return f"{int(value)}"
    return f"{value:.1f}".replace('.', ',')


def fetch_backend_prediction(metros: float) -> float | None:
    """Consulta el endpoint POST /predict del backend."""
    url = f"{BACKEND_API_URL}/predict"
    payload = json.dumps({'metros_cuadrados': metros}).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=payload,
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
    )
    try:
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return float(data.get('precio'))
    except Exception:
        return None


def get_local_model_prediction(metros: float) -> float:
    """Calcula la predicción directamente con la fórmula o el modelo local."""
    # Coeficientes calculados en entrenamiento:
    # m = 32,700,000, b = -1,861,444,444.4444
    if LOCAL_MODEL_PATH.exists():
        try:
            import joblib
            import numpy as np
            model = joblib.load(LOCAL_MODEL_PATH)
            return float(model.predict(np.array([[metros]]))[0])
        except Exception:
            pass
    # Fórmula exacta de regresión
    return float(32_700_000.0 * metros - 1_861_444_444.4444435)


def predict_price(metros_cuadrados: float) -> dict:
    """Predice el precio usando el backend o el modelo de regresión lineal local."""
    # 1. Intentar predecir desde el backend
    pred_val = fetch_backend_prediction(metros_cuadrados)
    origen = 'backend_api'

    # 2. Si el backend está apagado o no responde, usar modelo local/fórmula
    if pred_val is None:
        pred_val = get_local_model_prediction(metros_cuadrados)
        origen = 'modelo_local'

    match = None
    for item in TRAINING_DATA:
        if math.isclose(item['metros'], metros_cuadrados, rel_tol=1e-5):
            match = item
            break

    # Coordenada del punto en el SVG sobre la recta de regresión
    cx, cy = map_to_svg(metros_cuadrados, pred_val)

    result = {
        'metros_cuadrados': metros_cuadrados,
        'metros_formateado': format_area_m2(metros_cuadrados),
        'precio_estimado': pred_val,
        'precio_formateado': format_currency_cop(pred_val),
        'es_entrenamiento': match is not None,
        'origen': origen,
        'backend_url': BACKEND_API_URL,
        'cx': cx,
        'cy': cy,
    }

    if match:
        precio_real = match['precio']
        diff = pred_val - precio_real
        result['precio_real'] = precio_real
        result['precio_real_formateado'] = format_currency_cop(precio_real)
        result['diferencia'] = diff
        sign = '+' if diff > 0 else '-'
        result['diferencia_formateada'] = f"{sign} {format_currency_cop(abs(diff))}"

    return result


def get_chart_data():
    """Genera datos del gráfico SVG."""
    slope = 32_700_000.0
    intercept = -1_861_444_444.4444435

    points = []
    for item in TRAINING_DATA:
        cx, cy = map_to_svg(item['metros'], item['precio'])
        points.append({
            'metros': item['metros'],
            'precio_real': item['precio'],
            'precio_real_formateado': format_currency_cop(item['precio']),
            'cx': cx,
            'cy': cy,
        })

    x_start, x_end = 70, 155
    y_start = slope * x_start + intercept
    y_end = slope * x_end + intercept
    line_x1, line_y1 = map_to_svg(x_start, y_start)
    line_x2, line_y2 = map_to_svg(x_end, y_end)

    return {
        'points': points,
        'line': {'x1': line_x1, 'y1': line_y1, 'x2': line_x2, 'y2': line_y2},
    }
