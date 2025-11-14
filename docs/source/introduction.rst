Introduction
============

Présentation
------------

Le simulateur de trafic routier intelligent est conçu pour modéliser et analyser 
le comportement du trafic dans un réseau routier virtuel.

Objectifs du Projet
-------------------

* **Modélisation** : Créer un réseau routier réaliste avec routes et intersections
* **Simulation** : Faire circuler des véhicules intelligents selon des règles de trafic
* **Analyse** : Calculer des métriques de performance (congestion, vitesse moyenne, etc.)
* **Visualisation** : Afficher les résultats sous forme graphique
* **Export** : Sauvegarder les données pour analyse ultérieure

Cas d'Utilisation
-----------------

.. list-table:: Cas d'Utilisation du Simulateur
   :header-rows: 1
   :widths: 30 70

   * - Utilisateur
     - Bénéfice
   * - Urbanistes
     - Planification de réseaux routiers
   * - Chercheurs
     - Étude des modèles de trafic
   * - Éducateurs
     - Enseignement des concepts de simulation
   * - Développeurs
     - Base pour applications de mobilité intelligente

Architecture Technique
----------------------

Le projet suit une architecture modulaire:

.. mermaid::

   flowchart LR
       subgraph Entrées
           A[Configuration JSON]
           B[Paramètres CLI]
       end
       
       subgraph Noyau
           C[Models<br/>Véhicule/Route/Réseau]
           D[Core<br/>Simulateur/Analyseur]
           E[IO Utils<br/>Affichage/Export]
       end
       
       subgraph Sorties
           F[Graphiques]
           G[Rapports]
           H[Fichiers]
       end
       
       Entrées --> Noyau --> Sorties