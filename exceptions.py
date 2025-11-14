"""
Module Exceptions - Définitions des exceptions personnalisées
pour le simulateur de trafic routier.
"""

# Exception de base pour tout le simulateur
class SimulationError(Exception):
    """Exception de base pour toutes les erreurs du simulateur."""
    pass

class VehiculeError(SimulationError):
    """Exception générale liée aux véhicules."""
    pass
# -----------------------------
# Exceptions liées a la classe vehicule
# -----------------------------

class PositionInvalideError(VehiculeError):
    """Levée quand une position négative ou invalide est détectée."""
    pass

class VitesseInvalideError(VehiculeError):
    """Levée quand la vitesse d'un véhicule est invalide (ex : négative)."""
    pass

class DistanceInvalideError(VehiculeError):
    """Levée quand la distance fournie à 'avancer' est invalide."""
    pass

# -----------------------------
# Exceptions liées a la classe route
# -----------------------------
class LongueurInvalideError(ValueError):
    """Levée lorsque la longueur d'une route est invalide (<= 0)."""
    pass

class LimiteVitesseInvalideError(ValueError):
    """Levée lorsque la limite de vitesse d'une route est invalide (<= 0)."""
    pass

class VehiculeDejaPresentError(ValueError):
    """Levée lorsqu'on tente d'ajouter un véhicule déjà présent sur la route."""
    pass

class PositionVehiculeInvalideError(ValueError):
    """Levée lorsque la position d'un véhicule dépasse la longueur de la route."""
    pass

class AucuneMiseAJourPossibleError(RuntimeError):
    """Levée lorsque la mise à jour des véhicules est impossible (aucun véhicule sur la route)."""
    pass
class PositionFeuInvalideError(Exception):
    """Exception levée lorsqu'un feu rouge est placé à une position invalide sur une route."""
    pass
# -----------------------------
# Exceptions liées a la classe reseau
# -----------------------------

class RouteDejaExistanteError(ValueError):
    """Levée lorsqu'une route avec le même nom existe déjà dans le réseau."""
    pass

class RouteInexistanteError(ValueError):
    """Levée lorsqu'une route spécifiée n'existe pas dans le réseau routier."""
    pass

# -----------------------------
# Exceptions liées a la classe simulateur
# -----------------------------
class SimulationInterrompueError(Exception):
    """Levée lorsqu'une simulation est interrompue manuellement par l'utilisateur."""
    pass

class ErreurSimulationGenerale(Exception):
    """Levée lorsqu'une erreur inattendue survient pendant la simulation."""
    pass

class SimulationNonInitialiseeError(Exception):
    """Raised when simulation starts without proper initialization"""
    pass

# -----------------------------
# Exceptions liées a la classe analyseur
# -----------------------------
class AnalyseurError(Exception):
    """Erreur générale liée à l'analyse des statistiques."""
    pass

class DonneesInvalideError(AnalyseurError):
    """Données attendues par l'analyseur manquantes ou invalides."""
    pass

class CalculStatistiquesError(AnalyseurError):
    """Erreur survenue lors du calcul des statistiques."""
    pass
# -----------------------------
# Exceptions liées a la classe FeuRouge
# -----------------------------
class CycleInvalideError(Exception):
    """Exception levée lorsqu'un cycle de feu rouge est invalide."""
    pass