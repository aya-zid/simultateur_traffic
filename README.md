# 🚦 Simulateur de Trafic Routier Intelligent

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![PyPI](https://img.shields.io/pypi/v/simulateur-trafic-aya-zid.svg
Un simulateur de trafic routier complet écrit en Python, permettant de modéliser, simuler et analyser un réseau routier composé de routes, intersections, feux de circulation (*FeuRouge*) et véhicules.

---

## 🧠 Objectifs du projet

- Concevoir une application orientée objet structurée et extensible  
- Simuler la circulation de véhicules dans un réseau complexe  
- Intégrer un système de feux intelligents (*FeuRouge*)  
- Fournir des statistiques dynamiques (vitesse, congestion, temps de trajet)  
- Permettre des visualisations et exports de données  
- Assurer une architecture modulaire et testable  

---

## 🚀 Installation

### Depuis PyPI
```bash
pip install simulateur-trafic-aya-zid
```

### Depuis GitHub
```bash
git clone https://github.com/aya-zid/simulateur-trafic.git
cd simulateur-trafic
poetry install
```

---

## 🚀 Exécution

### 1️⃣ Simulation complète
```bash
python main.py -t 60 -d 60 -c data/config_reseau.json --graphique --export --affichage
```

**Arguments :**
- `-t` : nombre de tours (ex: 60 minutes)  
- `-d` : durée d’un pas de simulation (en secondes)  
- `-c` : fichier de configuration du réseau  
- `--graphique` : active les visualisations  
- `--export` : exporte les résultats  
- `--affichage` : affiche la progression en temps réel  

### 2️⃣ Démonstration rapide
```bash
python main.py
```

---

## 🧮 Exemple de configuration (data/config_reseau.json)

Ce fichier définit :  
- Les routes (longueur, vitesse limite)  
- Les intersections  
- Les feux tricolores (*FeuRouge*)  
- Les véhicules (position, vitesse, route initiale)

---

## 📊 Fonctionnalités principales

| Module        | Rôle |
|---------------|------|
| **Vehicule**        | Modélisation d’un véhicule (position, vitesse, comportement) |
| **Route**           | Gestion des véhicules, calculs de trafic |
| **FeuRouge**        | Cycles rouge/vert/orange configurables |
| **ReseauRoutier**   | Coordination routes + intersections |
| **Simulateur**      | Boucle principale de simulation |
| **Analyseur**       | Statistiques : vitesses, congestions, temps de trajet |
| **Affichage**       | Graphiques et rendu visuel |
| **Export**          | Sauvegarde des résultats |

---

## 🧪 Tests

Le projet inclut des tests unitaires et d’intégration.

### Exécuter tous les tests
```bash
pytest -v
```

---

## 📈 Résultats attendus

- Évolution des vitesses et densités au fil du temps  
- Identification automatique des congestions  
- Statistiques globales du réseau  
- Visualisation graphique complète (matplotlib)  

---

## 📦 PyPI

Package disponible ici :  
https://pypi.org/project/simulateur-trafic-aya-zid/

---

## 📜 Licence

Projet distribué sous licence **MIT**.  
© 2025 Aya Zid — Simulateur de Trafic Routier Intelligent.
