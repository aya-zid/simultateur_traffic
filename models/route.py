"""
Module Route - Définition de la classe Route

Ce module définit la classe Route qui représente une route
dans le réseau routier. Une route a une longueur, une limite de vitesse,
et peut contenir plusieurs véhicules.
"""
from exceptions import (
    LongueurInvalideError,
    LimiteVitesseInvalideError,
    VehiculeDejaPresentError,
    PositionVehiculeInvalideError,
    AucuneMiseAJourPossibleError
)



class Route:
    """
    Représente une route dans le réseau routier.
    
    Une route est caractérisée par son nom, sa longueur, sa limite de vitesse
    et la liste des véhicules qui s'y trouvent.
    
    Attributes:
        nom (str): Nom identifiant de la route
        longueur (float): Longueur totale de la route (en mètres)
        limite_vitesse (float): Limite de vitesse autorisée (en km/h)
        vehicules_presents (dict): Véhicules sur la route {id_vehicule: véhicule}
    
    Example:
        >>> route = Route("Autoroute_A1", 10000, 130)
        >>> voiture = Vehicule(1, "Autoroute_A1")
        >>> route.ajouter_vehicule(voiture)
        >>> len(route.vehicules_presents)
        1
    """
    
    def __init__(self, nom, longueur, limite_vitesse):
        """
        Initialise une nouvelle route.
        
        Args:
            nom (str): Nom de la route
            longueur (float): Longueur de la route en mètres
            limite_vitesse (float): Limite de vitesse en km/h
        
        Raises:
            ValueError: Si la longueur ou la limite de vitesse est négative
        """
        try:
            if longueur <= 0:
                raise LongueurInvalideError(f"La longueur de la route '{nom}' doit être positive (valeur: {longueur})")
            if limite_vitesse <= 0:
                raise LimiteVitesseInvalideError(f"La limite de vitesse doit être positive (valeur: {limite_vitesse})")
                
            self.nom = nom
            self.longueur = longueur
            self.limite_vitesse = limite_vitesse
            self.vehicules_presents = {}  # Dictionnaire {id: vehicule}
        
        except (LongueurInvalideError, LimiteVitesseInvalideError) as e:
            print(f"[ERREUR INIT ROUTE] {e}")
            

    def ajouter_vehicule(self, vehicule):
        """
        Ajoute un véhicule à la route.
        
        Le véhicule est ajouté à la liste des véhicules présents sur la route.
        Vérifie que le véhicule n'est pas déjà présent et que sa position est valide.
        
        Args:
            vehicule (Vehicule): Véhicule à ajouter à la route
        
        Raises:
            ValueError: Si le véhicule est déjà sur la route ou position invalide
        
        Example:
            >>> route = Route("Route_A", 1000, 90)
            >>> voiture = Vehicule(1, "Route_A")
            >>> route.ajouter_vehicule(voiture)
        """
        try:
            if vehicule.identifiant in self.vehicules_presents:
                raise VehiculeDejaPresentError(
                    f"Le véhicule {vehicule.identifiant} est déjà sur la route '{self.nom}'"
                )
    
            if vehicule.position > self.longueur:
                raise PositionVehiculeInvalideError(
                    f"Position {vehicule.position} dépasse la longueur maximale de la route ({self.longueur})"
                )
    
            self.vehicules_presents[vehicule.identifiant] = vehicule
            vehicule.route_actuelle = self.nom
    
        except (VehiculeDejaPresentError, PositionVehiculeInvalideError) as e:
            print(f"[ERREUR AJOUT VEHICULE] {e}")
            

    def supprimer_vehicule(self, identifiant_vehicule):
        """
        Supprime un véhicule de la route.
        
        Args:
            identifiant_vehicule (int): Identifiant du véhicule à supprimer
        
        Returns:
            Vehicule: Le véhicule supprimé ou None si non trouvé
        
        Example:
            >>> route.supprimer_vehicule(1)
            <Vehicule object at 0x...>
        """
        return self.vehicules_presents.pop(identifiant_vehicule, None)
    
    def mettre_a_jour_vehicules(self):
        """
        Met à jour tous les véhicules sur la route.
        Cette méthode devrait être appelée à chaque pas de simulation
        pour mettre à jour les positions et gérer les véhicules qui
        quittent la route.
        Returns:
            list: Liste des véhicules qui ont quitté la route
        Example:
            >>> vehicules_sortis = route.mettre_a_jour_vehicules()
            >>> for vehicule in vehicules_sortis:
            ...     print(f"Véhicule {vehicule.identifiant} a quitté la route")
        """
        try:
            if not self.vehicules_presents:
                raise AucuneMiseAJourPossibleError(
                    f"Aucun véhicule présent sur la route '{self.nom}', mise à jour impossible."
                )
            vehicules_sortis = []
            vehicules_a_supprimer = []
            for identifiant, vehicule in self.vehicules_presents.items():
                # Vérifier si le véhicule a dépassé la fin de la route
                if vehicule.position >= self.longueur:
                    vehicules_sortis.append(vehicule)
                    vehicules_a_supprimer.append(identifiant)
            # Supprimer les véhicules qui ont quitté la route
            for identifiant in vehicules_a_supprimer:
                self.supprimer_vehicule(identifiant)
            return vehicules_sortis
        except AucuneMiseAJourPossibleError as e:
            print(f"[ERREUR MISE À JOUR] {e}")
            return []
    
    def get_nombre_vehicules(self):
        """
        Retourne le nombre de véhicules actuellement sur la route.
        
        Returns:
            int: Nombre de véhicules présents
        
        Example:
            >>> route.get_nombre_vehicules()
            5
        """
        return len(self.vehicules_presents)
    
    def get_densite_trafic(self):
        """
        Calcule la densité du trafic sur la route.
        
        La densité est calculée comme le nombre de véhicules par kilomètre.
        
        Returns:
            float: Densité de trafic (véhicules/km)
        
        Example:
            >>> route.get_densite_trafic()
            25.8
        """
        longueur_km = self.longueur / 1000  # Conversion en kilomètres
        if longueur_km == 0:
            return 0
        return len(self.vehicules_presents) / longueur_km
    
    def __str__(self):
        """
        Représentation textuelle de la route.
        
        Returns:
            str: Description de la route
        """
        return f"Route '{self.nom}' ({self.longueur}m, limite: {self.limite_vitesse}km/h, {len(self.vehicules_presents)} véhicules)"
    
    def __repr__(self):
        """
        Représentation technique de la route.
        
        Returns:
            str: Représentation pouvant être utilisée pour recréer l'objet
        """
        return f"Route(nom='{self.nom}', longueur={self.longueur}, limite_vitesse={self.limite_vitesse})"
