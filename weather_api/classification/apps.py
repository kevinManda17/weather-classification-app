from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class ClassificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'classification'
    
    def ready(self):
        """Charger les modèles au démarrage de l'application"""
        try:
            from .utils import load_models
            if load_models():
                logger.info("✅ Modèles chargés avec succès au démarrage")
            else:
                logger.error("Erreur lors du chargement des modèles")
        except Exception as e:
            logger.error(f"Erreur lors du chargement des modèles: {e}")