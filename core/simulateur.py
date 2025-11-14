"""
Module Simulateur - Classe principale de simulation

Ce module définit la classe Simulateur qui orchestre la simulation complète
du trafic routier. Il gère le temps, met à jour le réseau et collecte les statistiques.
"""

import time
import json
from models.reseau import ReseauRoutier
from models.route import Route
from models.vehicule import Vehicule
from core.analyseur import Analyseur
from exceptions import SimulationInterrompueError, ErreurSimulationGenerale, SimulationNonInitialiseeError

class Simulateur:
    """
    Simulateur principal du trafic routier.
    
    Cette classe orchestre la simulation complète en gérant le temps,
    mettant à jour l'état du réseau, et collectant les statistiques.
    
    Attributes:
        reseau (ReseauRoutier): Réseau routier à simuler
        analyseur (Analyseur): Analyseur des statistiques de simulation
        temps_ecoule (float): Temps écoulé depuis le début de la simulation (secondes)
        historique_stats (list): Historique des statistiques à chaque pas de temps
        actif (bool): État de la simulation (en cours ou arrêtée)
    
    Example:
        >>> simulateur = Simulateur("data/config_reseau.json")
        >>> simulateur.lancer_simulation(n_tours=60, delta_t=60)
    """
    
    def __init__(self, fichier_config=None):
        """
        Initialise le simulateur avec un réseau.
        
        Args:
            fichier_config (str, optional): Chemin vers le fichier de configuration
        
        Raises:
            FileNotFoundError: Si le fichier de configuration n'existe pas
            json.JSONDecodeError: Si le fichier JSON est invalide
        """
        self.reseau = ReseauRoutier()
        self.analyseur = Analyseur(self.reseau)
        self.temps_ecoule = 0
        self.historique_stats = []
        self.actif = False
        
        if fichier_config:
            self.charger_configuration(fichier_config)
    
    def charger_configuration(self, fichier_config):
        """
        Charge la configuration du réseau depuis un fichier JSON.
        
        Args:
            fichier_config (str): Chemin vers le fichier de configuration JSON
        
        Example:
            >>> simulateur.charger_configuration("config/reseau_simple.json")
        """
        try:
            with open(fichier_config, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Créer les routes depuis la configuration
            for route_config in config.get('routes', []):
                route = Route(
                    nom=route_config['nom'],
                    longueur=route_config['longueur'],
                    limite_vitesse=route_config['limite_vitesse']
                )
                self.reseau.ajouter_route(route)
            
            # Configurer les intersections
            for intersection in config.get('intersections', []):
                route_source = intersection['source']
                for route_dest in intersection['destinations']:
                    self.reseau.ajouter_intersection(route_source, route_dest)
            
            # Ajouter des véhicules initiaux
            for vehicule_config in config.get('vehicules', []):
                vehicule = Vehicule(
                    identifiant=vehicule_config['id'],
                    route_actuelle=vehicule_config['route'],
                    position=vehicule_config.get('position', 0),
                    vitesse=vehicule_config.get('vitesse', 50)
                )
                route = self.reseau.get_route(vehicule_config['route'])
                if route:
                    route.ajouter_vehicule(vehicule)
            
            print(f"Configuration chargée: {len(self.reseau.routes)} routes, "
                  f"{self.reseau.get_nombre_total_vehicules()} véhicules initiaux")
                  
        except FileNotFoundError:
            print(f"⚠️  Fichier de configuration {fichier_config} non trouvé. "
                  "Utilisation d'un réseau vide.")
        except json.JSONDecodeError as e:
            print(f"❌ Erreur dans le fichier JSON: {e}")
        except KeyError as e:
            print(f"❌ Clé manquante dans la configuration: {e}")
    
    def lancer_simulation(self, n_tours=60, delta_t=60, afficher_progression=True, 
                     affichage_temps_reel=None):
        """
        Lance la simulation pour un nombre donné de pas de temps.
        Args:
        n_tours (int): Nombre de pas de simulation (défaut: 60)
        delta_t (float): Durée de chaque pas de simulation en secondes (défaut: 60)
        afficher_progression (bool): Afficher une barre de progression (défaut: True)
        affichage_temps_reel: Instance d'Affichage pour le tableau de bord temps réel

        """
        try:
            if not self.reseau or not self.reseau.routes:
                raise SimulationNonInitialiseeError("Le réseau routier n'est pas initialisé")

            self.actif = True
            print(f"🚀 Début de la simulation: {n_tours} tours de {delta_t} secondes")
            print(f"📊 État initial: {self.reseau.get_nombre_total_vehicules()} véhicules")
            
            for tour in range(n_tours):
                if not self.actif:
                    raise SimulationInterrompueError("Simulation arrêtée manuellement")
                
                try:
                    # Exécuter un pas de simulation
                    self._executer_pas_simulation(delta_t, tour)
                    
                    # Affichage temps réel si demandé (tous les 5 tours)
                    if affichage_temps_reel and (tour + 1) % 5 == 0:
                        affichage_temps_reel.mettre_a_jour(self.historique_stats[-1])
                    
                    # Afficher un résumé périodique
                    if (tour + 1) % 10 == 0:
                        self._afficher_resume(tour)
                        
                except Exception as e:
                    print(f"\n⚠️ Erreur au tour {tour}: {str(e)}")
                    raise ErreurSimulationGenerale(f"Erreur pendant le tour {tour}: {str(e)}")

            print(f"\n✅ Simulation terminée après {self.temps_ecoule:.0f} secondes")
            self._afficher_rapport_final()
                
        except SimulationNonInitialiseeError as e:
            print(f"\n❌ Erreur d'initialisation: {e}")
        except SimulationInterrompueError as e:
            print(f"\n⏹️ {e}")
        except ErreurSimulationGenerale as e:
            print(f"\n❌ Erreur critique: {e}")
        except KeyboardInterrupt:
            print("\n⏹️ Simulation interrompue par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur inattendue: {e}")
            raise
    
    def _executer_pas_simulation(self, delta_t, numero_tour):
        """
        Exécute un seul pas de simulation.
        
        Args:
            delta_t (float): Durée du pas en secondes
            numero_tour (int): Numéro du tour actuel
        """
        # Mettre à jour les véhicules
        self._mettre_a_jour_vehicules(delta_t)
        
        # Mettre à jour le réseau
        stats_reseau = self.reseau.mettre_a_jour_reseau()
        
        # Collecter les statistiques - FORCE route statistics collection
        stats_tour = self.analyseur.calculer_statistiques_tour()
        
        # Ensure route statistics are always included
        if 'routes' not in stats_tour:
            stats_tour['routes'] = self.analyseur._calculer_statistiques_routes()
        
        stats_tour.update({
            'tour': numero_tour,
            'temps_ecoule': self.temps_ecoule,
            'changements_route': stats_reseau['changements_route'],
            'vehicules_sortis': stats_reseau['vehicules_sortis']
        })
        
        self.historique_stats.append(stats_tour)
        self.temps_ecoule += delta_t
    
    def _mettre_a_jour_vehicules(self, delta_t):
        """
        Met à jour la position de tous les véhicules.
        """
        from core.fast_numba import update_positions
        for route in self.reseau.routes.values():
            # collect vehicle objects in stable order
            veh_list = list(route.vehicules_presents.values())
            if not veh_list:
                continue

            # prepare numeric arrays/lists
            positions = [v.position for v in veh_list]
            speeds = [v.vitesse for v in veh_list]
            limits = [route.limite_vitesse for _ in veh_list]
            lengths = [route.longueur for _ in veh_list]
            # use same density for all vehicles on this route (as in original code)
            dens = route.get_densite_trafic()
            densities = [dens for _ in veh_list]

            # call optimized updater
            new_positions_arr, new_speeds_arr = update_positions(positions, speeds, limits, lengths, densities, delta_t)

            # write back to vehicle objects
            for i, v in enumerate(veh_list):
                v.position = float(new_positions_arr[i])
                v.vitesse = float(new_speeds_arr[i])
    
    def _afficher_resume(self, tour):
        """
        Affiche un résumé périodique de la simulation.
        
        Args:
            tour (int): Numéro du tour actuel
        """
        stats_actuelles = self.historique_stats[-1] if self.historique_stats else {}
        
        print(f"\n--- Tour {tour} ---")
        print(f"⏱️  Temps écoulé: {self.temps_ecoule:.0f}s")
        print(f"🚗 Véhicules en circulation: {self.reseau.get_nombre_total_vehicules()}")
        print(f"📊 Vitesse moyenne: {stats_actuelles.get('vitesse_moyenne', 0):.1f} km/h")
        print(f"🚦 Densité moyenne: {stats_actuelles.get('densite_moyenne', 0):.1f} véh/km")
    
    def _afficher_rapport_final(self):
        """Affiche un rapport final de la simulation."""
        if not self.historique_stats:
            print("Aucune donnée collectée pendant la simulation")
            return
        
        stats_finales = self.analyseur.calculer_statistiques_globales()
        
        print("\n" + "="*50)
        print("📊 RAPPORT FINAL DE SIMULATION")
        print("="*50)
        print(f"⏱️  Durée totale: {self.temps_ecoule:.0f} secondes")
        print(f"🛣️  Routes simulées: {len(self.reseau.routes)}")
        print(f"🚗 Véhicules maximum: {stats_finales.get('max_vehicules', 0)}")
        print(f"📈 Vitesse moyenne globale: {stats_finales.get('vitesse_moyenne_globale', 0):.1f} km/h")
        print(f"🚨 Congestion maximale: {stats_finales.get('congestion_max', 0):.1f}%")
        print("="*50)
    
    def arreter_simulation(self):
        """Arrête la simulation en cours."""
        self.actif = False
        print("⏹️  Simulation arrêtée")
    
    def get_statistiques(self):
        """
        Retourne l'historique complet des statistiques.
        
        Returns:
            list: Historique des statistiques à chaque pas de temps
        """
        return self.historique_stats
    
    def __str__(self):
        """
        Représentation textuelle du simulateur.
        
        Returns:
            str: Description du simulateur
        """
        return (f"Simulateur: {len(self.reseau.routes)} routes, "
                f"{self.reseau.get_nombre_total_vehicules()} véhicules, "
                f"temps écoulé: {self.temps_ecoule:.0f}s")
