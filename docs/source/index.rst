.. Simulateur de Trafic Routier Intelligent documentation master file

Simulateur de Trafic Routier Intelligent
=========================================

.. toctree::
   :maxdepth: 2
   :caption: Contenu:

   introduction
   usage
   api/index
   examples

Introduction
------------

Le **Simulateur de Trafic Routier Intelligent** est une application Python 
pour modéliser et simuler un réseau routier avec véhicules, routes et intersections.

Fonctionnalités Principales
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* 🚗 Simulation de véhicules intelligents
* 🛣️ Modélisation de réseaux routiers complexes  
* 📊 Analyse en temps réel du trafic
* 📈 Visualisations graphiques avancées
* 💾 Export des données multiples formats
* 🧪 Architecture modulaire et testable

Architecture du Projet
~~~~~~~~~~~~~~~~~~~~~~

.. mermaid::

   graph TB
       A[main.py] --> B[models]
       A --> C[core] 
       A --> D[io_utils]
       
       B --> B1[vehicule.py]
       B --> B2[route.py]
       B --> B3[reseau.py]
       
       C --> C1[simulateur.py]
       C --> C2[analyseur.py]
       
       D --> D1[affichage.py]
       D --> D2[export.py]

Installation Rapide
-------------------

.. code-block:: bash

   git clone <votre-repo>
   cd simulateur_trafic
   pip install -r requirements.txt
   python main.py --help

Exemple d'Utilisation
---------------------

.. code-block:: python

   from simulateur_trafic.core.simulateur import Simulateur
   
   # Créer et lancer une simulation
   simulateur = Simulateur("data/config_reseau.json")
   simulateur.lancer_simulation(n_tours=60, delta_t=60)

Indices et Tables
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`