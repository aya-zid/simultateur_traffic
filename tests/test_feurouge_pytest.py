"""
Tests unitaires pour la classe FeuRouge - Version pytest
"""

import sys
import os
import pytest
from unittest.mock import patch
from io import StringIO

from models.feuRouge import FeuRouge


class TestFeuRougePytest:
    """
    Tests unitaires pour la classe FeuRouge utilisant le framework pytest
    """
    
    @pytest.fixture
    def feu_standard(self):
        """Fixture pour un feu avec cycle standard"""
        return FeuRouge(cycle=5)
    
    @pytest.fixture
    def feu_personnalise(self):
        """Fixture pour un feu avec cycle personnalisé"""
        return FeuRouge(cycle={'rouge': 10, 'vert': 8, 'orange': 2})
    
    def test_initialisation_standard(self, feu_standard):
        """Test de l'initialisation avec un cycle standard"""
        assert feu_standard.etat == 'rouge'
        assert feu_standard.cycle['rouge'] == 5
        assert feu_standard.cycle['vert'] == 5
        assert feu_standard.cycle['orange'] == 5
        assert feu_standard.temps_ecoule == 0.0
    
    def test_initialisation_personnalisee(self, feu_personnalise):
        """Test de l'initialisation avec un cycle personnalisé"""
        assert feu_personnalise.etat == 'rouge'
        assert feu_personnalise.cycle['rouge'] == 10
        assert feu_personnalise.cycle['vert'] == 8
        assert feu_personnalise.cycle['orange'] == 2
    
    def test_initialisation_cycle_invalide_negatif(self):
        """Test de l'initialisation avec un cycle négatif"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            feu = FeuRouge(cycle=-5)
        
        assert feu.etat == 'rouge'  # Doit utiliser les valeurs par défaut
        output = mock_stdout.getvalue()
        assert "ERREUR" in output
    
    def test_initialisation_cycle_zero(self):
        """Test de l'initialisation avec un cycle à zéro"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            feu = FeuRouge(cycle=0)
        
        assert feu.etat == 'rouge'  # Doit utiliser les valeurs par défaut
        output = mock_stdout.getvalue()
        assert "ERREUR" in output
    
    def test_initialisation_dict_incomplet(self):
        """Test de l'initialisation avec un dictionnaire incomplet"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            feu = FeuRouge(cycle={'rouge': 5, 'vert': 5})  # Manque 'orange'
        
        assert feu.etat == 'rouge'  # Doit utiliser les valeurs par défaut
        output = mock_stdout.getvalue()
        assert "ERREUR" in output
    
    def test_propriete_etat(self, feu_standard):
        """Test de la propriété etat en lecture seule"""
        assert feu_standard.etat == 'rouge'
        # Vérifier que c'est bien en lecture seule
        with pytest.raises(AttributeError):
            feu_standard.etat = 'vert'
    
    def test_avancer_temps_standard(self, feu_standard):
        """Test de avancer_temps avec cycle standard"""
        # Avancer de 3 secondes - doit rester rouge
        feu_standard.avancer_temps(3)
        assert feu_standard.etat == 'rouge'
        assert feu_standard.temps_ecoule == pytest.approx(3.0)
        
        # Avancer de 3 secondes supplémentaires - doit passer à vert
        feu_standard.avancer_temps(3)
        assert feu_standard.etat == 'vert'
        assert feu_standard.temps_ecoule == pytest.approx(1.0)  # 3+3-5=1
    
    def test_avancer_temps_personnalise(self, feu_personnalise):
        """Test de avancer_temps avec cycle personnalisé"""
        # Avancer de 8 secondes - doit rester rouge
        feu_personnalise.avancer_temps(8)
        assert feu_personnalise.etat == 'rouge'
        
        # Avancer de 3 secondes supplémentaires - doit passer à vert
        feu_personnalise.avancer_temps(3)
        assert feu_personnalise.etat == 'vert'
    
    def test_avancer_temps_cycle_complet(self):
        """Test d'un cycle complet"""
        feu = FeuRouge(cycle=3)  # 3 secondes par état
        
        # Rouge -> Vert
        feu.avancer_temps(3)
        assert feu.etat == 'vert'
        
        # Vert -> Orange
        feu.avancer_temps(3)
        assert feu.etat == 'orange'
        
        # Orange -> Rouge
        feu.avancer_temps(3)
        assert feu.etat == 'rouge'
    
    def test_avancer_temps_negatif(self, feu_standard):
        """Test de avancer_temps avec temps négatif"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            feu_standard.avancer_temps(-1)
        
        # L'état ne doit pas changer
        assert feu_standard.etat == 'rouge'
        output = mock_stdout.getvalue()
        assert "ERREUR" in output
    
    def test_avancer_temps_zero(self, feu_standard):
        """Test de avancer_temps avec temps zéro"""
        feu_standard.avancer_temps(0)
        assert feu_standard.etat == 'rouge'
        assert feu_standard.temps_ecoule == 0.0
    
    def test_get_prochain_changement(self, feu_standard):
        """Test de get_prochain_changement"""
        assert feu_standard.get_prochain_changement() == 5.0
        
        feu_standard.avancer_temps(2)
        assert feu_standard.get_prochain_changement() == 3.0
        
        feu_standard.avancer_temps(3)
        assert feu_standard.get_prochain_changement() == 5.0  # Nouvel état
    
    def test_get_cycle_total_standard(self, feu_standard):
        """Test de get_cycle_total avec cycle standard"""
        assert feu_standard.get_cycle_total() == 15.0  # 5+5+5
    
    def test_get_cycle_total_personnalise(self, feu_personnalise):
        """Test de get_cycle_total avec cycle personnalisé"""
        assert feu_personnalise.get_cycle_total() == 20.0  # 10+8+2
    
    def test_changement_etat_multiple(self):
        """Test de changement d'état multiple en une seule fois"""
        # Passer directement du rouge au orange
        feu = FeuRouge(cycle=3)
        feu.avancer_temps(9)  # 3 états complets
        assert feu.etat == 'rouge'  # Retour au rouge
    
    @pytest.mark.parametrize("cycle_initial, expected_total", [
        (5, 15.0),
        (10, 30.0),
        ({'rouge': 4, 'vert': 4, 'orange': 2}, 10.0),
        ({'rouge': 7, 'vert': 5, 'orange': 3}, 15.0),
    ])
    def test_get_cycle_total_parametrise(self, cycle_initial, expected_total):
        """Test paramétré de get_cycle_total avec différentes configurations"""
        feu = FeuRouge(cycle=cycle_initial)
        assert feu.get_cycle_total() == expected_total
    
    @pytest.mark.parametrize("temps_ecoule, expected_etat", [
        (0, 'rouge'),
        (4, 'rouge'),
        (5, 'vert'),
        (9, 'vert'),
        (10, 'orange'),
        (14, 'orange'),
        (15, 'rouge'),
    ])
    def test_cycle_complet_parametrise(self, temps_ecoule, expected_etat):
        """Test paramétré d'un cycle complet"""
        feu = FeuRouge(cycle=5)
        feu.avancer_temps(temps_ecoule)
        assert feu.etat == expected_etat
    
    def test_repr(self, feu_standard):
        """Test de la représentation technique"""
        expected_repr = "FeuRouge(cycle={'rouge': 5, 'vert': 5, 'orange': 5})"
        assert repr(feu_standard) == expected_repr
    
    def test_str(self, feu_standard):
        """Test de la représentation textuelle"""
        feu_standard.avancer_temps(2)
        str_representation = str(feu_standard)
        assert "FeuRouge(état='rouge'" in str_representation
        assert "changement dans" in str_representation


