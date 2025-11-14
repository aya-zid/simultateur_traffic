"""
Tests complets pour la classe Route - Amélioration de la couverture
"""

import pytest
import sys
import os
from unittest.mock import patch
from io import StringIO


from models.route import Route
from models.vehicule import Vehicule
from models.feuRouge import FeuRouge
from exceptions import (
    LongueurInvalideError, 
    LimiteVitesseInvalideError,
    VehiculeDejaPresentError,
    PositionVehiculeInvalideError,
    AucuneMiseAJourPossibleError,
    PositionFeuInvalideError
)


class TestRouteComplet:
    """
    Tests complets pour améliorer la couverture de la classe Route
    """
    
    def test_creation_route_longueur_invalide(self):
        """Test la création d'une route avec longueur invalide (gestion d'erreur)."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            route = Route("Route_Invalide", longueur=0, limite_vitesse=90)
        
        # Vérifie que l'erreur est gérée
        output = mock_stdout.getvalue()
        assert "[ERREUR INIT ROUTE]" in output
        assert "longueur" in output.lower()
    
    def test_creation_route_longueur_negative(self):
        """Test la création d'une route avec longueur négative (gestion d'erreur)."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            route = Route("Route_Negative", longueur=-100, limite_vitesse=90)
        
        output = mock_stdout.getvalue()
        assert "[ERREUR INIT ROUTE]" in output
    
    def test_creation_route_limite_vitesse_invalide(self):
        """Test la création d'une route avec limite de vitesse invalide (gestion d'erreur)."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            route = Route("Route_Vitesse_Invalide", longueur=1000, limite_vitesse=0)
        
        output = mock_stdout.getvalue()
        assert "[ERREUR INIT ROUTE]" in output
        assert "limite de vitesse" in output.lower()
    
    def test_creation_route_limite_vitesse_negative(self):
        """Test la création d'une route avec limite de vitesse négative (gestion d'erreur)."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            route = Route("Route_Vitesse_Negative", longueur=1000, limite_vitesse=-50)
        
        output = mock_stdout.getvalue()
        assert "[ERREUR INIT ROUTE]" in output
    
    def test_ajouter_vehicule_deja_present(self):
        """Test l'ajout d'un véhicule déjà présent sur la route (gestion d'erreur)."""
        route = Route("Route_A", 1000, 90)
        vehicule = Vehicule(1, "Route_A", position=0, vitesse=50)
        
        # Premier ajout - devrait fonctionner
        route.ajouter_vehicule(vehicule)
        
        # Deuxième ajout - devrait échouer
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            route.ajouter_vehicule(vehicule)
        
        output = mock_stdout.getvalue()
        assert "[ERREUR AJOUT VEHICULE]" in output
        assert "déjà sur la route" in output
    
    def test_ajouter_vehicule_position_invalide(self):
        """Test l'ajout d'un véhicule avec position invalide (gestion d'erreur)."""
        route = Route("Route_A", 1000, 90)
        # Véhicule avec position au-delà de la longueur de la route
        vehicule = Vehicule(1, "Route_A", position=1500, vitesse=50)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            route.ajouter_vehicule(vehicule)
        
        output = mock_stdout.getvalue()
        assert "[ERREUR AJOUT VEHICULE]" in output
        assert "dépasse la longueur" in output
    
    def test_mettre_a_jour_vehicules_route_vide(self):
        """Test la mise à jour sur une route vide (gestion d'erreur)."""
        route = Route("Route_Vide", 1000, 90)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            vehicules_sortis = route.mettre_a_jour_vehicules()
        
        assert vehicules_sortis == []
        output = mock_stdout.getvalue()
        assert "[ERREUR MISE À JOUR]" in output
        assert "aucun véhicule" in output.lower()
    
    def test_ajouter_feu_rouge_position_invalide_negative(self):
        """Test l'ajout d'un feu rouge avec position négative (gestion d'erreur)."""
        route = Route("Route_A", 1000, 90)
        feu = FeuRouge(cycle=5)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            route.ajouter_feu_rouge(feu, position=-50)
        
        output = mock_stdout.getvalue()
        assert "[ERREUR AJOUT FEU]" in output
        assert "position du feu invalide" in output.lower()
    
    def test_ajouter_feu_rouge_position_invalide_trop_grande(self):
        """Test l'ajout d'un feu rouge avec position trop grande (gestion d'erreur)."""
        route = Route("Route_A", 1000, 90)
        feu = FeuRouge(cycle=5)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            route.ajouter_feu_rouge(feu, position=1500)
        
        output = mock_stdout.getvalue()
        assert "[ERREUR AJOUT FEU]" in output
    
    def test_ajouter_feu_rouge_position_none(self):
        """Test l'ajout d'un feu rouge avec position None (doit utiliser la fin)."""
        route = Route("Route_A", 1000, 90)
        feu = FeuRouge(cycle=5)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            route.ajouter_feu_rouge(feu, position=None)
        
        # Vérifie que le feu est ajouté à la fin de la route
        assert 1000 in route.feux_rouges
        assert route.feux_rouges[1000] == feu
        output = mock_stdout.getvalue()
        assert "Feu rouge ajouté" in output
    
    def test_ajouter_feu_rouge_remplacement(self):
        """Test l'ajout d'un feu rouge qui remplace un feu existant."""
        route = Route("Route_A", 1000, 90)
        feu1 = FeuRouge(cycle=5)
        feu2 = FeuRouge(cycle=10)
        
        # Premier feu
        route.ajouter_feu_rouge(feu1, position=500)
        
        # Deuxième feu à la même position - devrait remplacer
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            route.ajouter_feu_rouge(feu2, position=500)
        
        output = mock_stdout.getvalue()
        assert "Remplacement du feu existant" in output
        assert route.feux_rouges[500] == feu2  # Le deuxième feu a remplacé le premier
    
    def test_doit_arreter_vehicule_feu_rouge(self):
        """Test la détection d'arrêt pour un feu rouge."""
        route = Route("Route_A", 1000, 90)
        feu = FeuRouge(cycle=5)
        route.ajouter_feu_rouge(feu, position=500)
        
        vehicule = Vehicule(1, "Route_A", position=400, vitesse=50)
        
        # Le véhicule veut avancer de 200m (de 400 à 600), donc traverse le feu à 500
        doit_arreter = route._doit_arreter_vehicule(vehicule, 200)
        
        assert doit_arreter == True  # Doit s'arrêter car feu rouge
    
    def test_doit_arreter_vehicule_feu_vert(self):
        """Test la détection d'arrêt pour un feu vert (ne doit pas s'arrêter)."""
        route = Route("Route_A", 1000, 90)
        feu = FeuRouge(cycle=5)
        feu.etat_actuel = 'vert'  # Forcer feu vert
        route.ajouter_feu_rouge(feu, position=500)
        
        vehicule = Vehicule(1, "Route_A", position=400, vitesse=50)
        
        doit_arreter = route._doit_arreter_vehicule(vehicule, 200)
        
        assert doit_arreter == False  # Ne doit pas s'arrêter car feu vert
    
    def test_doit_arreter_vehicule_feu_orange(self):
        """Test la détection d'arrêt pour un feu orange (doit s'arrêter)."""
        route = Route("Route_A", 1000, 90)
        feu = FeuRouge(cycle=5)
        feu.etat_actuel = 'orange'  # Forcer feu orange
        route.ajouter_feu_rouge(feu, position=500)
        
        vehicule = Vehicule(1, "Route_A", position=400, vitesse=50)
        
        doit_arreter = route._doit_arreter_vehicule(vehicule, 200)
        
        assert doit_arreter == True  # Doit s'arrêter car feu orange
    
    def test_doit_arreter_vehicule_pas_de_feu(self):
        """Test la détection d'arrêt sans feu (ne doit pas s'arrêter)."""
        route = Route("Route_A", 1000, 90)  # Pas de feu
        
        vehicule = Vehicule(1, "Route_A", position=400, vitesse=50)
        
        doit_arreter = route._doit_arreter_vehicule(vehicule, 200)
        
        assert doit_arreter == False  # Pas de feu, donc pas d'arrêt
    
    def test_get_distance_avant_obstacle_feu_rouge(self):
        """Test le calcul de distance avec feu rouge."""
        route = Route("Route_A", 1000, 90)
        feu = FeuRouge(cycle=5)
        route.ajouter_feu_rouge(feu, position=500)
        
        vehicule = Vehicule(1, "Route_A", position=400, vitesse=50)
        
        distance_max = 200  # Veut aller jusqu'à 600
        distance_reelle = route._get_distance_avant_obstacle(vehicule, distance_max)
        
        # Doit s'arrêter avant le feu (500 - 400 - 5 = 95m)
        assert distance_reelle == 95.0
    
    def test_get_distance_avant_obstacle_feu_vert(self):
        """Test le calcul de distance avec feu vert."""
        route = Route("Route_A", 1000, 90)
        feu = FeuRouge(cycle=5)
        feu.etat_actuel = 'vert'  # Forcer feu vert
        route.ajouter_feu_rouge(feu, position=500)
        
        vehicule = Vehicule(1, "Route_A", position=400, vitesse=50)
        
        distance_max = 200
        distance_reelle = route._get_distance_avant_obstacle(vehicule, distance_max)
        
        # Peut avancer normalement (jusqu'à la fin de la route ou distance_max)
        assert distance_reelle == 200  # Pas d'obstacle
    
    def test_get_distance_avant_obstacle_fin_route(self):
        """Test le calcul de distance avec fin de route."""
        route = Route("Route_A", 1000, 90)
        
        vehicule = Vehicule(1, "Route_A", position=900, vitesse=50)
        
        distance_max = 200  # Veut aller jusqu'à 1100, mais route finit à 1000
        distance_reelle = route._get_distance_avant_obstacle(vehicule, distance_max)
        
        # Doit s'arrêter à la fin de la route (1000 - 900 = 100m)
        assert distance_reelle == 100.0
    
    def test_get_distance_avant_obstacle_multiple_feux(self):
        """Test le calcul de distance avec plusieurs feux."""
        route = Route("Route_A", 1000, 90)
        
        # Deux feux rouges
        feu1 = FeuRouge(cycle=5)
        feu2 = FeuRouge(cycle=5)
        route.ajouter_feu_rouge(feu1, position=300)
        route.ajouter_feu_rouge(feu2, position=600)
        
        vehicule = Vehicule(1, "Route_A", position=200, vitesse=50)
        
        distance_max = 500  # Veut aller jusqu'à 700
        distance_reelle = route._get_distance_avant_obstacle(vehicule, distance_max)
        
        # Doit s'arrêter au premier feu (300 - 200 - 5 = 95m)
        assert distance_reelle == 95.0
    
    def test_mettre_a_jour_vehicules_avec_dt(self):
        """Test la mise à jour des véhicules avec dt personnalisé."""
        route = Route("Route_A", 1000, 90)
        vehicule = Vehicule(1, "Route_A", position=0, vitesse=36)  # 36 km/h = 10 m/s
        route.ajouter_vehicule(vehicule)
        
        # Mise à jour avec dt=2 secondes
        vehicules_sortis = route.mettre_a_jour_vehicules(dt=2.0)
        
        # 10 m/s * 2s = 20m
        assert vehicule.position == 20.0
        assert vehicules_sortis == []
    
    def test_mettre_a_jour_vehicules_avec_feu(self):
        """Test la mise à jour des véhicules avec feu rouge."""
        route = Route("Route_A", 1000, 90)
        feu = FeuRouge(cycle=5)
        route.ajouter_feu_rouge(feu, position=100)
        
        vehicule = Vehicule(1, "Route_A", position=0, vitesse=72)  # 72 km/h = 20 m/s
        route.ajouter_vehicule(vehicule)
        
        # Mise à jour avec dt=10 secondes
        vehicules_sortis = route.mettre_a_jour_vehicules(dt=10.0)
        
        # Doit s'arrêter avant le feu à 100m
        assert vehicule.position < 100
        assert vehicule.position > 0  # A avancé un peu
        assert vehicules_sortis == []
    
    def test_get_nombre_feux(self):
        """Test la récupération du nombre de feux."""
        route = Route("Route_A", 1000, 90)
        
        # Aucun feu initialement
        assert route.get_nombre_feux() == 0
        
        # Ajouter un feu
        feu1 = FeuRouge(cycle=5)
        route.ajouter_feu_rouge(feu1, position=500)
        assert route.get_nombre_feux() == 1
        
        # Ajouter un deuxième feu
        feu2 = FeuRouge(cycle=5)
        route.ajouter_feu_rouge(feu2, position=800)
        assert route.get_nombre_feux() == 2
    
    def test_get_etat_feux(self):
        """Test la récupération de l'état des feux."""
        route = Route("Route_A", 1000, 90)
        
        feu1 = FeuRouge(cycle=5)
        feu2 = FeuRouge(cycle=10)
        feu2.etat_actuel = 'vert'  # Forcer état différent
        
        route.ajouter_feu_rouge(feu1, position=500)
        route.ajouter_feu_rouge(feu2, position=800)
        
        etat_feux = route.get_etat_feux()
        
        assert len(etat_feux) == 2
        assert etat_feux[500] == 'rouge'
        assert etat_feux[800] == 'vert'

