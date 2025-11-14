"""
Module ReseauRoutier - Définition de la classe ReseauRoutier

Ce module définit la classe ReseauRoutier qui représente l'ensemble
du réseau routier. Elle gère toutes les routes, les intersections
et la logique globale de simulation.
"""

from typing import Dict, List, Optional
from exceptions import RouteDejaExistanteError, RouteInexistanteError

class ReseauRoutier:
    """
    Représente l'ensemble du réseau routier.
    
    Le réseau routier contient toutes les routes et gère les connections
    entre elles. Il orchestre la simulation globale du trafic.
    
    Attributes:
        routes (dict): Dictionnaire des routes {nom_route: objet_route}
        intersections (dict): Dictionnaire des connections entre routes
        historique_trafic (list): Historique des états du trafic
    
    Example:
        >>> reseau = ReseauRoutier()
        >>> route1 = Route("Route_A", 1000, 90)
        >>> reseau.ajouter_route(route1)
        >>> reseau.ajouter_intersection("Route_A", "Route_B")
    """
    
    def __init__(self):
        """
        Initialise un nouveau réseau routier vide.
        
        Le réseau commence sans routes ni intersections.
        L'historique du trafic est initialisé vide.
        """
        self.routes = {}  # {nom_route: Route}
        self.intersections = {}  # {route_source: [routes_destination]}
        self.historique_trafic = []
    
    def ajouter_route(self, route):
        """
        Ajoute une route au réseau.
        
        Args:
            route (Route): Route à ajouter au réseau
        
        Raises:
            ValueError: Si une route avec le même nom existe déjà
        
        Example:
            >>> reseau = ReseauRoutier()
            >>> route = Route("Autoroute_A1", 5000, 130)
            >>> reseau.ajouter_route(route)
        """
        try:
            if route.nom in self.routes:
                raise RouteDejaExistanteError(f"Une route avec le nom '{route.nom}' existe déjà")
            
            self.routes[route.nom] = route
            # Initialiser les intersections pour cette route
            if route.nom not in self.intersections:
                self.intersections[route.nom] = []
        except RouteDejaExistanteError as e:
            print(f"[ERREUR AJOUT ROUTE] {e}")
    
    def ajouter_intersection(self, route_source, route_destination):
        """
        Ajoute une connection entre deux routes.
        
        Crée une intersection permettant aux véhicules de passer
        de la route source à la route destination.
        
        Args:
            route_source (str): Nom de la route de départ
            route_destination (str): Nom de la route d'arrivée
        
        Raises:
            ValueError: Si une des routes n'existe pas
        
        Example:
            >>> reseau.ajouter_intersection("Route_A", "Route_B")
        """
        try:
            if route_source not in self.routes:
                raise RouteInexistanteError(f"La route source '{route_source}' n'existe pas")
            if route_destination not in self.routes:
                raise RouteInexistanteError(f"La route destination '{route_destination}' n'existe pas")
            
            if route_destination not in self.intersections[route_source]:
                self.intersections[route_source].append(route_destination)
        except RouteInexistanteError as e:
            print(f"[ERREUR INTERSECTION] {e}")
    
    def get_route(self, nom_route):
        """
        Récupère une route par son nom.
        
        Args:
            nom_route (str): Nom de la route à récupérer
        
        Returns:
            Route: La route correspondante ou None si non trouvée
        
        Example:
            >>> route = reseau.get_route("Autoroute_A1")
            >>> if route:
            ...     print(f"Route trouvée: {route.nom}")
        """
        return self.routes.get(nom_route)
    
    def get_routes_destination(self, route_source):
        """
        Récupère les routes accessibles depuis une route source.
        
        Args:
            route_source (str): Nom de la route de départ
        
        Returns:
            list: Liste des noms des routes accessibles
        
        Example:
            >>> destinations = reseau.get_routes_destination("Route_A")
            >>> print(destinations)
            ['Route_B', 'Route_C']
        """
        return self.intersections.get(route_source, [])
    
    def get_nombre_total_vehicules(self):
        """
        Calcule le nombre total de véhicules dans tout le réseau.
        
        Returns:
            int: Nombre total de véhicules
        
        Example:
            >>> total = reseau.get_nombre_total_vehicules()
            >>> print(f"Véhicules en circulation: {total}")
        """
        total = 0
        for route in self.routes.values():
            total += route.get_nombre_vehicules()
        return total
    
    def mettre_a_jour_reseau(self):
        """
        Met à jour l'état complet du réseau.
        
        Cette méthode met à jour toutes les routes et gère les véhicules
        qui changent de route aux intersections.
        
        Returns:
            dict: Statistiques de la mise à jour
        
        Example:
            >>> stats = reseau.mettre_a_jour_reseau()
            >>> print(f"Véhicules ayant changé de route: {stats['changements_route']}")
        """
        stats = {
            'changements_route': 0,
            'vehicules_sortis': 0
        }
        
        # Mettre à jour chaque route et collecter les véhicules sortants
        for nom_route, route in self.routes.items():
            vehicules_sortis = route.mettre_a_jour_vehicules()
            stats['vehicules_sortis'] += len(vehicules_sortis)
            
            # Pour chaque véhicule sortant, le déplacer vers une route suivante si possible
            for vehicule in vehicules_sortis:
                routes_destination = self.get_routes_destination(nom_route)
                if routes_destination:
                    # Choisir la première route disponible (logique simple)
                    nouvelle_route = routes_destination[0]
                    route_dest = self.get_route(nouvelle_route)
                    if route_dest:
                        vehicule.changer_de_route(nouvelle_route, 0)
                        route_dest.ajouter_vehicule(vehicule)
                        stats['changements_route'] += 1
        
        # Enregistrer l'état actuel du trafic dans l'historique
        etat_trafic = {
            'timestamp': len(self.historique_trafic),
            'total_vehicules': self.get_nombre_total_vehicules(),
            'densite_moyenne': self.get_densite_trafic_moyenne()
        }
        self.historique_trafic.append(etat_trafic)
        
        return stats
    
    def get_densite_trafic_moyenne(self):
        """
        Calcule la densité de trafic moyenne sur toutes les routes.
        
        Returns:
            float: Densité moyenne (véhicules/km)
        
        Example:
            >>> densite_moyenne = reseau.get_densite_trafic_moyenne()
            >>> print(f"Densité moyenne: {densite_moyenne:.2f} véhicules/km")
        """
        if not self.routes:
            return 0
        
        total_densite = 0
        for route in self.routes.values():
            total_densite += route.get_densite_trafic()
        
        return total_densite / len(self.routes)
    
    def __str__(self):
        """
        Représentation textuelle du réseau routier.
        
        Returns:
            str: Description du réseau
        """
        return f"Réseau routier avec {len(self.routes)} routes et {self.get_nombre_total_vehicules()} véhicules"
    
    def __repr__(self):
        """
        Représentation technique du réseau routier.
        
        Returns:
            str: Représentation pouvant être utilisée pour recréer l'objet
        """
        return f"ReseauRoutier(nb_routes={len(self.routes)}, nb_vehicules={self.get_nombre_total_vehicules()})"