# Tests d'intégration
class TestFeuRougeIntegration:
    """Tests d'intégration pour FeuRouge avec d'autres composants"""
    
    def test_integration_avec_route(self):
        """Test d'intégration FeuRouge avec Route"""
        from models.route import Route
        from models.vehicule import Vehicule
        
        # Créer une route avec un feu
        route = Route("Route_test", 1000, 50)
        feu = FeuRouge(cycle=5)
        route.ajouter_feu_rouge(feu, position=500)
        
        # Créer un véhicule
        vehicule = Vehicule(1, "Route_test", position=0, vitesse=50)
        route.ajouter_vehicule(vehicule)
        
        # Vérifier l'intégration
        assert route.get_nombre_feux() == 1
        assert 500 in route.get_etat_feux()
        assert route.get_etat_feux()[500] == 'rouge'
    
    def test_comportement_vehicules_feux(self):
        """Test du comportement des véhicules face aux feux"""
        from models.route import Route
        from models.vehicule import Vehicule
        
        route = Route("Route_test", 1000, 50)
        feu = FeuRouge(cycle=10)  # Long cycle pour test
        route.ajouter_feu_rouge(feu, position=200)
        
        vehicule = Vehicule(1, "Route_test", position=0, vitesse=72)  # 72 km/h = 20 m/s
        route.ajouter_vehicule(vehicule)
        
        # Avancer le temps - le véhicule devrait s'arrêter avant le feu rouge
        vehicules_sortis = route.mettre_a_jour_vehicules(dt=5)
        
        # Le véhicule ne devrait pas avoir dépassé le feu
        assert vehicule.position < 200
        assert len(vehicules_sortis) == 0


if __name__ == '__main__':
    # Permet d'exécuter les tests avec: python test_feurouge_pytest.py
    pytest.main([__file__, "-v"])