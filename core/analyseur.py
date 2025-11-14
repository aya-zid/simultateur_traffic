"""
Module Analyseur - Analyse des statistiques de simulation

Ce module définit la classe Analyseur qui calcule diverses métriques
et statistiques sur le réseau routier et la circulation.
"""

import statistics
from typing import Dict, List, Optional
from exceptions import (
    AnalyseurError,
    DonneesInvalideError,
    CalculStatistiquesError
)
class Analyseur:
    """
    Analyseur des statistiques de trafic routier.
    
    Cette classe calcule les métriques de performance du réseau
    comme les vitesses moyennes, les zones de congestion, et les temps de parcours.
    
    Attributes:
        reseau (ReseauRoutier): Réseau routier à analyser
        historique_congestion (list): Historique des niveaux de congestion
    
    Example:
        >>> analyseur = Analyseur(reseau)
        >>> stats = analyseur.calculer_statistiques_tour()
        >>> print(f"Vitesse moyenne: {stats['vitesse_moyenne']} km/h")
    """
    
    def __init__(self, reseau):
        """
        Initialise l'analyseur avec un réseau.
        
        Args:
            reseau (ReseauRoutier): Réseau routier à analyser
        """
        self.reseau = reseau
        self.historique_congestion = []
    
    def calculer_statistiques_tour(self) -> Dict:
        """
        Calcule les statistiques pour le tour actuel.
        
        Returns:
            dict: Dictionnaire contenant toutes les statistiques du tour
        
        Example:
            >>> stats = analyseur.calculer_statistiques_tour()
            >>> print(stats['vitesse_moyenne'])
            65.5
        """
        try:
            if not self.reseau:
                raise DonneesInvalideError("Réseau non fourni à l'analyseur")

            stats = {}
            
            # Vitesse moyenne de tous les véhicules
            stats['vitesse_moyenne'] = self._calculer_vitesse_moyenne()
            
            # Densité moyenne du trafic
            stats['densite_moyenne'] = self.reseau.get_densite_trafic_moyenne()
            
            # Niveau de congestion
            stats['taux_congestion'] = self._calculer_taux_congestion()
            
            # Nombre total de véhicules
            stats['total_vehicules'] = self.reseau.get_nombre_total_vehicules()
            
            # Statistiques par route
            stats['routes'] = self._calculer_statistiques_routes()
            
            # Ajouter à l'historique de congestion
            self.historique_congestion.append(stats['taux_congestion'])
            
            return stats
        except (DonneesInvalideError, CalculStatistiquesError) as e:
            print(f"[ERREUR CALCUL STATISTIQUES TOUR] {e}")
            return {}
        except Exception as e:
            # Convertir toute autre erreur en erreur de calcul pour traçabilité
            print(f"[ERREUR CALCUL STATISTIQUES TOUR] {e}")
            return {}

    def _calculer_vitesse_moyenne(self) -> float:
        """
        Calcule la vitesse moyenne de tous les véhicules.
        
        Returns:
            float: Vitesse moyenne en km/h, 0 si aucun véhicule
        """
        try:
            if not hasattr(self, 'reseau') or self.reseau is None:
                raise DonneesInvalideError("Réseau introuvable pour calcul de vitesse moyenne")

            vitesses = []
            for route in self.reseau.routes.values():
                for vehicule in route.vehicules_presents.values():
                    if not hasattr(vehicule, 'vitesse'):
                        raise CalculStatistiquesError(f"Véhicule {getattr(vehicule,'identifiant', '<unk>')} sans attribut 'vitesse'")
                    vitesses.append(vehicule.vitesse)
            
            if not vitesses:
                return 0.0
            
            return statistics.mean(vitesses)
        except (DonneesInvalideError, CalculStatistiquesError) as e:
            print(f"[ERREUR CALCUL VITESSE MOYENNE] {e}")
            return 0.0
        except Exception as e:
            print(f"[ERREUR CALCUL VITESSE MOYENNE] {e}")
            return 0.0

    def _calculer_taux_congestion(self) -> float:
        """
        Calcule le taux de congestion global du réseau.
        
        Le taux de congestion est basé sur la densité du trafic
        et la réduction de vitesse par rapport aux limites.
        
        Returns:
            float: Taux de congestion entre 0 (fluide) et 100 (bouchon)
        """
        if not self.reseau.routes:
            return 0.0
        
        scores_congestion = []
        
        for route in self.reseau.routes.values():
            # Score basé sur la densité
            densite = route.get_densite_trafic()
            score_densite = min(densite / 50.0 * 100, 100)  # 50 véh/km = congestion max
            
            # Score basé sur la réduction de vitesse
            if route.vehicules_presents:
                vitesses = [v.vitesse for v in route.vehicules_presents.values()]
                vitesse_moyenne = statistics.mean(vitesses)
                reduction_vitesse = max(0, route.limite_vitesse - vitesse_moyenne)
                score_vitesse = min(reduction_vitesse / route.limite_vitesse * 100, 100)
            else:
                score_vitesse = 0
            
            # Prendre le score maximum entre densité et vitesse
            score_route = max(score_densite, score_vitesse)
            scores_congestion.append(score_route)
        
        return statistics.mean(scores_congestion) if scores_congestion else 0.0
    
    def _calculer_statistiques_routes(self) -> dict:
        """
        Calcule les statistiques détaillées pour chaque route.
        
        Returns:
            dict: Statistiques par route {nom_route: stats}
        """
        import statistics
        stats_routes = {}
        
        for nom_route, route in self.reseau.routes.items():
            vehicules = list(route.vehicules_presents.values())
            
            if vehicules:
                vitesses = [v.vitesse for v in vehicules]
                longueur_km = route.longueur / 1000
                utilisation = len(vehicules) / longueur_km if longueur_km > 0 else 0
                
                stats_routes[nom_route] = {
                    'nb_vehicules': len(vehicules),
                    'vitesse_moyenne': statistics.mean(vitesses) if vitesses else 0,
                    'vitesse_max': max(vitesses) if vitesses else 0,
                    'vitesse_min': min(vitesses) if vitesses else 0,
                    'densite': route.get_densite_trafic(),
                    'utilisation': utilisation,
                    'limite_vitesse': route.limite_vitesse,
                    'longueur': route.longueur
                }
            else:
                stats_routes[nom_route] = {
                    'nb_vehicules': 0,
                    'vitesse_moyenne': 0,
                    'vitesse_max': 0,
                    'vitesse_min': 0,
                    'densite': 0,
                    'utilisation': 0,
                    'limite_vitesse': route.limite_vitesse,
                    'longueur': route.longueur
                }
        
        return stats_routes
    
    def calculer_statistiques_globales(self) -> Dict:
        """
        Calcule les statistiques globales sur toute la simulation.
        
        Returns:
            dict: Statistiques globales résumées
        
        Example:
            >>> stats_globales = analyseur.calculer_statistiques_globales()
            >>> print(f"Congestion maximale: {stats_globales['congestion_max']}%")
        """
        if not hasattr(self.reseau, 'historique_trafic') or not self.reseau.historique_trafic:
            return {}
        
        # Extraire les données de l'historique
        total_vehicules = [etat['total_vehicules'] for etat in self.reseau.historique_trafic]
        densites = [etat['densite_moyenne'] for etat in self.reseau.historique_trafic]
        
        stats_globales = {
            'max_vehicules': max(total_vehicules) if total_vehicules else 0,
            'min_vehicules': min(total_vehicules) if total_vehicules else 0,
            'vehicules_moyens': statistics.mean(total_vehicules) if total_vehicules else 0,
            'densite_max': max(densites) if densites else 0,
            'densite_moyenne': statistics.mean(densites) if densites else 0,
            'congestion_max': max(self.historique_congestion) if self.historique_congestion else 0,
            'congestion_moyenne': statistics.mean(self.historique_congestion) if self.historique_congestion else 0,
        }
        
        # Calculer la vitesse moyenne globale
        vitesses_moyennes = [stats.get('vitesse_moyenne', 0) 
                           for stats in self.reseau.historique_trafic 
                           if 'vitesse_moyenne' in stats]
        if vitesses_moyennes:
            stats_globales['vitesse_moyenne_globale'] = statistics.mean(vitesses_moyennes)
        else:
            stats_globales['vitesse_moyenne_globale'] = 0
        
        return stats_globales
    
    def identifier_zones_congestion(self, seuil=70.0) -> List[Dict]:
        """
        Identifie les routes avec un niveau de congestion élevé.
        
        Args:
            seuil (float): Seuil de congestion en pourcentage (défaut: 70%)
        
        Returns:
            list: Liste des routes congestionnées avec leurs statistiques
        
        Example:
            >>> zones_congestion = analyseur.identifier_zones_congestion(seuil=80)
            >>> for zone in zones_congestion:
            ...     print(f"Route {zone['route']}: {zone['taux_congestion']}%")
        """
        routes_congestionnees = []
        stats_routes = self._calculer_statistiques_routes()
        
        for nom_route, stats in stats_routes.items():
            route = self.reseau.get_route(nom_route)
            if not route:
                continue
            
            # Calculer le taux de congestion pour cette route
            densite = stats['densite']
            score_densite = min(densite / 50.0 * 100, 100)
            
            reduction_vitesse = max(0, route.limite_vitesse - stats['vitesse_moyenne'])
            score_vitesse = min(reduction_vitesse / route.limite_vitesse * 100, 100)
            
            taux_congestion = max(score_densite, score_vitesse)
            
            if taux_congestion >= seuil:
                routes_congestionnees.append({
                    'route': nom_route,
                    'taux_congestion': taux_congestion,
                    'vehicules': stats['nb_vehicules'],
                    'vitesse_moyenne': stats['vitesse_moyenne'],
                    'limite_vitesse': route.limite_vitesse,
                    'densite': densite
                })
        
        # Trier par niveau de congestion décroissant
        routes_congestionnees.sort(key=lambda x: x['taux_congestion'], reverse=True)
        
        return routes_congestionnees
    
    def calculer_temps_parcours_moyen(self, longueur_parcours=1000) -> float:
        """
        Calcule le temps de parcours moyen pour une distance donnée.
        
        Args:
            longueur_parcours (float): Distance du parcours en mètres (défaut: 1000)
        
        Returns:
            float: Temps de parcours moyen en secondes
        """
        vitesse_moyenne = self._calculer_vitesse_moyenne()
        
        if vitesse_moyenne <= 0:
            return float('inf')
        
        # Convertir la vitesse moyenne en m/s
        vitesse_ms = vitesse_moyenne / 3.6
        
        # Calculer le temps de parcours
        temps_parcours = longueur_parcours / vitesse_ms
        
        return temps_parcours
    
    def generer_rapport_performance(self) -> Dict:
        """
        Génère un rapport complet de performance du réseau.
        
        Returns:
            dict: Rapport détaillé de performance
        """
        stats_globales = self.calculer_statistiques_globales()
        zones_congestion = self.identifier_zones_congestion()
        stats_actuelles = self.calculer_statistiques_tour()
        
        rapport = {
            'performance_generale': {
                'note': self._calculer_note_performance(stats_globales),
                'vitesse_moyenne': stats_globales.get('vitesse_moyenne_globale', 0),
                'congestion_moyenne': stats_globales.get('congestion_moyenne', 0),
                'efficacite_reseau': self._calculer_efficacite_reseau(stats_globales)
            },
            'zones_problematiques': zones_congestion,
            'statistiques_actuelles': stats_actuelles,
            'recommandations': self._generer_recommandations(zones_congestion)
        }
        
        return rapport
    
    def _calculer_note_performance(self, stats_globales) -> str:
        """Calcule une note de performance basée sur les statistiques."""
        congestion = stats_globales.get('congestion_moyenne', 0)
        
        if congestion < 20:
            return "Excellent"
        elif congestion < 40:
            return "Bon"
        elif congestion < 60:
            return "Moyen"
        elif congestion < 80:
            return "Médiocre"
        else:
            return "Critique"
    
    def _calculer_efficacite_reseau(self, stats_globales) -> float:
        """Calcule un score d'efficacité du réseau (0-100)."""
        congestion = stats_globales.get('congestion_moyenne', 100)
        return max(0, 100 - congestion)
    
    def _generer_recommandations(self, zones_congestion) -> List[str]:
        """Génère des recommandations basées sur les zones congestionnées."""
        recommandations = []
        
        if not zones_congestion:
            recommandations.append("✅ Le réseau fonctionne de manière optimale")
            return recommandations
        
        if len(zones_congestion) > 3:
            recommandations.append("🚨 Plusieurs routes sont congestionnées - envisager des itinéraires alternatifs")
        
        for zone in zones_congestion[:3]:  # Top 3 des zones problématiques
            rec = (f"🛣️  Route {zone['route']}: {zone['taux_congestion']:.1f}% de congestion - "
                   f"{zone['vehicules']} véhicules à {zone['vitesse_moyenne']:.1f} km/h")
            recommandations.append(rec)
        
        return recommandations
