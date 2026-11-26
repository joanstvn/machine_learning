import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .services import (
    PROFILE,
    TRAINING_DATA,
    BACKEND_API_URL,
    get_chart_data,
    predict_price,
)


def index_view(request):
    """Vista principal con servidor Django (SSR)."""
    error = None
    metros_input = request.POST.get('metros_cuadrados') or request.GET.get('metros_cuadrados')

    if metros_input is None:
        selected_metros = 70.0
    else:
        try:
            cleaned = str(metros_input).replace(',', '.').strip()
            selected_metros = float(cleaned)
            if selected_metros <= 0:
                error = 'Ingresa una superficie válida mayor que 0 m².'
                selected_metros = 100.0
        except ValueError:
            error = 'Por favor ingresa un número válido de metros cuadrados.'
            selected_metros = 100.0

    result = None
    if not error:
        try:
            result = predict_price(selected_metros)
        except Exception as exc:
            error = f"Error al procesar predicción: {exc}"

    chart_data = get_chart_data()

    context = {
        'profile': PROFILE,
        'training_data': TRAINING_DATA,
        'chart_data': chart_data,
        'result': result,
        'error': error,
        'selected_metros': selected_metros,
        'backend_api_url': BACKEND_API_URL,
    }
    return render(request, 'frontend/index.html', context)


@csrf_exempt
def predict_api(request):
    """Endpoint API JSON para predicciones dinámicas con vanilla JS."""
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                body = json.loads(request.body.decode('utf-8'))
                metros_raw = body.get('metros_cuadrados')
            else:
                metros_raw = request.POST.get('metros_cuadrados')
        except Exception:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
    else:
        metros_raw = request.GET.get('metros_cuadrados')

    if metros_raw is None:
        return JsonResponse({'error': 'El parámetro metros_cuadrados es requerido'}, status=400)

    try:
        cleaned = str(metros_raw).replace(',', '.').strip()
        metros = float(cleaned)
        if metros <= 0:
            return JsonResponse({'error': 'La superficie debe ser mayor que 0 m²'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Superficie numérica no válida'}, status=400)

    try:
        prediction = predict_price(metros)
        return JsonResponse(prediction)
    except Exception as exc:
        return JsonResponse({'error': f'Error al calcular la predicción: {exc}'}, status=500)


def model_api(request):
    """Endpoint API JSON con el estado del modelo y backend."""
    return JsonResponse({
        'status': 'ready',
        'backend_api_url': BACKEND_API_URL,
        'formula': 'y = 32.700.000x - 1.861.444.444',
    })
