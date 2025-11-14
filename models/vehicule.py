"""
Module Vehicule - Définition de la classe Vehicule

Ce module définit la classe Vehicule qui représente un véhicule
dans la simulation de trafic routier. Chaque véhicule a une position,
une vitesse, et peut se déplacer sur différentes routes.
"""

from exceptions import (
    PositionInvalideError,
    VitesseInvalideError,
    DistanceInvalideError,
)

class Vehicule:
    """
    Représente un véhicule dans le simulateur de trafic.
    """

    def __init__(self, identifiant, route_actuelle, position=0, vitesse=0):
        """
        Initialise un nouveau véhicule.
        Gère les erreurs d’entrée sans provoquer l’arrêt du programme.
        """
        try:
            if identifiant < 0:
                raise ValueError("L'identifiant doit être un nombre positif.")
            if position < 0:
                raise PositionInvalideError("La position ne peut pas être négative.")
            if vitesse < 0:
                raise VitesseInvalideError("La vitesse ne peut pas être négative.")
            
            self.identifiant = identifiant
            self.route_actuelle = route_actuelle
            self.position = position
            self.vitesse = vitesse
            self.historique_routes = [route_actuelle]

        except (ValueError, PositionInvalideError, VitesseInvalideError) as e:
            # On signale l’erreur mais on empêche l’arrêt brutal
            print(f"[Erreur] Initialisation du véhicule échouée ({identifiant}) : {e}")
            # Valeurs par défaut de secours
            self.identifiant = identifiant if identifiant >= 0 else 0
            self.route_actuelle = route_actuelle or "Route_Inconnue"
            self.position = max(0, position)
            self.vitesse = max(0, vitesse)
            self.historique_routes = [self.route_actuelle]

    def avancer(self, distance):
        """
        Déplace le véhicule vers l'avant sur sa route actuelle.
        Gère les valeurs invalides sans lever d’exception.
        """
        try:
            if distance < 0:
                raise DistanceInvalideError("La distance ne peut pas être négative.")
            if self.vitesse < 0:
                raise VitesseInvalideError("La vitesse ne peut pas être négative.")

            nouvelle_position = self.position + distance
            if nouvelle_position < 0:
                raise PositionInvalideError("La position calculée est invalide.")

            self.position = nouvelle_position

        except (DistanceInvalideError, VitesseInvalideError, PositionInvalideError) as e:
            print(f"[Erreur] Impossible de faire avancer le véhicule {self.identifiant} : {e}")

    def changer_de_route(self, nouvelle_route, nouvelle_position=0):
        """
        Change la route actuelle du véhicule sans lever d’exception.
        """
        try:
            if not nouvelle_route:
                raise ValueError("Le nom de la nouvelle route est vide.")
            if nouvelle_position < 0:
                raise PositionInvalideError("La position sur la nouvelle route ne peut pas être négative.")

            self.route_actuelle = nouvelle_route
            self.position = nouvelle_position
            self.historique_routes.append(nouvelle_route)

        except (ValueError, PositionInvalideError) as e:
            print(f"[Erreur] Changement de route impossible pour le véhicule {self.identifiant} : {e}")

    def __str__(self):
        return (
            f"Véhicule {self.identifiant} sur {self.route_actuelle} "
            f"à position {self.position}m, vitesse {self.vitesse}km/h"
        )

    def __repr__(self):
        return (
            f"Vehicule(identifiant={self.identifiant}, "
            f"route_actuelle='{self.route_actuelle}', "
            f"position={self.position}, vitesse={self.vitesse})"
        )
