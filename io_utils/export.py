"""
Module Export - Export des données de simulation

Ce module fournit des fonctions pour exporter les résultats de simulation
dans différents formats (CSV, JSON, Excel) et générer des rapports.
"""

import json
import csv
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import sys
import os

# Ajouter le chemin pour importer les modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class Export:
    """
    Classe pour l'export des données de simulation.
    
    Cette classe permet d'exporter les résultats de simulation
    dans différents formats pour analyse ultérieure.
    
    Attributes:
        format_date (str): Format pour les horodatages
        repertoire_sortie (str): Répertoire par défaut pour les exports
    
    Example:
        >>> export = Export()
        >>> export.exporter_csv(historique_stats, "resultats_simulation.csv")
    """
    
    def __init__(self, repertoire_sortie="exports"):
        """
        Initialise l'export avec un répertoire de sortie.
        
        Args:
            repertoire_sortie (str): Répertoire pour les fichiers d'export
        """
        self.repertoire_sortie = repertoire_sortie
        self.format_date = "%Y%m%d_%H%M%S"
        
        # Créer le répertoire s'il n'existe pas
        os.makedirs(repertoire_sortie, exist_ok=True)
    
    def exporter_json(self, data: Dict, nom_fichier: Optional[str] = None):
        """
        Exporte les données au format JSON.
        
        Args:
            data (dict): Données à exporter
            nom_fichier (str, optional): Nom du fichier de sortie
        
        Returns:
            str: Chemin du fichier créé
        
        Example:
            >>> chemin = export.exporter_json(statistiques, "stats.json")
        """
        if nom_fichier is None:
            timestamp = datetime.now().strftime(self.format_date)
            nom_fichier = f"simulation_{timestamp}.json"
        
        chemin_complet = os.path.join(self.repertoire_sortie, nom_fichier)
        
        try:
            with open(chemin_complet, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Données JSON exportées: {chemin_complet}")
            return chemin_complet
            
        except Exception as e:
            print(f"❌ Erreur lors de l'export JSON: {e}")
            return None
    
    def exporter_csv(self, historique_stats: List[Dict], nom_fichier: Optional[str] = None):
        """
        Exporte l'historique des statistiques au format CSV.
        
        Args:
            historique_stats (list): Historique des statistiques
            nom_fichier (str, optional): Nom du fichier de sortie
        
        Returns:
            str: Chemin du fichier créé
        
        Example:
            >>> chemin = export.exporter_csv(historique_stats, "resultats.csv")
        """
        if not historique_stats:
            print("❌ Aucune donnée à exporter")
            return None
        
        if nom_fichier is None:
            timestamp = datetime.now().strftime(self.format_date)
            nom_fichier = f"statistiques_{timestamp}.csv"
        
        chemin_complet = os.path.join(self.repertoire_sortie, nom_fichier)
        
        try:
            # Préparer les données pour CSV
            lignes = []
            for stats in historique_stats:
                ligne = {
                    'tour': stats.get('tour', 0),
                    'temps_ecoule': stats.get('temps_ecoule', 0),
                    'vitesse_moyenne': stats.get('vitesse_moyenne', 0),
                    'densite_moyenne': stats.get('densite_moyenne', 0),
                    'taux_congestion': stats.get('taux_congestion', 0),
                    'total_vehicules': stats.get('total_vehicules', 0),
                    'changements_route': stats.get('changements_route', 0),
                    'vehicules_sortis': stats.get('vehicules_sortis', 0)
                }
                
                # Ajouter les statistiques par route
                if 'routes' in stats:
                    for nom_route, stats_route in stats['routes'].items():
                        ligne[f'{nom_route}_vehicules'] = stats_route.get('nb_vehicules', 0)
                        ligne[f'{nom_route}_vitesse'] = stats_route.get('vitesse_moyenne', 0)
                        ligne[f'{nom_route}_densite'] = stats_route.get('densite', 0)
                
                lignes.append(ligne)
            
            # Écrire le CSV
            with open(chemin_complet, 'w', newline='', encoding='utf-8') as f:
                if lignes:
                    fieldnames = lignes[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(lignes)
            
            print(f"✅ Données CSV exportées: {chemin_complet} ({len(lignes)} lignes)")
            return chemin_complet
            
        except Exception as e:
            print(f"❌ Erreur lors de l'export CSV: {e}")
            return None
    
    def exporter_excel(self, historique_stats: List[Dict], nom_fichier: Optional[str] = None):
        """
        Exporte les données au format Excel avec plusieurs onglets.
        
        Args:
            historique_stats (list): Historique des statistiques
            nom_fichier (str, optional): Nom du fichier de sortie
        
        Returns:
            str: Chemin du fichier créé
        
        Example:
            >>> chemin = export.exporter_excel(historique_stats, "rapport.xlsx")
        """
        try:
            import openpyxl
        except ImportError:
            print("❌ openpyxl n'est pas installé. Installez-le avec: pip install openpyxl")
            return None
        
        if nom_fichier is None:
            timestamp = datetime.now().strftime(self.format_date)
            nom_fichier = f"rapport_complet_{timestamp}.xlsx"
        
        chemin_complet = os.path.join(self.repertoire_sortie, nom_fichier)
        
        try:
            with pd.ExcelWriter(chemin_complet, engine='openpyxl') as writer:
                
                # Onglet 1: Statistiques temporelles
                if historique_stats:
                    df_stats = pd.DataFrame(historique_stats)
                    df_stats.to_excel(writer, sheet_name='Statistiques_Temporelles', index=False)
                
                # Onglet 2: Résumé global
                if historique_stats:
                    resume_data = {
                        'Métrique': [
                            'Tours de simulation',
                            'Durée totale (s)',
                            'Vitesse moyenne globale (km/h)',
                            'Densité moyenne globale (véh/km)',
                            'Congestion moyenne (%)',
                            'Véhicules maximum',
                            'Changements de route totaux'
                        ],
                        'Valeur': [
                            len(historique_stats),
                            historique_stats[-1].get('temps_ecoule', 0) if historique_stats else 0,
                            sum(s.get('vitesse_moyenne', 0) for s in historique_stats) / len(historique_stats) if historique_stats else 0,
                            sum(s.get('densite_moyenne', 0) for s in historique_stats) / len(historique_stats) if historique_stats else 0,
                            sum(s.get('taux_congestion', 0) for s in historique_stats) / len(historique_stats) if historique_stats else 0,
                            max(s.get('total_vehicules', 0) for s in historique_stats) if historique_stats else 0,
                            sum(s.get('changements_route', 0) for s in historique_stats) if historique_stats else 0
                        ]
                    }
                    df_resume = pd.DataFrame(resume_data)
                    df_resume.to_excel(writer, sheet_name='Resume_Global', index=False)
                
                # Onglet 3: Statistiques par route (dernier tour)
                if historique_stats and 'routes' in historique_stats[-1]:
                    routes_data = []
                    for nom_route, stats_route in historique_stats[-1]['routes'].items():
                        routes_data.append({
                            'Route': nom_route,
                            'Véhicules': stats_route.get('nb_vehicules', 0),
                            'Vitesse moyenne (km/h)': stats_route.get('vitesse_moyenne', 0),
                            'Densité (véh/km)': stats_route.get('densite', 0),
                            'Utilisation': stats_route.get('utilisation', 0)
                        })
                    df_routes = pd.DataFrame(routes_data)
                    df_routes.to_excel(writer, sheet_name='Routes_Finales', index=False)
            
            print(f"✅ Rapport Excel exporté: {chemin_complet}")
            return chemin_complet
            
        except Exception as e:
            print(f"❌ Erreur lors de l'export Excel: {e}")
            return None
    
    def generer_rapport_complet(self, simulateur, nom_fichier: Optional[str] = None):
        """
        Génère un rapport complet avec toutes les données de simulation.
        
        Args:
            simulateur: Instance du simulateur
            nom_fichier (str, optional): Nom du fichier de sortie
        
        Returns:
            str: Chemin du fichier créé
        
        Example:
            >>> chemin = export.generer_rapport_complet(simulateur)
        """
        if nom_fichier is None:
            timestamp = datetime.now().strftime(self.format_date)
            nom_fichier = f"rapport_complet_{timestamp}.json"
        
        chemin_complet = os.path.join(self.repertoire_sortie, nom_fichier)
        
        try:
            # Collecter toutes les données
            rapport = {
                'metadata': {
                    'date_generation': datetime.now().isoformat(),
                    'duree_simulation': simulateur.temps_ecoule,
                    'nombre_tours': len(simulateur.historique_stats),
                    'nombre_routes': len(simulateur.reseau.routes),
                    'vehicules_maximum': max(
                        [stats.get('total_vehicules', 0) for stats in simulateur.historique_stats]
                    ) if simulateur.historique_stats else 0
                },
                'reseau': {
                    'routes': {
                        nom: {
                            'longueur': route.longueur,
                            'limite_vitesse': route.limite_vitesse,
                            'vehicules_actuels': route.get_nombre_vehicules()
                        } for nom, route in simulateur.reseau.routes.items()
                    },
                    'intersections': simulateur.reseau.intersections
                },
                'statistiques_globales': simulateur.analyseur.calculer_statistiques_globales(),
                'historique_detaille': simulateur.historique_stats,
                'zones_congestion': simulateur.analyseur.identifier_zones_congestion(),
                'performance': simulateur.analyseur.generer_rapport_performance()
            }
            
            # Exporter le rapport
            with open(chemin_complet, 'w', encoding='utf-8') as f:
                json.dump(rapport, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Rapport complet exporté: {chemin_complet}")
            return chemin_complet
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération du rapport: {e}")
            return None
    
    def exporter_pour_visualisation(self, historique_stats: List[Dict], prefixe: str = "visu"):
        """
        Exporte les données dans un format optimisé pour la visualisation.
        
        Args:
            historique_stats (list): Historique des statistiques
            prefixe (str): Préfixe pour les fichiers
        
        Returns:
            dict: Chemins des fichiers créés
        
        Example:
            >>> fichiers = export.exporter_pour_visualisation(historique_stats)
        """
        timestamp = datetime.now().strftime(self.format_date)
        fichiers_crees = {}
        
        # Export JSON pour visualisations web
        fichiers_crees['json'] = self.exporter_json(
            historique_stats, 
            f"{prefixe}_{timestamp}.json"
        )
        
        # Export CSV pour analyse
        fichiers_crees['csv'] = self.exporter_csv(
            historique_stats,
            f"{prefixe}_{timestamp}.csv"
        )
        
        # Export des métriques clés séparément
        if historique_stats:
            metriques_cles = {
                'temps': [s.get('temps_ecoule', 0) for s in historique_stats],
                'vitesse': [s.get('vitesse_moyenne', 0) for s in historique_stats],
                'densite': [s.get('densite_moyenne', 0) for s in historique_stats],
                'congestion': [s.get('taux_congestion', 0) for s in historique_stats],
                'vehicules': [s.get('total_vehicules', 0) for s in historique_stats]
            }
            
            metriques_chemin = os.path.join(
                self.repertoire_sortie, 
                f"metriques_cles_{timestamp}.json"
            )
            with open(metriques_chemin, 'w', encoding='utf-8') as f:
                json.dump(metriques_cles, f, ensure_ascii=False, indent=2)
            fichiers_crees['metriques'] = metriques_chemin
        
        return fichiers_crees

    def __str__(self):
        """Représentation textuelle de l'export."""
        return f"Export(repertoire={self.repertoire_sortie})"
