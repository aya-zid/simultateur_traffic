"""
Configuration partagée pour les tests pytest

Ce module contient les fixtures partagées pour éviter la duplication
du code d'initialisation dans les tests.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from models.vehicule import Vehicule
from models.route import Route
from models.reseau import ReseauRoutier

@pytest.fixture
def route_simple():
    """Crée une route simple pour les tests."""
    return Route("A1", longueur=1000, limite_vitesse=50)


@pytest.fixture
def route_longue():
    """Crée une route longue pour les tests."""
    return Route("Autoroute_A2", longueur=5000, limite_vitesse=130)


@pytest.fixture
def vehicule_exemple(route_simple):
    """Crée un véhicule exemple sur une route simple."""
    return Vehicule(identifiant=1, route_actuelle=route_simple.nom, position=0, vitesse=30)


@pytest.fixture
def vehicule_avance(route_simple):
    """Crée un véhicule avancé sur une route."""
    return Vehicule(identifiant=2, route_actuelle=route_simple.nom, position=500, vitesse=40)


@pytest.fixture
def reseau_simple(route_simple, vehicule_exemple):
    """Crée un réseau simple avec une route et un véhicule."""
    reseau = ReseauRoutier()
    reseau.ajouter_route(route_simple)
    route_simple.ajouter_vehicule(vehicule_exemple)
    return reseau


@pytest.fixture
def reseau_complexe(route_simple, route_longue, vehicule_exemple, vehicule_avance):
    """Crée un réseau complexe avec plusieurs routes et véhicules."""
    reseau = ReseauRoutier()
    
    # Ajouter les routes
    reseau.ajouter_route(route_simple)
    reseau.ajouter_route(route_longue)
    
    # Ajouter les véhicules
    route_simple.ajouter_vehicule(vehicule_exemple)
    route_longue.ajouter_vehicule(vehicule_avance)
    
    # Créer des intersections
    reseau.ajouter_intersection("A1", "Autoroute_A2")
    reseau.ajouter_intersection("Autoroute_A2", "A1")
    
    return reseau


@pytest.fixture
def vehicule_pres_fin_route(route_simple):
    """Crée un véhicule près de la fin d'une route."""
    return Vehicule(identifiant=3, route_actuelle=route_simple.nom, position=950, vitesse=30)

@pytest.fixture
def config_file_simple():
    """Crée un fichier de configuration simple pour les tests."""
    import tempfile
    import json
    import os
    
    config_data = {
        "routes": [
            {
                "nom": "Route_Test_A",
                "longueur": 1500,
                "limite_vitesse": 60
            },
            {
                "nom": "Route_Test_B", 
                "longueur": 2000,
                "limite_vitesse": 80
            }
        ],
        "intersections": [
            {
                "source": "Route_Test_A",
                "destinations": ["Route_Test_B"]
            }
        ],
        "vehicules": [
            {
                "id": 1,
                "route": "Route_Test_A",
                "position": 0,
                "vitesse": 45
            },
            {
                "id": 2,
                "route": "Route_Test_B", 
                "position": 500,
                "vitesse": 65
            }
        ]
    }
    
    # Créer un fichier temporaire
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f, indent=2)
        temp_config_file = f.name
    
    yield temp_config_file
    
    # Nettoyer après le test
    if os.path.exists(temp_config_file):
        os.unlink(temp_config_file)


@pytest.fixture
def analyseur_simple(reseau_simple):
    """Crée un analyseur avec un réseau simple."""
    from core.analyseur import Analyseur
    return Analyseur(reseau_simple)


@pytest.fixture  
def simulateur_simple(reseau_simple):
    """Crée un simulateur avec un réseau simple."""
    from core.simulateur import Simulateur
    simulateur = Simulateur()
    simulateur.reseau = reseau_simple
    return simulateur