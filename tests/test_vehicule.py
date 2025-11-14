"""
Tests complets pour la classe Vehicule - Couverture 100%
"""

import pytest
import sys
import os
from unittest.mock import patch
from io import StringIO


from models.vehicule import Vehicule
from exceptions import PositionInvalideError, VitesseInvalideError, DistanceInvalideError


class TestVehiculeComplet:
    """
    Tests complets pour couvrir 100% de la classe Vehicule
    """
    
    def test_creation_vehicule_identifiant_negatif(self):
        """Test la création d'un véhicule avec identifiant négatif (gestion d'erreur)."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            vehicule = Vehicule(identifiant=-1, route_actuelle="Route_A", position=100, vitesse=50)
        
        # Vérifie que l'objet est créé avec des valeurs par défaut
        assert vehicule.identifiant == 0  # Doit être corrigé à 0
        assert vehicule.route_actuelle == "Route_A"
        output = mock_stdout.getvalue()
        assert "[Erreur]" in output
        assert "identifiant" in output.lower()
    
    def test_creation_vehicule_position_negative(self):
        """Test la création d'un véhicule avec position négative (gestion d'erreur)."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=-50, vitesse=50)
        
        # Vérifie que la position est corrigée à 0
        assert vehicule.position == 0
        output = mock_stdout.getvalue()
        assert "[Erreur]" in output
        assert "position" in output.lower()
    
    def test_creation_vehicule_vitesse_negative(self):
        """Test la création d'un véhicule avec vitesse négative (gestion d'erreur)."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=100, vitesse=-30)
        
        # Vérifie que la vitesse est corrigée à 0
        assert vehicule.vitesse == 0
        output = mock_stdout.getvalue()
        assert "[Erreur]" in output
        assert "vitesse" in output.lower()
    
    def test_creation_vehicule_route_none(self):
        """Test la création d'un véhicule avec route_actuelle None (gestion d'erreur)."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            vehicule = Vehicule(identifiant=-1, route_actuelle=None, position=-100, vitesse=-50)
        
        # Vérifie les valeurs par défaut
        assert vehicule.identifiant == 0
        assert vehicule.route_actuelle == "Route_Inconnue"
        assert vehicule.position == 0
        assert vehicule.vitesse == 0
        output = mock_stdout.getvalue()
        assert "[Erreur]" in output
    
    def test_avancer_distance_negative(self):
        """Test l'avancement avec distance négative (gestion d'erreur)."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=100, vitesse=50)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            vehicule.avancer(-50)
        
        # La position ne doit pas changer
        assert vehicule.position == 100
        output = mock_stdout.getvalue()
        assert "[Erreur]" in output
        assert "distance" in output.lower()
    
    def test_avancer_vitesse_negative(self):
        """Test l'avancement quand la vitesse est négative (gestion d'erreur)."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=100, vitesse=50)
        vehicule.vitesse = -10  # Forcer une vitesse négative
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            vehicule.avancer(50)
        
        # La position ne doit pas changer
        assert vehicule.position == 100
        output = mock_stdout.getvalue()
        assert "[Erreur]" in output
        assert "vitesse" in output.lower()
    

    def test_changer_de_route_nom_vide(self):
        """Test le changement de route avec un nom vide (gestion d'erreur)."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=100, vitesse=50)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            vehicule.changer_de_route("", 200)
        
        # La route et position ne doivent pas changer
        assert vehicule.route_actuelle == "Route_A"
        assert vehicule.position == 100
        output = mock_stdout.getvalue()
        assert "[Erreur]" in output
        assert "vide" in output.lower()
    
    def test_changer_de_route_position_negative(self):
        """Test le changement de route avec position négative (gestion d'erreur)."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=100, vitesse=50)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            vehicule.changer_de_route("Nouvelle_Route", -50)
        
        # La route et position ne doivent pas changer
        assert vehicule.route_actuelle == "Route_A"
        assert vehicule.position == 100
        output = mock_stdout.getvalue()
        assert "[Erreur]" in output
        assert "position" in output.lower()
    
    def test_changer_de_route_nom_none(self):
        """Test le changement de route avec nom None (gestion d'erreur)."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=100, vitesse=50)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            vehicule.changer_de_route(None, 200)
        
        # La route et position ne doivent pas changer
        assert vehicule.route_actuelle == "Route_A"
        assert vehicule.position == 100
        output = mock_stdout.getvalue()
        assert "[Erreur]" in output
    
    def test_avancer_success_scenario(self):
        """Test scenario normal d'avancement sans erreur."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=100, vitesse=50)
        
        # Pas de capture stdout car pas d'erreur attendue
        vehicule.avancer(150.75)
        
        assert vehicule.position == 250.75
    
    def test_changer_de_route_success_scenario(self):
        """Test scenario normal de changement de route sans erreur."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=100, vitesse=50)
        
        # Pas de capture stdout car pas d'erreur attendue
        vehicule.changer_de_route("Route_B", 50)
        
        assert vehicule.route_actuelle == "Route_B"
        assert vehicule.position == 50
        assert vehicule.historique_routes == ["Route_A", "Route_B"]
    
    def test_vehicule_avec_vitesse_zero(self):
        """Test le comportement avec vitesse zéro."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=100, vitesse=0)
        
        vehicule.avancer(50)
        
        assert vehicule.position == 150  # Doit avancer même avec vitesse 0
    
    def test_vehicule_avec_position_zero(self):
        """Test le comportement avec position zéro."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=0, vitesse=50)
        
        vehicule.avancer(100)
        
        assert vehicule.position == 100
    
    def test_historique_routes_initial(self):
        """Test que l'historique des routes est initialisé correctement."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_Initiale")
        
        assert vehicule.historique_routes == ["Route_Initiale"]
        assert len(vehicule.historique_routes) == 1
    
    def test_multiple_changements_route(self):
        """Test de multiples changements de route successifs."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A")
        
        vehicule.changer_de_route("Route_B", 10)
        vehicule.changer_de_route("Route_C", 20)
        vehicule.changer_de_route("Route_D", 30)
        
        assert vehicule.route_actuelle == "Route_D"
        assert vehicule.position == 30
        assert vehicule.historique_routes == ["Route_A", "Route_B", "Route_C", "Route_D"]
    
    def test_repr_apres_modifications(self):
        """Test la représentation technique après modifications."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=0, vitesse=30)
        
        vehicule.avancer(150)
        vehicule.vitesse = 60
        
        representation = repr(vehicule)
        
        assert "identifiant=1" in representation
        assert "route_actuelle='Route_A'" in representation
        assert "position=150" in representation
        assert "vitesse=60" in representation
    
    def test_str_apres_modifications(self):
        """Test la représentation textuelle après modifications."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=0, vitesse=30)
        
        vehicule.avancer(150)
        vehicule.vitesse = 60
        
        representation = str(vehicule)
        
        assert "Véhicule 1" in representation
        assert "Route_A" in representation
        assert "150m" in representation
        assert "60km/h" in representation


class TestVehiculeEdgeCases:
    """
    Tests des cas limites pour la classe Vehicule
    """
    
    def test_avancer_distance_zero(self):
        """Test avancer avec distance zéro."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=100, vitesse=50)
        
        vehicule.avancer(0)
        
        assert vehicule.position == 100  # Position inchangée
    
    def test_avancer_distance_float(self):
        """Test avancer avec distance décimale."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=100, vitesse=50)
        
        vehicule.avancer(75.5)
        
        assert vehicule.position == 175.5
    
    def test_changer_de_route_meme_route(self):
        """Test changement vers la même route."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=100, vitesse=50)
        
        vehicule.changer_de_route("Route_A", 50)
        
        # Doit fonctionner et ajouter à l'historique
        assert vehicule.route_actuelle == "Route_A"
        assert vehicule.position == 50
        assert vehicule.historique_routes == ["Route_A", "Route_A"]
    
    def test_vehicule_sans_route_actuelle(self):
        """Test création avec route_actuelle vide string."""
        vehicule = Vehicule(identifiant=1, route_actuelle="", position=100, vitesse=50)
        
        assert vehicule.route_actuelle == ""
        assert vehicule.historique_routes == [""]


# Tests paramétrés pour couvrir différentes combinaisons
class TestVehiculeParametre:
    """
    Tests paramétrés pour la classe Vehicule
    """
    
    @pytest.mark.parametrize("identifiant,route,position,vitesse", [
        (1, "Route_A", 0, 0),
        (999, "Route_B", 1000, 120),
        (0, "Route_C", 50, 30),
        (42, "Route_D", 75.5, 85.5),
    ])
    def test_creation_parametree_valide(self, identifiant, route, position, vitesse):
        """Test création de véhicule avec différents paramètres valides."""
        vehicule = Vehicule(identifiant, route, position, vitesse)
        
        assert vehicule.identifiant == identifiant
        assert vehicule.route_actuelle == route
        assert vehicule.position == position
        assert vehicule.vitesse == vitesse
    
    @pytest.mark.parametrize("distance_avancement,position_attendue", [
        (0, 100),
        (50, 150),
        (100.5, 200.5),
        (1000, 1100),
    ])
    def test_avancer_parametre(self, distance_avancement, position_attendue):
        """Test avancement avec différentes distances."""
        vehicule = Vehicule(identifiant=1, route_actuelle="Route_A", position=100, vitesse=50)
        
        vehicule.avancer(distance_avancement)
        
        assert vehicule.position == position_attendue


if __name__ == '__main__':
    pytest.main([__file__, "-v"])