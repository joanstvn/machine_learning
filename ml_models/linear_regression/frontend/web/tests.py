from django.test import SimpleTestCase, Client
from web.services import TRAINING_DATA, predict_price


class LinearRegressionFrontendTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_index_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Joan Stiven Rios Valderrama')
        self.assertContains(response, 'Análisis y Desarrollo de Software')
        self.assertContains(response, '3494620')
        self.assertContains(response, 'Predicción de precio')

    def test_index_post_prediction(self):
        response = self.client.post('/', {'metros_cuadrados': '100'})
        self.assertEqual(response.status_code, 200)
        # Para 100 m², el resultado principal debe ser la predicción del modelo: 1.408.555.556
        self.assertContains(response, '1.408.555.556')
        # Y la tarjeta informativa de entrenamiento muestra el valor real registrado: 1.500.000.000
        self.assertContains(response, '1.500.000.000')

    def test_predict_api_with_training_values(self):
        for item in TRAINING_DATA:
            m2 = item['metros']
            response = self.client.get(f'/api/predict/?metros_cuadrados={m2}')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data['es_entrenamiento'])
            self.assertEqual(data['precio_real'], item['precio'])
            self.assertIn('precio_formateado', data)

    def test_predict_api_custom_value(self):
        response = self.client.get('/api/predict/?metros_cuadrados=95')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['es_entrenamiento'])
        self.assertGreater(data['precio_estimado'], 0)

    def test_predict_api_invalid_value(self):
        response = self.client.get('/api/predict/?metros_cuadrados=-10')
        self.assertEqual(response.status_code, 400)

    def test_model_api(self):
        response = self.client.get('/api/model/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ready')