class TestRouteIntegration:
    """
    Tests d'intégration pour la classe Route
    """
    
    def test_route_complete_avec_feux_et_vehicules(self):
        """Test complet d'une route avec feux et véhicules."""
        route = Route("Route_Complete", 2000, 90)
        
        # Ajouter plusieurs feux
        feu1 = FeuRouge(cycle={'rouge': 10, 'vert': 20, 'orange': 5})
        feu2 = FeuRouge(cycle={'rouge': 5, 'vert': 15, 'orange': 3})
        route.ajouter_feu_rouge(feu1, position=500)
        route.ajouter_feu_rouge(feu2, position=1200)
        
        # Ajouter plusieurs véhicules
        vehicule1 = Vehicule(1, "Route_Complete", position=0, vitesse=50)
        vehicule2 = Vehicule(2, "Route_Complete", position=100, vitesse=60)
        route.ajouter_vehicule(vehicule1)
        route.ajouter_vehicule(vehicule2)
        
        # Vérifications initiales
        assert route.get_nombre_vehicules() == 2
        assert route.get_nombre_feux() == 2
        assert route.get_densite_trafic() == 1.0  # 2 véhicules / 2km
        
        # Simuler plusieurs mises à jour
        for _ in range(5):
            route.mettre_a_jour_vehicules(dt=1.0)
        
        # Vérifier que les véhicules ont avancé mais sont toujours sur la route
        assert vehicule1.position > 0
        assert vehicule2.position > 100
        assert route.get_nombre_vehicules() == 2


if __name__ == '__main__':
    pytest.main([__file__, "-v"])