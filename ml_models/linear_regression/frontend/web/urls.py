from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('predict/', views.predict_api, name='predict'),
    path('api/predict/', views.predict_api, name='api_predict'),
    path('model/', views.model_api, name='model_status'),
    path('api/model/', views.model_api, name='api_model_status'),
]
