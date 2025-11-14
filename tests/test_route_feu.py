"""
Tests d'intégration Route + FeuRouge

Ce module teste le comportement des véhicules face aux feux de circulation sur les routes.
"""

import pytest
import sys
import os


from models.route import Route
from models.feuRouge import FeuRouge
from models.vehicule import Vehicule


class TestRouteFeuIntegration:
    """
    Tests d'intégration entre Route et FeuRouge
    """
    
    def test_arret_au_feu_rouge(self):
        """
        Test qu'un véhicule s'arrête devant un feu rouge.
        """
        # Créer une route
        route = Route("Route_test", 1000, 90)
        
        # Créer un feu rouge (cycle long pour rester rouge)
        feu = FeuRouge(cycle={'rouge': 30, 'vert': 20, 'orange': 5})
        route.ajouter_feu_rouge(feu, position=200)  # Feu plus proche
        
        # Créer un véhicule avec vitesse plus élevée
        vehicule = Vehicule(1, "Route_test", position=0, vitesse=72)  # 72 km/h = 20 m/s
        route.ajouter_vehicule(vehicule)
        
        # Simuler 15 secondes de déplacement
        for _ in range(15):
            route.mettre_a_jour_vehicules(dt=1.0)
        
        # Vérifier que le véhicule s'est arrêté avant le feu
        # Avec marge de sécurité, il devrait s'arrêter vers 195m
        assert vehicule.position < 200
        assert vehicule.position > 150  # Il a quand même bien avancé
        
        # Vérifier que le feu est toujours rouge
        assert feu.etat == 'rouge'

    def test_arret_au_feu_orange(self):
        """
        Test qu'un véhicule s'arrête aussi au feu orange.
        """
        route = Route("Route_test", 1000, 90)
        
        # Créer un feu et le mettre directement à l'orange
        feu = FeuRouge(cycle={'rouge': 5, 'vert': 5, 'orange': 10})
        feu.etat_actuel = 'orange'  # Forcer l'état orange
        feu.temps_ecoule = 0.0
        
        route.ajouter_feu_rouge(feu, position=150)
        
        vehicule = Vehicule(1, "Route_test", position=0, vitesse=54)  # 54 km/h = 15 m/s
        route.ajouter_vehicule(vehicule)
        
        # Vérifier que le feu est bien orange
        assert feu.etat == 'orange'
        
        # Simuler 10 secondes
        for _ in range(10):
            route.mettre_a_jour_vehicules(dt=1.0)
        
        # Vérifier que le véhicule s'est arrêté avant le feu orange
        assert vehicule.position < 150
    
    def test_comportement_sans_feu(self):
        """
        Test qu'un véhicule avance normalement sans feu.
        """
        route = Route("Route_test", 1000, 90)
        
        vehicule = Vehicule(1, "Route_test", position=0, vitesse=36)  # 36 km/h = 10 m/s
        route.ajouter_vehicule(vehicule)
        
        # Simuler 10 secondes
        for _ in range(10):
            route.mettre_a_jour_vehicules(dt=1.0)
        
        # Sans feu, le véhicule devrait avancer normalement
        # 10 m/s * 10s = 100m
        assert vehicule.position == 100.0
    
    def test_marge_securite_feux(self):
        """
        Test que les véhicules s'arrêtent avec une marge de sécurité avant le feu.
        """
        route = Route("Route_test", 1000, 90)
        
        feu = FeuRouge(cycle=30)  # Reste rouge
        route.ajouter_feu_rouge(feu, position=50)  # Feu très proche
        
        vehicule = Vehicule(1, "Route_test", position=0, vitesse=18)  # 18 km/h = 5 m/s
        route.ajouter_vehicule(vehicule)
        
        # Simuler jusqu'à ce que le véhicule s'arrête
        for _ in range(20):
            route.mettre_a_jour_vehicules(dt=1.0)
            if vehicule.position >= 45:  # Proche du feu
                break
        
        # Vérifier la marge de sécurité (s'arrête avant 50m)
        assert vehicule.position < 50
        assert vehicule.position > 0


# Tests avec pytest pour l'intégration complète
class TestRouteFeuPytest:
    """
    Tests pytest pour l'intégration Route + FeuRouge
    """
    
    @pytest.fixture
    def route_avec_feu_rouge(self):
        """Fixture pour une route avec un feu rouge"""
        route = Route("Route_fixture", 1000, 90)
        feu = FeuRouge(cycle=30)  # Long cycle rouge
        route.ajouter_feu_rouge(feu, position=300)
        return route, feu
    
    @pytest.fixture 
    def route_avec_feu_vert(self):
        """Fixture pour une route avec un feu vert"""
        route = Route("Route_fixture_vert", 1000, 90)
        feu = FeuRouge(cycle=30)
        feu.etat_actuel = 'vert'  # Forcer vert
        feu.temps_ecoule = 0.0
        route.ajouter_feu_rouge(feu, position=300)
        return route, feu
    
    @pytest.fixture
    def vehicule_rapide(self):
        """Fixture pour un véhicule rapide"""
        return Vehicule(99, "Route_fixture", position=0, vitesse=90)  # 90 km/h
    
    def test_arret_feux_rouge(self, route_avec_feu_rouge, vehicule_rapide):
        """Test d'arrêt au feu rouge"""
        route, feu = route_avec_feu_rouge
        vehicule = vehicule_rapide
        
        route.ajouter_vehicule(vehicule)
        
        # Simuler
        route.mettre_a_jour_vehicules(dt=10.0)
        
        # Vérifier l'arrêt avant le feu
        assert vehicule.position < 300
        assert feu.etat == 'rouge'
    
    def test_passage_feux_vert(self, route_avec_feu_vert, vehicule_rapide):
        """Test de passage au feu vert"""
        route, feu = route_avec_feu_vert
        vehicule = vehicule_rapide
        
        route.ajouter_vehicule(vehicule)
        
        # Vérifier état initial
        assert feu.etat == 'vert'
        
        # Simuler
        route.mettre_a_jour_vehicules(dt=10.0)
        
        # Vérifier que le véhicule a avancé (ne s'est pas arrêté)
        assert vehicule.position > 0
    
    def test_etat_feux_route(self, route_avec_feu_rouge):
        """Test la récupération de l'état des feux d'une route"""
        route, feu = route_avec_feu_rouge
        
        etat_feux = route.get_etat_feux()
        assert len(etat_feux) == 1
        assert 300 in etat_feux
        assert etat_feux[300] == 'rouge'
    
  
if __name__ == '__main__':
    pytest.main([__file__, "-v"])