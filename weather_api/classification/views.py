from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
import logging

from .utils import weather_model_manager, WEATHER_ADVICE, CNN_CLASSES
from .serializers import ImageUploadSerializer, TabularDataSerializer, PredictionResultSerializer

logger = logging.getLogger(__name__)

@api_view(['GET'])
def api_overview(request):
    """Vue d'aperçu de l'API"""
    api_urls = {
        'Prédiction Image (CNN)': '/api/predict/image/',
        'Prédiction Données (Tabulaire)': '/api/predict/tabular/',
        'Test API': '/api/test/',
        'Statut Modèles': '/api/status/',
        'Classes CNN': '/api/classes/',
        'Documentation': '/api/docs/',
    }
    return Response(api_urls)

@api_view(['POST'])
def predict_image(request):
    """Prédiction à partir d'une image (CNN)"""
    serializer = ImageUploadSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': 'Image invalide ou manquante',
            'model': 'CNN'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        if not weather_model_manager.loaded:
            return Response({
                'success': False,
                'error': 'Modèles non chargés',
                'model': 'CNN'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        image_file = serializer.validated_data['image']
        result = weather_model_manager.predict_cnn(image_file)
        
        response_data = {
            'success': True,
            'model': 'CNN',
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'all_predictions': result['all_predictions'],
            'advice': result['advice'],
            'error': ''
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur prédiction image: {e}")
        return Response({
            'success': False,
            'error': str(e),
            'model': 'CNN',
            'prediction': '',
            'confidence': 0.0,
            'advice': {}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def predict_tabular(request):
    """Prédiction à partir de données tabulaires"""
    serializer = TabularDataSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'error': 'Données invalides',
            'details': serializer.errors,
            'model': 'Tabulaire'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        if not weather_model_manager.loaded:
            return Response({
                'success': False,
                'error': 'Modèles non chargés',
                'model': 'Tabulaire'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        data = serializer.validated_data
        result = weather_model_manager.predict_tabular(data)
        
        response_data = {
            'success': True,
            'model': 'Tabulaire',
            'prediction': result['prediction'],
            'advice': result['advice'],
            'features_used': result['features_used'],
            'error': ''
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Erreur prédiction tabulaire: {e}")
        return Response({
            'success': False,
            'error': str(e),
            'model': 'Tabulaire',
            'prediction': '',
            'advice': {},
            'features_used': []
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def test_api(request):
    """Test de l'API"""
    return Response({
        'message': 'API Weather Classification Django fonctionne correctement!',
        'status': 'active',
        'models_loaded': weather_model_manager.loaded
    })

@api_view(['GET'])
def model_status(request):
    """Statut des modèles"""
    status_info = {
        'cnn_loaded': weather_model_manager.cnn_model is not None,
        'tabular_loaded': weather_model_manager.tabular_model is not None,
        'all_loaded': weather_model_manager.loaded,
        'available_classes': list(CNN_CLASSES.values())
    }
    return Response(status_info)

@api_view(['GET'])
def available_classes(request):
    """Liste des classes disponibles"""
    return Response({
        'cnn_classes': CNN_CLASSES,
        'advice_categories': list(WEATHER_ADVICE.values())[0].keys() if WEATHER_ADVICE else []
    })

@api_view(['GET'])
def api_docs(request):
    """Documentation de l'API"""
    docs = {
        'Prédiction Image': {
            'endpoint': '/api/predict/image/',
            'method': 'POST',
            'format': 'multipart/form-data',
            'parameters': {
                'image': 'Fichier image (JPEG, PNG, WebP)'
            }
        },
        'Prédiction Tabulaire': {
            'endpoint': '/api/predict/tabular/',
            'method': 'POST',
            'format': 'application/json',
            'parameters': {
                'wind_speed': 'float (0-200 km/h)',
                'precipitation': 'float (0-100 %)',
                'temperature': 'float (-50-60 °C)',
                'humidity': 'float (0-100 %)',
                'pressure': 'float (800-1100 hPa)',
                'solar_radiation': 'int (0:Faible, 1:Modéré, 2:Élevé)',
                'cloud_cover': 'float (0-100 %)',
                'visibility': 'float (0-50 km)',
                'dew_point': 'float (-30-30 °C)',
                'uv_index': 'float (0-12)'
            }
        }
    }
    return Response(docs)