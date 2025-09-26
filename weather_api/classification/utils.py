import os
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import logging

logger = logging.getLogger(__name__)

# --- Classes CNN ---
CNN_CLASSES = {
    0: "Shine",
    1: "Cloudy", 
    2: "Foggy",
    3: "Lightning",
    4: "Rainbow",
    5: "Rainy",
    6: "Rime",
    7: "Sandstorm",
    8: "Sunrise"
}

# --- Conseils météo ---
WEATHER_ADVICE = {
    "Shine": {
        "agriculture": "Irrigation recommandée si le sol est sec",
        "solar": "Production solaire optimale",
        "general": "Temps ensoleillé idéal pour les activités extérieures"
    },
    "Cloudy": {
        "agriculture": "Irrigation possible si nécessaire",
        "solar": "Production solaire réduite",
        "general": "Ciel couvert, temps stable"
    },
    "Foggy": {
        "agriculture": "Risque de maladies cryptogamiques, surveiller les cultures",
        "solar": "Production solaire quasi nulle",
        "general": "Brouillard, prudence pour les déplacements"
    },
    "Lightning": {
        "agriculture": "Attention aux orages violents, protéger les équipements",
        "solar": "Production solaire interrompue",
        "general": "Orages, éviter les activités extérieures"
    },
    "Rainbow": {
        "agriculture": "Temps agréable après la pluie, humidité modérée",
        "solar": "Production solaire variable",
        "general": "Arc-en-ciel, temps en amélioration"
    },
    "Rainy": {  
        "agriculture": "Bonne pour les cultures, inutile d'irriguer",
        "solar": "Production solaire faible",
        "general": "Pluie, prévoir un parapluie"
    },
    "Rime": {
        "agriculture": "Risque de gel, protéger les cultures sensibles",
        "solar": "Production solaire faible mais ciel dégagé",
        "general": "Gel blanc, routes potentiellement glissantes"
    },
    "Sandstorm": {
        "agriculture": "Risque de dégâts sur les cultures, protéger si possible",
        "solar": "Production solaire perturbée par la poussière",
        "general": "Tempête de sable, protéger les voies respiratoires"
    },
    "Sunrise": {
        "agriculture": "Bonne pour démarrer les activités agricoles",
        "solar": "Production solaire modérée",
        "general": "Lever de soleil, belle journée en perspective"
    }
}

WEATHER_ADVICE_TAB = {
    "Cloudy": {
        "agriculture": "Irrigation possible si nécessaire",
        "solar": "Production solaire réduite",
        "general": "Temps couvert mais stable"
    },
    "Rainy": {  
        "agriculture": "Bonne pour les cultures, inutile d'irriguer",
        "solar": "Production solaire faible",
        "general": "Prévoir des vêtements de pluie"
    },
    "Snowy": {
        "agriculture": "Risque de gel, protéger les cultures sensibles",
        "solar": "Production solaire faible mais ciel dégagé",
        "general": "Neige, routes difficiles"
    },
    "Sunny": {
        "agriculture": "Bonne pour démarrer les activités agricoles",
        "solar": "Production solaire modérée",
        "general": "Temps ensoleillé idéal"
    }
}

# --- Features attendues pour le modèle tabulaire ---
FEATURES = [
    "Wind Speed",
    "Precipitation (%)",
    "Temperature",
    "Humidity",
    "Pressure",
    "Solar Radiation",
    "Cloud Cover",
    "Visibility",
    "Dew Point",
    "UV Index"
]

class WeatherModelManager:
    def __init__(self):
        self.cnn_model = None
        self.tabular_model = None
        self.loaded = False
    
    def load_models(self):
        """Charger les modèles depuis les fichiers"""
        try:
            # Chemin vers les modèles
            base_dir = os.path.dirname(os.path.dirname(__file__))
            cnn_path = os.path.join(base_dir, 'models', 'cnn_model.h5')
            tabular_path = os.path.join(base_dir, 'models', 'tabular_model.pkl')
            
            # Charger le modèle CNN
            if os.path.exists(cnn_path):
                self.cnn_model = load_model(cnn_path)
                logger.info("Modèle CNN chargé avec succès")
            else:
                logger.warning(f"Fichier modèle CNN non trouvé: {cnn_path}")
            
            # Charger le modèle tabulaire
            if os.path.exists(tabular_path):
                self.tabular_model = joblib.load(tabular_path)
                logger.info("Modèle tabulaire chargé avec succès")
            else:
                logger.warning(f"Fichier modèle tabulaire non trouvé: {tabular_path}")
            
            self.loaded = True
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement des modèles: {e}")
            return False
    
    def prepare_image(self, img, target_size=(128, 128)):
        """Préparer l'image pour le modèle CNN"""
        try:
            # Si c'est un fichier uploadé
            if hasattr(img, 'read'):
                img = Image.open(img)
            
            # Redimensionner et convertir
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img = img.resize(target_size)
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.0
            
            return img_array
            
        except Exception as e:
            logger.error(f"Erreur préparation image: {e}")
            raise
    
    def predict_cnn(self, image_file):
        """Prédiction avec le modèle CNN"""
        if not self.cnn_model:
            raise Exception("Modèle CNN non chargé")
        
        try:
            img_array = self.prepare_image(image_file)
            predictions = self.cnn_model.predict(img_array, verbose=0)
            pred_index = np.argmax(predictions[0])
            pred_class = CNN_CLASSES.get(pred_index, "Unknown")
            
            return {
                "prediction": pred_class,
                "confidence": float(predictions[0][pred_index]),
                "all_predictions": {
                    CNN_CLASSES.get(i, f"Class_{i}"): float(conf) 
                    for i, conf in enumerate(predictions[0])
                },
                "advice": WEATHER_ADVICE.get(pred_class, {})
            }
            
        except Exception as e:
            logger.error(f"Erreur prédiction CNN: {e}")
            raise
    
    def predict_tabular(self, data):
        """Prédiction avec le modèle tabulaire"""
        if not self.tabular_model:
            raise Exception("Modèle tabulaire non chargé")
        
        try:
            # Préparer les features dans le bon ordre
            X_input = [data.get(feat, 0.0) for feat in FEATURES]
            X_input = np.array([X_input])
            
            prediction = self.tabular_model.predict(X_input)[0]
            pred_class = str(prediction)
            
            return {
                "prediction": pred_class,
                "advice": WEATHER_ADVICE_TAB.get(pred_class, {}),
                "features_used": FEATURES
            }
            
        except Exception as e:
            logger.error(f"Erreur prédiction tabulaire: {e}")
            raise

# Instance globale
weather_model_manager = WeatherModelManager()

def load_models():
    """Fonction pour charger les modèles au démarrage"""
    return weather_model_manager.load_models()