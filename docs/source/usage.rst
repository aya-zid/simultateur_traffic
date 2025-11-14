Utilisation
===========

Ligne de Commande
-----------------

Le simulateur peut être lancé directement avec des paramètres:

.. code-block:: bash

   python main.py --tours 100 --deltat 30 --export-all --real-time-display

Options Disponibles
~~~~~~~~~~~~~~~~~~~

.. program-output:: python ../main.py --help
   :shell:

Exemples d'Utilisation
~~~~~~~~~~~~~~~~~~~~~~

**Simulation rapide avec visualisation**:

.. code-block:: bash

   python main.py -t 50 -d 60 --real-time-display

**Simulation longue avec export complet**:

.. code-block:: bash

   python main.py -t 200 -d 30 --export-all --export-dir "mes_resultats"

**Mode silencieux pour traitement par lots**:

.. code-block:: bash

   python main.py -t 100 --no-progress --no-graph

Utilisation en tant que Module
------------------------------

Le simulateur peut aussi être importé comme module Python:

.. code-block:: python

   from simulateur_trafic import Simulateur, Analyseur, Affichage
   
   # Initialisation
   simulateur = Simulateur("config/reseau.json")
   
   # Simulation
   simulateur.lancer_simulation(n_tours=60, delta_t=60)
   
   # Analyse
   rapport = simulateur.analyseur.generer_rapport_performance()
   
   # Visualisation
   affichage = Affichage()
   affichage.afficher_rapport_performance(rapport)

Configuration du Réseau
-----------------------

Le fichier de configuration JSON définit le réseau routier:

.. code-block:: json

   {
     "routes": [
       {
         "nom": "Autoroute_A1",
         "longueur": 10000,
         "limite_vitesse": 130
       }
     ],
     "intersections": [
       {
         "source": "Autoroute_A1", 
         "destinations": ["Route_B1", "Route_C2"]
       }
     ],
     "vehicules": [
       {
         "id": 1,
         "route": "Autoroute_A1",
         "position": 0,
         "vitesse": 110
       }
     ]
   }

Format des Sorties
------------------

Le simulateur génère plusieurs types de sorties:

.. list-table:: Formats de Sortie
   :header-rows: 1

   * - Format
     - Fichier
     - Usage
   * - CSV
     - statistiques_simulation.csv
     - Analyse avec Excel/R
   * - JSON
     - donnees_simulation.json
     - Traitement programmatique
   * - Excel
     - rapport_simulation.xlsx
     - Rapport professionnel
   * - PNG
     - evolution_statistiques.png
     - Présentations

Visualisations
--------------

Le simulateur génère plusieurs types de graphiques:

* **Évolution temporelle** : Statistiques sur la durée de simulation
* **Carte du réseau** : Représentation visuelle du réseau routier
* **Comparaison routes** : Performance comparative des différentes routes

Exemple Complet
---------------

.. code-block:: python

   # Exemple complet d'utilisation
   from simulateur_trafic.core.simulateur import Simulateur
   from simulateur_trafic.io_utils.affichage import Affichage
   from simulateur_trafic.io_utils.export import Export
   
   def simulation_complete():
       # Initialisation
       simulateur = Simulateur("data/config_reseau.json")
       affichage = Affichage()
       export = Export()
       
       # Simulation
       simulateur.lancer_simulation(n_tours=100, delta_t=30)
       
       # Résultats
       rapport = simulateur.analyseur.generer_rapport_performance()
       affichage.afficher_rapport_performance(rapport)
       
       # Export
       export.exporter_csv(simulateur.historique_stats)
       affichage.generer_graphique_evolution(simulateur.historique_stats)
       
       return simulateur