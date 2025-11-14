Exemples
========

Exemple Basique
---------------

L'exemple le plus simple pour démarrer:

.. code-block:: python

   from simulateur_trafic.core.simulateur import Simulateur
   
   # Simulation avec configuration par défaut
   simulateur = Simulateur()
   simulateur.lancer_simulation(n_tours=60, delta_t=60)

Exemple avec Configuration Personnalisée
----------------------------------------

Création d'un réseau personnalisé:

.. code-block:: python

   from simulateur_trafic.models.vehicule import Vehicule
   from simulateur_trafic.models.route import Route
   from simulateur_trafic.models.reseau import ReseauRoutier
   from simulateur_trafic.core.simulateur import Simulateur
   
   # Création manuelle du réseau
   reseau = ReseauRoutier()
   
   # Ajouter des routes
   route1 = Route("Autoroute_Nord", 5000, 110)
   route2 = Route("Route_Principale", 3000, 90)
   reseau.ajouter_route(route1)
   reseau.ajouter_route(route2)
   
   # Créer une intersection
   reseau.ajouter_intersection("Autoroute_Nord", "Route_Principale")
   
   # Ajouter des véhicules
   voiture1 = Vehicule(1, "Autoroute_Nord", position=0, vitesse=100)
   voiture2 = Vehicule(2, "Route_Principale", position=500, vitesse=80)
   route1.ajouter_vehicule(voiture1)
   route2.ajouter_vehicule(voiture2)
   
   # Simulateur avec réseau personnalisé
   simulateur = Simulateur()
   simulateur.reseau = reseau
   simulateur.lancer_simulation(n_tours=50, delta_t=30)

Exemple avec Analyse Avancée
----------------------------

Utilisation des fonctionnalités d'analyse:

.. code-block:: python

   from simulateur_trafic.core.simulateur import Simulateur
   from simulateur_trafic.core.analyseur import Analyseur
   
   simulateur = Simulateur("data/config_reseau.json")
   simulateur.lancer_simulation(n_tours=100, delta_t=60)
   
   # Analyse détaillée
   analyseur = simulateur.analyseur
   
   # Statistiques globales
   stats_globales = analyseur.calculer_statistiques_globales()
   print(f"Vitesse moyenne: {stats_globales['vitesse_moyenne_globale']:.1f} km/h")
   
   # Zones de congestion
   zones_congestion = analyseur.identifier_zones_congestion(seuil=70)
   for zone in zones_congestion:
       print(f"Route {zone['route']}: {zone['taux_congestion']:.1f}% de congestion")
   
   # Rapport de performance complet
   rapport = analyseur.generer_rapport_performance()
   print(f"Note de performance: {rapport['performance_generale']['note']}")

Exemple avec Export des Données
-------------------------------

Export complet des résultats:

.. code-block:: python

   from simulateur_trafic.core.simulateur import Simulateur
   from simulateur_trafic.io_utils.export import Export
   
   simulateur = Simulateur("data/config_reseau.json")
   simulateur.lancer_simulation(n_tours=80, delta_t=45)
   
   # Export dans différents formats
   export = Export(repertoire_sortie="resultats")
   
   # Export CSV pour analyse
   export.exporter_csv(simulateur.historique_stats, "mes_statistiques.csv")
   
   # Export JSON pour traitement
   export.exporter_json(simulateur.historique_stats, "donnees_brutes.json")
   
   # Rapport Excel complet
   export.exporter_excel(simulateur.historique_stats, "rapport.xlsx")
   
   # Rapport détaillé
   export.generer_rapport_complet(simulateur, "rapport_complet.json")

Exemple avec Visualisation
--------------------------

Génération de graphiques avancés:

.. code-block:: python

   from simulateur_trafic.core.simulateur import Simulateur
   from simulateur_trafic.io_utils.affichage import Affichage
   
   simulateur = Simulateur("data/config_reseau.json")
   simulateur.lancer_simulation(n_tours=120, delta_t=30)
   
   affichage = Affichage()
   
   # Graphique d'évolution
   affichage.generer_graphique_evolution(
       simulateur.historique_stats,
       "evolution_trafic.png"
   )
   
   # Carte du réseau
   affichage.generer_carte_flux(
       simulateur.reseau,
       "carte_reseau.png" 
   )
   
   # Comparaison des routes
   stats_routes = simulateur.analyseur._calculer_statistiques_routes()
   affichage.generer_graphique_comparaison_routes(
       stats_routes,
       "comparaison_routes.png"
   )

Scripts d'Exemple
-----------------

Le projet inclut des scripts d'exemple dans le dossier `examples/`:

.. code-block:: bash

   # Exemple de simulation urbaine
   python examples/simulation_urbaine.py
   
   # Exemple d'analyse de congestion  
   python examples/analyse_congestion.py
   
   # Exemple de génération de rapports
   python examples/generation_rapports.py