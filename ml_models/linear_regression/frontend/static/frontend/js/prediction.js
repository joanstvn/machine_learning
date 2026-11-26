document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('prediction-form');
  const input = document.getElementById('metros-cuadrados');
  const button = document.getElementById('prediction-button');
  const priceDisplay = document.getElementById('prediction-price');
  const hintDisplay = document.getElementById('prediction-hint');
  const errorBox = document.getElementById('prediction-error-box');
  const errorText = document.getElementById('prediction-error-text');
  const currentChartPoint = document.getElementById('chart-current-point');
  const chips = document.querySelectorAll('.training-chip');
  const trainingCard = document.getElementById('training-match-card');
  const trainingRealPrice = document.getElementById('training-real-price');
  const trainingDiff = document.getElementById('training-diff');

  function updateActiveChip(value) {
    const num = parseFloat(String(value).replace(',', '.'));
    chips.forEach((chip) => {
      const chipM2 = parseFloat(chip.dataset.m2);
      if (Math.abs(chipM2 - num) < 0.001) {
        chip.classList.add('is-active');
      } else {
        chip.classList.remove('is-active');
      }
    });
  }

  function hideError() {
    if (errorBox) {
      errorBox.style.display = 'none';
      errorText.textContent = '';
    }
  }

  function showError(msg) {
    if (errorBox) {
      errorText.textContent = msg;
      errorBox.style.display = 'flex';
    }
  }

  async function performPrediction(metrosValue) {
    const raw = String(metrosValue).replace(',', '.').trim();
    const val = parseFloat(raw);

    if (isNaN(val) || val <= 0) {
      showError('Ingresa una superficie válida mayor que 0 m².');
      return;
    }

    hideError();
    updateActiveChip(val);

    const originalBtnText = button.textContent;
    button.disabled = true;
    button.textContent = 'Calculando…';

    try {
      const response = await fetch(`/api/predict/?metros_cuadrados=${encodeURIComponent(val)}`, {
        headers: {
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.error || `Error ${response.status} en la predicción`);
      }

      const data = await response.json();

      // Actualizar el precio y descripción
      if (priceDisplay) {
        priceDisplay.textContent = data.precio_formateado;
      }
      if (hintDisplay) {
        hintDisplay.textContent = `Para una vivienda de ${data.metros_formateado} m²`;
      }

      // Actualizar tarjeta comparativa si es valor de entrenamiento
      if (trainingCard) {
        if (data.es_entrenamiento && data.precio_real_formateado) {
          if (trainingRealPrice) trainingRealPrice.textContent = data.precio_real_formateado;
          if (trainingDiff) trainingDiff.textContent = data.diferencia_formateada || '';
          trainingCard.classList.remove('is-hidden');
        } else {
          trainingCard.classList.add('is-hidden');
        }
      }

      // Actualizar coordenada del punto en el gráfico SVG
      if (currentChartPoint && data.cx != null && data.cy != null) {
        currentChartPoint.setAttribute('cx', data.cx);
        currentChartPoint.setAttribute('cy', data.cy);
        currentChartPoint.style.display = 'block';
      }
    } catch (err) {
      showError(err.message || 'Error al comunicarse con el servidor Django.');
    } finally {
      button.disabled = false;
      button.textContent = originalBtnText;
    }
  }

  // Evento submit del formulario (intercepción con vanilla JS)
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      performPrediction(input.value);
    });
  }

  // Evento al escribir en el input
  if (input) {
    input.addEventListener('input', () => {
      updateActiveChip(input.value);
    });
  }

  // Eventos al hacer click en los chips de valores de entrenamiento
  chips.forEach((chip) => {
    chip.addEventListener('click', () => {
      const m2 = chip.dataset.m2;
      if (input) {
        input.value = m2;
      }
      performPrediction(m2);
    });
  });

  // Inicializar estado de chip activo
  if (input && input.value) {
    updateActiveChip(input.value);
  }
});
