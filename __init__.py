"""
Simulateur de Trafic Routier Intelligent

Un package Python pour modéliser et simuler un réseau routier intelligent.
Ce package permet de créer des routes, intersections, véhicules et de simuler
la circulation avec analyse des performances.

Sous-modules:
- models: Classes de base (Véhicule, Route, Réseau)
- core: Moteur de simulation et analyse
- io_utils: Affichage et export des données
- tests: Tests unitaires
- data: Fichiers de configuration

Exemple d'utilisation:
    >>> from simulateur_trafic.core.simulateur import Simulateur
    >>> simu = Simulateur("data/config_reseau.json")
    >>> simu.lancer_simulation(60, 60)

Auteur: Aya Zid
Version: 1.0.0
Licence: MIT
"""

__version__ = "1.0.0"
__author__ = "Aya Zid"
__email__ = "azid28278@gmail.com"
__license__ = "MIT"

# Import des classes principales pour faciliter l'accès
from models.vehicule import Vehicule
from models.route import Route
from models.reseau import ReseauRoutier
from core.simulateur import Simulateur
from core.analyseur import Analyseur
from io_utils.affichage import Affichage
from io_utils.export import Export

__all__ = [
    "Vehicule",
    "Route", 
    "ReseauRoutier",
    "Simulateur",
    "Analyseur",
    "Affichage",
    "Export"
]