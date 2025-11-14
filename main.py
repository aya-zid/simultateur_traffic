#!/usr/bin/env python3
"""
Module principal - Point d'entrée de l'application de simulation de trafic
Ce module lance la simulation de trafic routier avec les paramètres spécifiés.
Il intègre l'affichage graphique et l'export des résultats.
"""
import sys
import os
import argparse
import json
# Ajouter le répertoire parent au chemin pour importer les modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.simulateur import Simulateur
from io_utils.affichage import Affichage
from io_utils.export import Export
def main():
    """
    Fonction principale qui lance la simulation de trafic avec visualisation.
    Cette fonction parse les arguments de ligne de commande,
    initialise le simulateur, les modules d'affichage et d'export,
    et lance la simulation complète.
    """
    parser = argparse.ArgumentParser(
        description="Simulateur de Trafic Routier Intelligent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py                                  # Simulation par défaut (60 tours de 60s)
  python main.py -t 120 -d 30                    # 120 tours de 30 secondes
  python main.py -c data/config_reseau.json      # Configuration personnalisée
  python main.py --no-progress --no-graph        # Sans progression ni graphiques
  python main.py --export-all                    # Export complet des résultats
  python main.py --real-time-display             # Affichage temps réel
        """
    )
    parser.add_argument(
        '-c', '--config',
        default='data/config_reseau.json',
        help='Fichier de configuration JSON (défaut: data/config_reseau.json)'
    )
    parser.add_argument(
        '-t', '--tours',
        type=int,
        default=60,
        help='Nombre de tours de simulation (défaut: 60)'
    )
    parser.add_argument(
        '-d', '--deltat',
        type=float,
        default=60.0,
        help='Durée de chaque tour en secondes (défaut: 60.0)'
    )
    parser.add_argument(
        '--no-progress',
        action='store_true',
        help='Désactiver l\'affichage de la progression'
    )
    parser.add_argument(
        '--no-graph',
        action='store_true',
        help='Désactiver les graphiques à la fin de la simulation'
    )
    parser.add_argument(
        '--export-all',
        action='store_true',
        help='Exporter toutes les données (CSV, JSON, Excel)'
    )
    parser.add_argument(
        '--real-time-display',
        action='store_true',
        help='Afficher le tableau de bord en temps réel'
    )
    parser.add_argument(
        '--export-dir',
        default='exports',
        help='Répertoire pour les exports (défaut: exports)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mode verbeux avec plus de détails'
    )
    args = parser.parse_args()
    # Afficher les paramètres de simulation
    print("="*70)
    print("🚦 SIMULATEUR DE TRAFIC ROUTIER INTELLIGENT")
    print("="*70)
    print(f"📁 Configuration: {args.config}")
    print(f"🔄 Tours de simulation: {args.tours}")
    print(f"⏱️  Durée par tour: {args.deltat} secondes")
    print(f"⏰ Durée totale: {args.tours * args.deltat} secondes")
    print(f"📊 Graphiques: {'Non' if args.no_graph else 'Oui'}")
    print(f"💾 Export données: {'Oui' if args.export_all else 'Non'}")
    print(f"📈 Affichage temps réel: {'Oui' if args.real_time_display else 'Non'}")
    print("="*70)
    try:
        # Vérifier si le fichier de configuration existe
        if not os.path.exists(args.config):
            print(f"⚠️  Fichier de configuration {args.config} non trouvé.")
            print("   Le simulateur démarrera avec un réseau vide.")
            # Créer une configuration par défaut si le fichier n'existe pas
            from data.config_reseau import creer_configuration_defaut, sauvegarder_configuration
            config = creer_configuration_defaut()
            sauvegarder_configuration(config, args.config)
            print(f"✅ Configuration par défaut créée: {args.config}")
        # Initialiser les composants
        simulateur = Simulateur(args.config)
        affichage = Affichage()
        export = Export(repertoire_sortie=args.export_dir)
        # Lancer la simulation avec les paramètres
        print("\n🚀 Démarrage de la simulation...")
        simulateur.lancer_simulation(
            n_tours=args.tours,
            delta_t=args.deltat,
            afficher_progression=not args.no_progress,
            affichage_temps_reel=affichage if args.real_time_display else None
        )
        # AFFICHAGE DES RÉSULTATS
        print("\n" + "="*70)
        print("📈 GÉNÉRATION DES RÉSULTATS")
        print("="*70)
        # 1. Afficher le rapport de performance
        rapport_performance = simulateur.analyseur.generer_rapport_performance()
        affichage.afficher_rapport_performance(rapport_performance)
        # 2. Générer les graphiques (sauf si désactivé)
        if not args.no_graph:
            print("\n🎨 Génération des graphiques...")
            # Graphique d'évolution temporelle
            affichage.generer_graphique_evolution(
                simulateur.historique_stats,
                os.path.join(args.export_dir, "evolution_statistiques.png")
            )
            # Carte du réseau avec flux
            affichage.generer_carte_flux(
                simulateur.reseau,
                os.path.join(args.export_dir, "carte_reseau.png")
            )
            # Find the last tour with vehicles for each route
            def get_last_nonzero_route_stats(historique_stats):
                for stats in reversed(historique_stats):
                    routes = stats.get('routes', {})
                    if any(r['nb_vehicules'] > 0 for r in routes.values()):
                        return routes
                return historique_stats[-1].get('routes', {}) if historique_stats else {}
            # Use this for the graph
            current_route_stats = get_last_nonzero_route_stats(simulateur.historique_stats)
            print("DEBUG: last_nonzero_route_stats =", current_route_stats)
            if current_route_stats and any(r['nb_vehicules'] > 0 for r in current_route_stats.values()):
                affichage.generer_graphique_comparaison_routes(
                    current_route_stats,
                    os.path.join(args.export_dir, "comparaison_routes.png")
                )
            else:
                print("⚠️  Aucune statistique de route disponible pour la comparaison")
        # 3. Exporter les données (si demandé)
        if args.export_all:
            print("\n💾 Export des données...")
            # Export CSV des statistiques
            export.exporter_csv(simulateur.historique_stats, "statistiques_simulation.csv")
            # Export JSON complet
            export.exporter_json(simulateur.historique_stats, "donnees_simulation.json")
            # Export Excel avec plusieurs onglets
            export.exporter_excel(simulateur.historique_stats, "rapport_simulation.xlsx")
            # Rapport complet
            export.generer_rapport_complet(simulateur, "rapport_complet.json")
            print(f"✅ Toutes les données exportées dans le dossier: {args.export_dir}")
        # 4. Afficher les statistiques finales si mode verbeux
        if args.verbose:
            print("\n" + "🔍 STATISTIQUES DÉTAILLÉES FINALES")
            print("-" * 50)
            if simulateur.historique_stats:
                dernier_tour = simulateur.historique_stats[-1]
                stats_globales = simulateur.analyseur.calculer_statistiques_globales()
                print(f"📊 Vitesse moyenne finale: {dernier_tour.get('vitesse_moyenne', 0):.1f} km/h")
                print(f"🚦 Densité moyenne finale: {dernier_tour.get('densite_moyenne', 0):.1f} véh/km")
                print(f"🚨 Taux de congestion final: {dernier_tour.get('taux_congestion', 0):.1f}%")
                print(f"🚗 Véhicules maximum: {stats_globales.get('max_vehicules', 0)}")
                print(f"⭐ Performance globale: {stats_globales.get('vitesse_moyenne_globale', 0):.1f} km/h")
                # Afficher les zones de congestion
                zones_congestion = simulateur.analyseur.identifier_zones_congestion(seuil=50)
                if zones_congestion:
                    print(f"\n🔴 Zones congestionnées (>50%):")
                    for zone in zones_congestion[:3]:
                        print(f"   • {zone['route']}: {zone['taux_congestion']:.1f}%")
        print("\n" + "="*70)
        print("✅ SIMULATION TERMINÉE AVEC SUCCÈS")
        print("="*70)
        return 0
    except FileNotFoundError as e:
        print(f"❌ Erreur: Fichier non trouvé - {e}")
        return 1
    except KeyboardInterrupt:
        print(f"\n⏹️  Simulation interrompue par l'utilisateur")
        return 130
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
def demo_rapide():
    """
    Fonction de démonstration rapide pour tester le système.
    Cette fonction peut être appelée pour une démonstration rapide
    sans arguments en ligne de commande.
    Example:
        >>> from main import demo_rapide
        >>> demo_rapide()
    """
    print("🎯 DÉMONSTRATION RAPIDE DU SIMULATEUR")
    print("Configuration: 30 tours de 30 secondes")
    try:
        simulateur = Simulateur("data/config_reseau.json")
        affichage = Affichage()
        # Simulation courte
        simulateur.lancer_simulation(n_tours=30, delta_t=30, afficher_progression=True)
        # Affichage rapide des résultats
        rapport = simulateur.analyseur.generer_rapport_performance()
        affichage.afficher_rapport_performance(rapport)
        # Graphique simple
        affichage.generer_graphique_evolution(simulateur.historique_stats)
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration: {e}")
        return False
if __name__ == "__main__":
    """
    Point d'entrée principal lorsqu'on exécute le script directement.
    
    Example:
        $ python main.py -t 100 -d 30 --export-all --real-time-display
        $ python main.py --no-graph --export-dir "mes_exports"
        $ python main.py --verbose --tours 50
    """
    # Si aucun argument n'est fourni, proposer une démonstration rapide
    if len(sys.argv) == 1:
        print("🤔 Aucun argument fourni. Voulez-vous lancer une démonstration rapide?")
        reponse = input("(O)ui ou (N)on? ").strip().lower()
        if reponse in ['o', 'oui', 'y', 'yes']:
            success = demo_rapide()
            sys.exit(0 if success else 1)
        else:
            print("Utilisez --help pour voir les options disponibles")
            sys.exit(0)
    exit_code = main()
    sys.exit(exit_code)