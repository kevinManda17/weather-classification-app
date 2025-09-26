from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField(
        max_length=None, 
        allow_empty_file=False, 
        help_text="Image météo à analyser"
    )

class TabularDataSerializer(serializers.Serializer):
    wind_speed = serializers.FloatField(
        min_value=0.0, max_value=200.0, 
        help_text="Vitesse du vent (km/h)"
    )
    precipitation = serializers.FloatField(
        min_value=0.0, max_value=100.0,
        help_text="Précipitation (%)"
    )
    temperature = serializers.FloatField(
        min_value=-50.0, max_value=60.0,
        help_text="Température (°C)"
    )
    humidity = serializers.FloatField(
        min_value=0.0, max_value=100.0,
        help_text="Humidité (%)"
    )
    pressure = serializers.FloatField(
        min_value=800.0, max_value=1100.0,
        help_text="Pression atmosphérique (hPa)"
    )
    solar_radiation = serializers.ChoiceField(
        choices=[(0, 'Faible'), (1, 'Modéré'), (2, 'Élevé')],
        help_text="Rayonnement solaire"
    )
    cloud_cover = serializers.FloatField(
        min_value=0.0, max_value=100.0,
        help_text="Couverture nuageuse (%)"
    )
    visibility = serializers.FloatField(
        min_value=0.0, max_value=50.0,
        help_text="Visibilité (km)"
    )
    dew_point = serializers.FloatField(
        min_value=-30.0, max_value=30.0,
        help_text="Point de rosée (°C)"
    )
    uv_index = serializers.FloatField(
        min_value=0.0, max_value=12.0,
        help_text="Indice UV"
    )
    
    def to_internal_value(self, data):
        # Mapping des noms de champs
        field_mapping = {
            'wind_speed': 'Wind Speed',
            'precipitation': 'Precipitation (%)',
            'temperature': 'Temperature',
            'humidity': 'Humidity',
            'pressure': 'Pressure',
            'solar_radiation': 'Solar Radiation',
            'cloud_cover': 'Cloud Cover',
            'visibility': 'Visibility',
            'dew_point': 'Dew Point',
            'uv_index': 'UV Index'
        }
        
        # Convertir pour le modèle
        model_data = {}
        for field, model_field in field_mapping.items():
            model_data[model_field] = data.get(field, 0.0)
        
        return model_data

class PredictionResultSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    prediction = serializers.CharField()
    confidence = serializers.FloatField(required=False)
    advice = serializers.DictField()
    error = serializers.CharField(required=False, allow_blank=True)
    model = serializers.CharField()
    all_predictions = serializers.DictField(required=False)
    features_used = serializers.ListField(required=False)