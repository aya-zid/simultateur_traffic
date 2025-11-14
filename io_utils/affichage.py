"""
Module Affichage - Visualisation des données de simulation

Ce module fournit des fonctions pour afficher les résultats de simulation
sous forme de graphiques et de visualisations en console.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, List, Optional
import sys
import os

# Ajouter le chemin pour importer les modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class Affichage:
    """
    Classe pour la visualisation des données de simulation.
    
    Cette classe génère des graphiques et des affichages console
    pour analyser les résultats de la simulation de trafic.
    
    Attributes:
        style (str): Style matplotlib à utiliser
        palette_couleurs (list): Palette de couleurs pour les graphiques
    
    Example:
        >>> affichage = Affichage()
        >>> affichage.afficher_statistiques_temps_reel(stats)
    """
    
    def __init__(self, style='seaborn-v0_8'):
        """
        Initialise l'affichage avec un style donné.
        
        Args:
            style (str): Style matplotlib (défaut: 'seaborn-v0_8')
        """
        self.style = style
        plt.style.use(style)
        self.palette_couleurs = sns.color_palette("husl", 8)
        
    def afficher_tableau_bord_temps_reel(self, stats_actuelles: Dict, reseau):
        """
        Affiche un tableau de bord en temps réel dans la console.
        
        Args:
            stats_actuelles (dict): Statistiques du tour actuel
            reseau: Réseau routier à afficher
        
        Example:
            >>> affichage.afficher_tableau_bord_temps_reel(stats, reseau)
        """
        print("\n" + "="*70)
        print("📊 TABLEAU DE BORD TEMPS RÉEL")
        print("="*70)
        
        # Statistiques générales
        print(f"⏱️  Temps écoulé: {stats_actuelles.get('temps_ecoule', 0):.0f}s")
        print(f"🚗 Véhicules en circulation: {stats_actuelles.get('total_vehicules', 0)}")
        print(f"📈 Vitesse moyenne: {stats_actuelles.get('vitesse_moyenne', 0):.1f} km/h")
        print(f"🚦 Densité moyenne: {stats_actuelles.get('densite_moyenne', 0):.1f} véh/km")
        print(f"🚨 Taux de congestion: {stats_actuelles.get('taux_congestion', 0):.1f}%")
        
        # Routes les plus congestionnées
        if 'routes' in stats_actuelles:
            routes_triees = sorted(
                stats_actuelles['routes'].items(),
                key=lambda x: x[1].get('densite', 0),
                reverse=True
            )[:3]  # Top 3
            
            print("\n🔴 ROUTES LES PLUS CONGESTIONNÉES:")
            for nom_route, stats_route in routes_triees:
                if stats_route['nb_vehicules'] > 0:
                    print(f"   {nom_route}: {stats_route['nb_vehicules']} véhicules, "
                          f"densité: {stats_route['densite']:.1f} véh/km")
        
        print("="*70)
    
    def generer_graphique_evolution(self, historique_stats: List[Dict], fichier_sortie: Optional[str] = None):
        """
        Génère un graphique montrant l'évolution des statistiques dans le temps.
        
        Args:
            historique_stats (list): Historique des statistiques
            fichier_sortie (str, optional): Fichier pour sauvegarder le graphique
        
        Example:
            >>> affichage.generer_graphique_evolution(historique_stats, "evolution.png")
        """
        if not historique_stats:
            print("❌ Aucune donnée pour générer le graphique")
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Évolution des Statistiques de Trafic', fontsize=16, fontweight='bold')
        
        # Extraire les données
        temps = [stats.get('temps_ecoule', 0) for stats in historique_stats]
        vitesses = [stats.get('vitesse_moyenne', 0) for stats in historique_stats]
        densites = [stats.get('densite_moyenne', 0) for stats in historique_stats]
        congestions = [stats.get('taux_congestion', 0) for stats in historique_stats]
        vehicules = [stats.get('total_vehicules', 0) for stats in historique_stats]
        
        # Graphique 1: Vitesse moyenne
        ax1.plot(temps, vitesses, color=self.palette_couleurs[0], linewidth=2)
        ax1.set_title('Vitesse Moyenne', fontweight='bold')
        ax1.set_ylabel('Vitesse (km/h)')
        ax1.grid(True, alpha=0.3)
        ax1.fill_between(temps, vitesses, alpha=0.3, color=self.palette_couleurs[0])
        
        # Graphique 2: Densité du trafic
        ax2.plot(temps, densites, color=self.palette_couleurs[1], linewidth=2)
        ax2.set_title('Densité du Trafic', fontweight='bold')
        ax2.set_ylabel('Densité (véh/km)')
        ax2.grid(True, alpha=0.3)
        ax2.fill_between(temps, densites, alpha=0.3, color=self.palette_couleurs[1])
        
        # Graphique 3: Taux de congestion
        ax3.plot(temps, congestions, color=self.palette_couleurs[2], linewidth=2)
        ax3.set_title('Taux de Congestion', fontweight='bold')
        ax3.set_ylabel('Congestion (%)')
        ax3.set_xlabel('Temps (s)')
        ax3.grid(True, alpha=0.3)
        ax3.fill_between(temps, congestions, alpha=0.3, color=self.palette_couleurs[2])
        
        # Graphique 4: Nombre de véhicules
        ax4.plot(temps, vehicules, color=self.palette_couleurs[3], linewidth=2)
        ax4.set_title('Véhicules en Circulation', fontweight='bold')
        ax4.set_ylabel('Nombre de véhicules')
        ax4.set_xlabel('Temps (s)')
        ax4.grid(True, alpha=0.3)
        ax4.fill_between(temps, vehicules, alpha=0.3, color=self.palette_couleurs[3])
        
        plt.tight_layout()
        
        if fichier_sortie:
            plt.savefig(fichier_sortie, dpi=300, bbox_inches='tight')
            print(f"✅ Graphique sauvegardé: {fichier_sortie}")
        
        plt.show()
    
    def generer_carte_flux(self, reseau, fichier_sortie: Optional[str] = None):
        """
        Génère une carte visuelle du réseau avec les flux de trafic.
        
        Args:
            reseau: Réseau routier à visualiser
            fichier_sortie (str, optional): Fichier pour sauvegarder la carte
        
        Example:
            >>> affichage.generer_carte_flux(reseau, "carte_trafic.png")
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Positionner les routes de manière schématique
        positions_routes = {}
        angle = 0
        angle_step = 2 * np.pi / len(reseau.routes)
        
        for i, (nom_route, route) in enumerate(reseau.routes.items()):
            # Position circulaire pour une visualisation claire
            x = np.cos(angle) * 5
            y = np.sin(angle) * 5
            positions_routes[nom_route] = (x, y)
            
            # Tracer la route
            nb_vehicules = route.get_nombre_vehicules()
            epaisseur = 1 + (nb_vehicules / 10)  # Épaisseur proportionnelle au trafic
            
            # Couleur basée sur la congestion
            densite = route.get_densite_trafic()
            if densite > 30:
                couleur = 'red'
            elif densite > 15:
                couleur = 'orange'
            else:
                couleur = 'green'
            
            ax.plot([0, x], [0, y], color=couleur, linewidth=epaisseur, 
                   alpha=0.7, label=nom_route if i < 10 else "")
            
            # Ajouter le nom de la route et les statistiques
            ax.annotate(f"{nom_route}\n({nb_vehicules}v, {densite:.1f}v/km)", 
                       (x, y), xytext=(5, 5), textcoords='offset points',
                       fontsize=8, ha='left')
            
            angle += angle_step
        
        # Tracer les intersections
        for nom_route, (x, y) in positions_routes.items():
            ax.scatter(x, y, color='blue', s=50, alpha=0.7, zorder=5)
        
        # Tracer les connections entre routes
        for route_source, routes_dest in reseau.intersections.items():
            if route_source in positions_routes:
                x1, y1 = positions_routes[route_source]
                for route_dest in routes_dest:
                    if route_dest in positions_routes:
                        x2, y2 = positions_routes[route_dest]
                        ax.plot([x1, x2], [y1, y2], 'gray', linestyle='--', 
                               alpha=0.4, linewidth=0.5)
        
        ax.set_title('Carte du Réseau Routier avec Flux de Trafic', fontweight='bold')
        ax.set_xlabel('Position X')
        ax.set_ylabel('Position Y')
        ax.grid(True, alpha=0.3)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.set_aspect('equal')
        
        # Légende pour les couleurs
        legend_elements = [
            plt.Line2D([0], [0], color='green', lw=4, label='Fluide (<15 véh/km)'),
            plt.Line2D([0], [0], color='orange', lw=4, label='Modéré (15-30 véh/km)'),
            plt.Line2D([0], [0], color='red', lw=4, label='Congestionné (>30 véh/km)')
        ]
        ax.legend(handles=legend_elements, loc='lower right')
        
        plt.tight_layout()
        
        if fichier_sortie:
            plt.savefig(fichier_sortie, dpi=300, bbox_inches='tight')
            print(f"✅ Carte sauvegardée: {fichier_sortie}")
        
        plt.show()
    
    def afficher_rapport_performance(self, rapport: Dict):
        """
        Affiche un rapport de performance détaillé dans la console.
        
        Args:
            rapport (dict): Rapport de performance généré par l'analyseur
        
        Example:
            >>> affichage.afficher_rapport_performance(rapport)
        """
        print("\n" + "="*80)
        print("📈 RAPPORT DE PERFORMANCE DÉTAILLÉ")
        print("="*80)
        
        perf = rapport.get('performance_generale', {})
        print(f"🎯 Note de performance: {perf.get('note', 'N/A')}")
        print(f"📊 Efficacité du réseau: {perf.get('efficacite_reseau', 0):.1f}%")
        print(f"🚗 Vitesse moyenne: {perf.get('vitesse_moyenne', 0):.1f} km/h")
        print(f"🚨 Congestion moyenne: {perf.get('congestion_moyenne', 0):.1f}%")
        
        # Zones problématiques
        zones_problemes = rapport.get('zones_problematiques', [])
        if zones_problemes:
            print(f"\n🔴 ZONES À FORTE CONGESTION ({len(zones_problemes)} routes):")
            for zone in zones_problemes[:5]:  # Top 5 seulement
                print(f"   • {zone['route']}: {zone['taux_congestion']:.1f}% "
                      f"({zone['vehicules']} véhicules, {zone['vitesse_moyenne']:.1f} km/h)")
        
        # Recommandations
        recommandations = rapport.get('recommandations', [])
        if recommandations:
            print(f"\n💡 RECOMMANDATIONS:")
            for rec in recommandations:
                print(f"   • {rec}")
        
        print("="*80)
    
    def generer_graphique_comparaison_routes(self, stats_routes: Dict, fichier_sortie: Optional[str] = None):
        """
        Génère un graphique comparant les routes entre elles.
        
        Args:
            stats_routes (dict): Statistiques par route
            fichier_sortie (str, optional): Fichier de sauvegarde
        
        Example:
            >>> affichage.generer_graphique_comparaison_routes(stats_routes)
        """
        if not stats_routes:
            print("❌ Aucune donnée de routes disponible")
            return
        
        noms_routes = list(stats_routes.keys())
        vitesses = [stats.get('vitesse_moyenne', 0) for stats in stats_routes.values()]
        densites = [stats.get('densite', 0) for stats in stats_routes.values()]
        vehicules = [stats.get('nb_vehicules', 0) for stats in stats_routes.values()]
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
        
        # Graphique 1: Vitesses par route
        bars1 = ax1.bar(noms_routes, vitesses, color=self.palette_couleurs[0], alpha=0.7)
        ax1.set_title('Vitesse Moyenne par Route', fontweight='bold')
        ax1.set_ylabel('Vitesse (km/h)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Graphique 2: Densité par route
        bars2 = ax2.bar(noms_routes, densites, color=self.palette_couleurs[1], alpha=0.7)
        ax2.set_title('Densité du Trafic par Route', fontweight='bold')
        ax2.set_ylabel('Densité (véh/km)')
        ax2.tick_params(axis='x', rotation=45)
        
        # Graphique 3: Nombre de véhicules par route
        bars3 = ax3.bar(noms_routes, vehicules, color=self.palette_couleurs[2], alpha=0.7)
        ax3.set_title('Nombre de Véhicules par Route', fontweight='bold')
        ax3.set_ylabel('Nombre de véhicules')
        ax3.tick_params(axis='x', rotation=45)
        
        # Ajouter les valeurs sur les barres
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax = bar.axes
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.1f}', ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        
        if fichier_sortie:
            plt.savefig(fichier_sortie, dpi=300, bbox_inches='tight')
            print(f"✅ Graphique de comparaison sauvegardé: {fichier_sortie}")
        
        plt.show()

    def __str__(self):
        """Représentation textuelle de l'affichage."""
        return f"Affichage(style={self.style})"
