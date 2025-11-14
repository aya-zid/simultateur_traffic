"""
Tests unitaires pour la classe FeuRouge - Version unittest
"""

import unittest
import sys
import os
from unittest.mock import patch
from io import StringIO

from models.feuRouge import FeuRouge


class TestFeuRougeUnittest(unittest.TestCase):
    """
    Tests unitaires pour la classe FeuRouge utilisant le framework unittest
    """
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.feu_standard = FeuRouge(cycle=5)
        self.feu_personnalise = FeuRouge(cycle={'rouge': 10, 'vert': 8, 'orange': 2})
    
    def test_initialisation_standard(self):
        """Test de l'initialisation avec un cycle standard"""
        self.assertEqual(self.feu_standard.etat, 'rouge')
        self.assertEqual(self.feu_standard.cycle['rouge'], 5)
        self.assertEqual(self.feu_standard.cycle['vert'], 5)
        self.assertEqual(self.feu_standard.cycle['orange'], 5)
        self.assertEqual(self.feu_standard.temps_ecoule, 0.0)
    
    def test_initialisation_personnalisee(self):
        """Test de l'initialisation avec un cycle personnalisé"""
        self.assertEqual(self.feu_personnalise.etat, 'rouge')
        self.assertEqual(self.feu_personnalise.cycle['rouge'], 10)
        self.assertEqual(self.feu_personnalise.cycle['vert'], 8)
        self.assertEqual(self.feu_personnalise.cycle['orange'], 2)
    
    def test_initialisation_cycle_invalide_negatif(self):
        """Test de l'initialisation avec un cycle négatif"""
        # Capture la sortie print
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            feu = FeuRouge(cycle=-5)
        
        # Vérifie que l'objet est créé avec des valeurs par défaut
        self.assertEqual(feu.etat, 'rouge')
        # Vérifie qu'un message d'erreur a été imprimé
        output = mock_stdout.getvalue()
        self.assertIn("ERREUR", output)
    
    def test_initialisation_cycle_zero(self):
        """Test de l'initialisation avec un cycle à zéro"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            feu = FeuRouge(cycle=0)
        
        self.assertEqual(feu.etat, 'rouge')
        output = mock_stdout.getvalue()
        self.assertIn("ERREUR", output)
    
    def test_initialisation_dict_incomplet(self):
        """Test de l'initialisation avec un dictionnaire incomplet"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            feu = FeuRouge(cycle={'rouge': 5, 'vert': 5})  # Manque 'orange'
        
        self.assertEqual(feu.etat, 'rouge')
        output = mock_stdout.getvalue()
        self.assertIn("ERREUR", output)
    
    def test_propriete_etat(self):
        """Test de la propriété etat en lecture seule"""
        self.assertEqual(self.feu_standard.etat, 'rouge')
        # Vérifier que c'est bien en lecture seule
        with self.assertRaises(AttributeError):
            self.feu_standard.etat = 'vert'
    
    def test_avancer_temps_standard(self):
        """Test de avancer_temps avec cycle standard"""
        # Avancer de 3 secondes - doit rester rouge
        self.feu_standard.avancer_temps(3)
        self.assertEqual(self.feu_standard.etat, 'rouge')
        self.assertAlmostEqual(self.feu_standard.temps_ecoule, 3.0)
        
        # Avancer de 3 secondes supplémentaires - doit passer à vert
        self.feu_standard.avancer_temps(3)
        self.assertEqual(self.feu_standard.etat, 'vert')
        self.assertAlmostEqual(self.feu_standard.temps_ecoule, 1.0)  # 3+3-5=1
    
    def test_avancer_temps_personnalise(self):
        """Test de avancer_temps avec cycle personnalisé"""
        # Avancer de 8 secondes - doit rester rouge
        self.feu_personnalise.avancer_temps(8)
        self.assertEqual(self.feu_personnalise.etat, 'rouge')
        
        # Avancer de 3 secondes supplémentaires - doit passer à vert
        self.feu_personnalise.avancer_temps(3)
        self.assertEqual(self.feu_personnalise.etat, 'vert')
    
    def test_avancer_temps_cycle_complet(self):
        """Test d'un cycle complet"""
        feu = FeuRouge(cycle=3)  # 3 secondes par état
        
        # Rouge -> Vert
        feu.avancer_temps(3)
        self.assertEqual(feu.etat, 'vert')
        
        # Vert -> Orange
        feu.avancer_temps(3)
        self.assertEqual(feu.etat, 'orange')
        
        # Orange -> Rouge
        feu.avancer_temps(3)
        self.assertEqual(feu.etat, 'rouge')
    
    def test_avancer_temps_negatif(self):
        """Test de avancer_temps avec temps négatif"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.feu_standard.avancer_temps(-1)
        
        # L'état ne doit pas changer
        self.assertEqual(self.feu_standard.etat, 'rouge')
        output = mock_stdout.getvalue()
        self.assertIn("ERREUR", output)
    
    def test_avancer_temps_zero(self):
        """Test de avancer_temps avec temps zéro"""
        self.feu_standard.avancer_temps(0)
        self.assertEqual(self.feu_standard.etat, 'rouge')
        self.assertEqual(self.feu_standard.temps_ecoule, 0.0)
    
    def test_get_prochain_changement(self):
        """Test de get_prochain_changement"""
        self.assertEqual(self.feu_standard.get_prochain_changement(), 5.0)
        
        self.feu_standard.avancer_temps(2)
        self.assertEqual(self.feu_standard.get_prochain_changement(), 3.0)
        
        self.feu_standard.avancer_temps(3)
        self.assertEqual(self.feu_standard.get_prochain_changement(), 5.0)  # Nouvel état
    
    def test_get_cycle_total_standard(self):
        """Test de get_cycle_total avec cycle standard"""
        self.assertEqual(self.feu_standard.get_cycle_total(), 15.0)  # 5+5+5
    
    def test_get_cycle_total_personnalise(self):
        """Test de get_cycle_total avec cycle personnalisé"""
        self.assertEqual(self.feu_personnalise.get_cycle_total(), 20.0)  # 10+8+2
    
    def test_changement_etat_multiple(self):
        """Test de changement d'état multiple en une seule fois"""
        # Passer directement du rouge au orange
        feu = FeuRouge(cycle=3)
        feu.avancer_temps(9)  # 3 états complets
        self.assertEqual(feu.etat, 'rouge')  # Retour au rouge
    
    def test_repr(self):
        """Test de la représentation technique"""
        feu = FeuRouge(cycle=5)
        expected_repr = "FeuRouge(cycle={'rouge': 5, 'vert': 5, 'orange': 5})"
        self.assertEqual(repr(feu), expected_repr)
    
    def test_str(self):
        """Test de la représentation textuelle"""
        feu = FeuRouge(cycle=5)
        feu.avancer_temps(2)
        str_representation = str(feu)
        self.assertIn("FeuRouge(état='rouge'", str_representation)
        self.assertIn("changement dans", str_representation)


if __name__ == '__main__':
    # Exécuter les tests avec une sortie détaillée
    unittest.main(verbosity=2)