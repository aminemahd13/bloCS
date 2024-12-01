# Jeu 2048-Terraria

Ce projet est une implémentation en Python d'un jeu hybride combinant les éléments de Terraria et du jeu populaire 2048, avec une conception modulaire et des commandes faciles à utiliser pour l'installation et l'exécution.

## Description

Le jeu 2048-Terraria est un jeu de puzzle et d'aventure où le joueur doit miner des blocs dans un monde de type Terraria pour obtenir des tuiles numérotées. L'objectif est de faire glisser ces tuiles sur une grille pour les combiner et créer une tuile avec le numéro 2048. Cette implémentation inclut des fonctionnalités supplémentaires et des améliorations pour offrir une expérience plus engageante.

## Produit Minimum Viable (MVP)

- Organisation: Brainstorming dans un premier temps et plannification
- Premier prototype de la map, et des skins
- Ajout du code pour afficher la map et tout visualiser 
- Collision / gravité
- Structure modulaire pour un développement et des tests plus faciles

## Interface Graphique MVC

Le projet suit le modèle de conception Modèle-Vue-Contrôleur (MVC) :

- **Modèle** : Gère l'état et la logique du jeu, y compris la grille, les valeurs des tuiles et les blocs minés.
- **Vue** : Gère la représentation graphique du jeu, y compris le rendu de la grille, des tuiles et du monde de minage.
- **Contrôleur** : Gère les entrées utilisateur et met à jour le modèle et la vue en conséquence.

## Cas d'Usage

1. **Démarrer le Jeu** : L'utilisateur lance le jeu et est présenté avec le menu principal.
2. **Miner des Blocs** : L'utilisateur mine des blocs dans un monde de type Terraria pour obtenir des tuiles numérotées.
3. **Jouer au Jeu 2048** : L'utilisateur utilise les touches ZQSD pour déplacer les tuiles sur la grille. Les tuiles avec le même numéro fusionnent lorsqu'elles se touchent.
4. **Gagner le Jeu** : L'utilisateur gagne en créant une tuile avec le numéro 2048
5. **Perdre le Jeu** : Le jeu se termine lorsqu'il n'y a plus de mouvements possibles, ou lorsqu'il tombe
6. **Voir les Conseils** : L'utilisateur peut voir des conseils sur la façon de jouer au jeu depuis le menu principal.
7. **Quitter le Jeu** : L'utilisateur peut quitter le jeu à tout moment.

## Feuille de Route

### Phase 1 : Développement Initial
- [x] Implémenter les mécanismes de base du jeu 2048
- [x] Implémenter les mécanismes de minage de blocs inspirés de Terraria
- [x] Configurer la structure du projet et les dépendances
- [x] Créer le menu principal et l'écran de jeu

### Phase 2 : Améliorations
- [x] Ajouter la génération aléatoire de tuiles et la logique de score
- [x] Implémenter des contrôles intuitifs pour les mouvements basés sur la grille
- [x] Développer une structure modulaire pour un développement et des tests plus faciles

### Phase 3 : Fonctionnalités Supplémentaires
- [ ] Implémenter des modes de jeu avancés
- [ ] Ajouter des effets sonores et de la musique de fond
- [ ] Améliorer l'interface graphique avec des animations

## Fonctionnalités Complétées

- Mécanismes de base du jeu 2048
- Mécanismes de minage de blocs inspirés de Terraria
- Génération aléatoire de tuiles avec logique de score
- Contrôles intuitifs pour les mouvements basés sur la grille
- Structure modulaire pour un développement et des tests plus faciles
- Menu principal et écran de jeu

## Fonctionnalités Partiellement Complétées

- Modes de jeu avancés
- Effets sonores et musique de fond
- Interface graphique améliorée avec des animations

## Exigences

Assurez-vous que Python est installé sur votre système, puis configurez les dépendances requises.
Veuillez à bien télécharger tous les modules comme pygame 

