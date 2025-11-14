"""
Module FeuRouge - Définition de la classe FeuRouge

Ce module définit la classe FeuRouge qui représente un feu de circulation
dans la simulation de trafic routier. Le feu alterne entre les états
rouge, vert et orange selon un cycle configurable.
"""

from exceptions import CycleInvalideError

class FeuRouge:
    """
    Représente un feu de circulation dans le simulateur de trafic.
    
    Le feu alterne cycliquement entre trois états : rouge, vert, orange.
    Le timing de chaque état peut être configuré via le cycle.
    
    Attributes:
        cycle (dict): Configuration du cycle {état: durée}
        temps_ecoule (float): Temps écoulé depuis le dernier changement d'état
        etat_actuel (str): État courant du feu ('rouge', 'vert', 'orange')
        ordre_etats (list): Ordre de transition des états
    
    Example:
        >>> feu = FeuRouge(cycle=5)
        >>> feu.etat
        'rouge'
        >>> feu.avancer_temps(3)
        >>> feu.etat
        'rouge'
        >>> feu.avancer_temps(3)
        >>> feu.etat
        'vert'
    """
    
    def __init__(self, cycle=5):
        """
        Initialise un nouveau feu de circulation.
        
        Args:
            cycle (int or dict): Si int, durée égale pour tous les états.
                               Si dict, configuration personnalisée du cycle.
        
        Raises:
            CycleInvalideError: Si le cycle est invalide
        
        Example:
            >>> feu1 = FeuRouge(5)  # Cycle standard de 5 secondes par état
            >>> feu2 = FeuRouge({'rouge': 10, 'vert': 8, 'orange': 2})  # Cycle personnalisé
        """
        try:
            self.temps_ecoule = 0.0
            self.ordre_etats = ['rouge', 'vert', 'orange']
            
            if isinstance(cycle, (int, float)):
                if cycle <= 0:
                    raise CycleInvalideError(f"La durée du cycle doit être positive (valeur: {cycle})")
                # Cycle standard : durée égale pour tous les états
                self.cycle = {etat: cycle for etat in self.ordre_etats}
            elif isinstance(cycle, dict):
                # Vérifier que tous les états nécessaires sont présents
                etats_manquants = [etat for etat in self.ordre_etats if etat not in cycle]
                if etats_manquants:
                    raise CycleInvalideError(f"États manquants dans le cycle: {etats_manquants}")
                
                # Vérifier que les durées sont positives
                for etat, duree in cycle.items():
                    if duree <= 0:
                        raise CycleInvalideError(f"Durée invalide pour l'état '{etat}': {duree}")
                
                self.cycle = cycle.copy()
            else:
                raise CycleInvalideError(f"Type de cycle non supporté: {type(cycle)}")
            
            # Commencer avec l'état rouge
            self.etat_actuel = 'rouge'
            
        except CycleInvalideError as e:
            print(f"[ERREUR INIT FEU ROUGE] {e}")
            # Valeurs par défaut de secours
            self.cycle = {'rouge': 5, 'vert': 5, 'orange': 5}
            self.etat_actuel = 'rouge'
            self.temps_ecoule = 0.0
            self.ordre_etats = ['rouge', 'vert', 'orange']

    @property
    def etat(self):
        """
        Retourne l'état actuel du feu.
        
        Returns:
            str: État actuel ('rouge', 'vert', 'orange')
        
        Example:
            >>> feu = FeuRouge()
            >>> feu.etat
            'rouge'
        """
        return self.etat_actuel

    def avancer_temps(self, dt):
        """
        Fait avancer le temps et change l'état si nécessaire.
        
        Args:
            dt (float): Temps écoulé en secondes
        
        Example:
            >>> feu = FeuRouge(5)
            >>> feu.avancer_temps(3)  # Feu toujours rouge
            >>> feu.avancer_temps(3)  # Feu passe à vert
        """
        try:
            if dt < 0:
                raise ValueError(f"L'intervalle de temps ne peut pas être négatif: {dt}")
            
            self.temps_ecoule += dt
            duree_etat_actuel = self.cycle[self.etat_actuel]
            
            # Vérifier si on doit changer d'état
            while self.temps_ecoule >= duree_etat_actuel:
                self.temps_ecoule -= duree_etat_actuel
                self._changer_etat()
                duree_etat_actuel = self.cycle[self.etat_actuel]
                
        except ValueError as e:
            print(f"[ERREUR TEMPS FEU] {e}")

    def _changer_etat(self):
        """
        Passe à l'état suivant dans le cycle.
        Méthode interne utilisée par avancer_temps.
        """
        index_actuel = self.ordre_etats.index(self.etat_actuel)
        index_suivant = (index_actuel + 1) % len(self.ordre_etats)
        self.etat_actuel = self.ordre_etats[index_suivant]

    def get_prochain_changement(self):
        """
        Retourne le temps restant avant le prochain changement d'état.
        
        Returns:
            float: Temps restant en secondes
        
        Example:
            >>> feu = FeuRouge(5)
            >>> feu.avancer_temps(2)
            >>> feu.get_prochain_changement()
            3.0
        """
        duree_etat_actuel = self.cycle[self.etat_actuel]
        return duree_etat_actuel - self.temps_ecoule

    def get_cycle_total(self):
        """
        Retourne la durée totale d'un cycle complet.
        
        Returns:
            float: Durée totale du cycle en secondes
        
        Example:
            >>> feu = FeuRouge({'rouge': 10, 'vert': 8, 'orange': 2})
            >>> feu.get_cycle_total()
            20.0
        """
        return sum(self.cycle.values())

    def __str__(self):
        """
        Représentation textuelle du feu rouge.
        
        Returns:
            str: Description du feu
        """
        temps_restant = self.get_prochain_changement()
        return f"FeuRouge(état='{self.etat_actuel}', changement dans {temps_restant:.1f}s)"

    def __repr__(self):
        """
        Représentation technique du feu rouge.
        
        Returns:
            str: Représentation pouvant être utilisée pour recréer l'objet
        """
        return f"FeuRouge(cycle={self.cycle})"