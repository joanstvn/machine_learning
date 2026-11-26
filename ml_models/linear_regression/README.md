# Predicción de precios de vivienda · Regresión lineal

Proyecto Full-Stack estructurado con separación estricta entre **Backend** (FastAPI + scikit-learn) y **Frontend** (Django + Vanilla JS y CSS nativo), listo para desarrollo local y despliegue en **Railway**.

## Datos del proyecto

- **Aprendiz:** Joan Stiven Rios Valderrama
- **Programa:** Análisis y Desarrollo de Software
- **Ficha:** 3494620
- **Ecuación del modelo:** $y = mx + b$ ($y \approx 32.700.000x - 1.861.444.444$)

---

## Estructura del proyecto

El repositorio está dividido estrictamente en dos carpetas independientes:

```text
linear_regression/
├── backend/                  # TODO EL BACKEND (API & Machine Learning)
│   ├── main.py              # API FastAPI con /predict, /model y /training-data
│   ├── train.py             # Script de entrenamiento scikit-learn
│   ├── model/
│   │   └── linear_model.joblib # Modelo serializado
│   ├── requirements.txt     # Dependencias de Python para el backend
│   ├── Dockerfile           # Imagen Docker para el backend
│   ├── Procfile             # Comando de inicio para Railway (uvicorn)
│   └── railway.json         # Configuración de despliegue en Railway
│
└── frontend/                 # TODO EL FRONTEND (Django)
    ├── manage.py            # CLI oficial de Django para el frontend
    ├── config/              # Configuración Django (settings, urls, wsgi)
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── web/                 # Aplicación Django (vistas, servicios y pruebas)
    │   ├── views.py
    │   ├── services.py      # Cliente que consulta el backend API
    │   ├── urls.py
    │   └── tests.py
    ├── templates/           # Templates HTML con el diseño original
    │   └── frontend/
    │       └── index.html
    ├── static/              # Estilos CSS y JavaScript interactivo
    │   └── frontend/
    │       ├── css/
    │       └── js/
    ├── requirements.txt     # Dependencias de Python para el frontend
    ├── Dockerfile           # Imagen Docker para el frontend
    ├── Procfile             # Comando de inicio para Railway (gunicorn)
    └── railway.json         # Configuración de despliegue en Railway
```

---

## Valores de entrenamiento del backend

El backend expone en `GET /training-data` los 9 valores con los que se entrenó el modelo:

| Superficie ($m^2$) | Precio real (COP) | Predicción del modelo (COP) |
| :---: | :---: | :---: |
| **70** | $ 420.000.000 | $ 427.555.556 |
| **80** | $ 800.000.000 | $ 754.555.556 |
| **90** | $ 900.000.000 | $ 1.081.555.556 |
| **100** | $ 1.500.000.000 | $ 1.408.555.556 |
| **110** | $ 1.800.000.000 | $ 1.735.555.556 |
| **120** | $ 2.100.000.000 | $ 2.062.555.556 |
| **130** | $ 2.400.000.000 | $ 2.389.555.556 |
| **140** | $ 2.700.000.000 | $ 2.716.555.556 |
| **150** | $ 3.000.000.000 | $ 3.043.555.556 |

### Funcionalidades del buscador en el frontend:
- **Autocompletado (`<datalist>`):** Sugiere automáticamente los metros cuadrados del dataset con su precio real registrado.
- **Chips interactivos:** Botones rápidos de $70 \text{ m}^2$ a $150 \text{ m}^2$ para consultar de un toque.
- **Comparación real vs. predicción:** Resalta si la superficie consultada pertenece al set de entrenamiento del backend, indicando la diferencia en pesos colombianos.
- **Gráfico SVG:** Grafica los 9 puntos de entrenamiento y el punto consultado en tiempo real.

---

## Ejecución en modo desarrollo (Local)

### 1. Terminal 1: Iniciar Backend

```bash
cd backend
pip install -r requirements.txt
python train.py                 # Si necesitas entrenar/regenerar el modelo
uvicorn main:app --reload --port 8001
```

La API y la documentación interactiva Swagger quedarán en:
- API: <http://127.0.0.1:8001>
- Docs: <http://127.0.0.1:8001/docs>

### 2. Terminal 2: Iniciar Frontend (Django)

```bash
cd frontend
pip install -r requirements.txt
python manage.py runserver 8000
```

Abre en tu navegador:
👉 **<http://127.0.0.1:8000>**

*(El frontend se comunicará automáticamente con `http://127.0.0.1:8001` para predecir precios).*

---

## Despliegue en Railway (Dos Servicios)

Cada carpeta cuenta con su propio `Dockerfile`, `Procfile`, `railway.json` y `requirements.txt`.

### Paso 1: Desplegar el Backend en Railway
1. En [railway.app](https://railway.app), crea un nuevo proyecto desde tu repositorio GitHub.
2. En la configuración del servicio (**Settings**):
   - **Root Directory:** `/backend`
3. En **Networking** > **Generate Domain**, genera tu dominio público (ej: `https://mi-backend.up.railway.app`).

### Paso 2: Desplegar el Frontend (Django) en Railway
1. En el mismo proyecto de Railway, haz clic en **+ New** > **GitHub Repo** (selecciona el mismo repositorio).
2. En la configuración de este segundo servicio (**Settings**):
   - **Root Directory:** `/frontend`
3. En **Variables**, agrega la variable de entorno para conectar con el backend:
   - `BACKEND_API_URL` = `https://mi-backend.up.railway.app`
4. En **Networking** > **Generate Domain**, genera el dominio para el frontend (ej: `https://mi-frontend.up.railway.app`).

¡Front y Back quedarán desplegados de forma totalmente independiente y comunicados entre sí!
