from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_overview, name='api-overview'),
    path('predict/image/', views.predict_image, name='predict-image'),
    path('predict/tabular/', views.predict_tabular, name='predict-tabular'),
    path('test/', views.test_api, name='test-api'),
    path('status/', views.model_status, name='model-status'),
    path('classes/', views.available_classes, name='available-classes'),
    path('docs/', views.api_docs, name='api-docs'),
]