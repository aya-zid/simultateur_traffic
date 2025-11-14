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
    AucuneMiseAJourPossibleError,
    PositionFeuInvalideError
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
        feux_rouges (dict): Feux rouges sur la route {position: FeuRouge}
    
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
            self.feux_rouges = {}  # Dictionnaire {position: FeuRouge}
        
        except (LongueurInvalideError, LimiteVitesseInvalideError) as e:
            print(f"[ERREUR INIT ROUTE] {e}")
            
    def ajouter_feu_rouge(self, feu, position=None):
        """
        Ajoute un feu rouge à la route à la position donnée.
        
        Args:
            feu (FeuRouge): Feu rouge à ajouter
            position (float): Position sur la route en mètres. Si None, place à la fin.
        
        Raises:
            PositionFeuInvalideError: Si la position est invalide
        
        Example:
            >>> route = Route("Route_A", 1000, 90)
            >>> feu = FeuRouge(cycle=5)
            >>> route.ajouter_feu_rouge(feu, position=500)
        """
        try:
            if position is None:
                position = self.longueur  # Par défaut à la fin de la route
            
            if position < 0 or position > self.longueur:
                raise PositionFeuInvalideError(
                    f"Position du feu invalide: {position}. Doit être entre 0 et {self.longueur}"
                )
            
            # Vérifier s'il y a déjà un feu à cette position
            if position in self.feux_rouges:
                print(f"[ATTENTION] Remplacement du feu existant à la position {position}")
            
            self.feux_rouges[position] = feu
            print(f"Feu rouge ajouté à la position {position}m sur la route '{self.nom}'")
            
        except PositionFeuInvalideError as e:
            print(f"[ERREUR AJOUT FEU] {e}")

    def _doit_arreter_vehicule(self, vehicule, distance_proposee):
        """
        Détermine si un véhicule doit s'arrêter à cause d'un feu rouge.
        
        Args:
            vehicule (Vehicule): Véhicule à vérifier
            distance_proposee (float): Distance que le véhicule veut parcourir
        
        Returns:
            bool: True si le véhicule doit s'arrêter
        """
        nouvelle_position = vehicule.position + distance_proposee
        
        # Vérifier chaque feu rouge sur la route
        for position_feu, feu in self.feux_rouges.items():
            # Si le véhicule va traverser la position du feu
            if vehicule.position < position_feu <= nouvelle_position:
                if feu.etat in ['rouge', 'orange']:
                    return True
        return False

    def _get_distance_avant_obstacle(self, vehicule, distance_max):
        """
        Calcule la distance que le véhicule peut parcourir avant un obstacle.
        
        Args:
            vehicule (Vehicule): Véhicule à vérifier
            distance_max (float): Distance maximale souhaitée
        
        Returns:
            float: Distance réelle que le véhicule peut parcourir
        """
        distance_possible = distance_max
        
        # Vérifier les feux rouges
        for position_feu, feu in self.feux_rouges.items():
            if vehicule.position < position_feu <= vehicule.position + distance_max:
                if feu.etat in ['rouge', 'orange']:
                    # Le véhicule doit s'arrêter avant le feu
                    distance_avant_feu = position_feu - vehicule.position - 5  # Marge de sécurité
                    if distance_avant_feu < distance_possible:
                        distance_possible = max(0, distance_avant_feu)
        
        # Vérifier la fin de la route
        distance_fin_route = self.longueur - vehicule.position
        if distance_fin_route < distance_possible:
            distance_possible = max(0, distance_fin_route)
        
        return distance_possible

    def mettre_a_jour_vehicules(self, dt=1.0):
        """
        Met à jour tous les véhicules sur la route.
        Cette méthode devrait être appelée à chaque pas de simulation
        pour mettre à jour les positions et gérer les véhicules qui
        quittent la route.
        
        Args:
            dt (float): Intervalle de temps en secondes pour la mise à jour
        
        Returns:
            list: Liste des véhicules qui ont quitté la route
        
        Example:
            >>> vehicules_sortis = route.mettre_a_jour_vehicules(dt=1.0)
            >>> for vehicule in vehicules_sortis:
            ...     print(f"Véhicule {vehicule.identifiant} a quitté la route")
        """
        try:
            # Mettre à jour tous les feux rouges
            for feu in self.feux_rouges.values():
                feu.avancer_temps(dt)
            
            if not self.vehicules_presents:
                raise AucuneMiseAJourPossibleError(
                    f"Aucun véhicule présent sur la route '{self.nom}', mise à jour impossible."
                )
            
            vehicules_sortis = []
            vehicules_a_supprimer = []
            
            for identifiant, vehicule in self.vehicules_presents.items():
                # Calculer la distance que le véhicule souhaite parcourir
                vitesse_ms = vehicule.vitesse * 1000 / 3600  # Conversion km/h -> m/s
                distance_souhaitee = vitesse_ms * dt
                
                # Déterminer la distance réelle en tenant compte des feux
                distance_reelle = self._get_distance_avant_obstacle(vehicule, distance_souhaitee)
                
                # Faire avancer le véhicule
                if distance_reelle > 0:
                    vehicule.avancer(distance_reelle)
                
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
    
    def get_nombre_feux(self):
        """
        Retourne le nombre de feux rouges sur la route.
        
        Returns:
            int: Nombre de feux rouges
        
        Example:
            >>> route.get_nombre_feux()
            2
        """
        return len(self.feux_rouges)
    
    def get_etat_feux(self):
        """
        Retourne l'état de tous les feux de la route.
        
        Returns:
            dict: Dictionnaire {position: état_du_feu}
        
        Example:
            >>> route.get_etat_feux()
            {500: 'rouge', 800: 'vert'}
        """
        return {position: feu.etat for position, feu in self.feux_rouges.items()}
    
    def __str__(self):
        """
        Représentation textuelle de la route.
        
        Returns:
            str: Description de la route
        """
        return (f"Route '{self.nom}' ({self.longueur}m, limite: {self.limite_vitesse}km/h, "
                f"{len(self.vehicules_presents)} véhicules, {len(self.feux_rouges)} feux)")
    
    def __repr__(self):
        """
        Représentation technique de la route.
        
        Returns:
            str: Représentation pouvant être utilisée pour recréer l'objet
        """
        return f"Route(nom='{self.nom}', longueur={self.longueur}, limite_vitesse={self.limite_vitesse})"