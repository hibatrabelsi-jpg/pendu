# Pendu - Édition Deluxe

Un jeu de pendu avec interface graphique Pygame.

## Fonctionnalités

- Devinez le mot lettre par lettre avant que le pendu ne soit complété
- 3 niveaux de difficulté (facile, moyen, difficile)
- Clavier virtuel cliquable + clavier physique
- Système de scores avec classement
- Possibilité d'ajouter vos propres mots

## Installation

### Prérequis

- Python 3.10 ou supérieur
- Pygame

### Installer Pygame

```bash
pip install pygame
```

## Lancer le jeu

```bash
cd src
python3 main.py
```

## Comment jouer

1. **Menu principal** : Choisissez "Jouer", "Tableau des scores" ou "Ajouter un mot"
2. **Entrez votre nom** pour enregistrer votre score
3. **Choisissez une difficulté** :
   - Facile : mots de 4-6 lettres (score ×1)
   - Moyen : mots de 7-9 lettres (score ×2)
   - Difficile : mots de 10+ lettres (score ×3)
4. **Devinez le mot** en cliquant sur les lettres ou en tapant au clavier
5. Vous avez droit à **7 erreurs** maximum

## Calcul du score

```
Score = Vies restantes × Coefficient de difficulté
```

## Structure du projet

```
pendu/
├── data/
│   ├── liste_mots.txt      # Liste des mots (1 mot par ligne)
│   └── scores.txt          # Historique des scores
├── src/
│   ├── main.py             # Point d'entrée
│   ├── config/             # Configuration (dimensions, couleurs)
│   ├── core/               # Logique métier (jeu, scores)
│   ├── ui/                 # Interface graphique
│   │   ├── components/     # Boutons, clavier, champs de saisie
│   │   ├── screens/        # Écrans (menu, jeu, scores...)
│   │   └── renderer.py     # Fonctions de dessin
│   └── utils/              # Utilitaires (animations)
└── README.md
```

## Contrôles

| Action | Contrôle |
|--------|----------|
| Choisir une lettre | Clic sur le clavier virtuel ou touche clavier |
| Retour au menu | Bouton "← Retour" ou touche Échap |
| Rejouer | Bouton "Rejouer" ou touche Entrée |
| Quitter | Bouton "Quitter" ou touche Échap (depuis le menu) |

## Auteurs

Projet réalisé dans le cadre d'un exercice de programmation Python avec Pygame.
