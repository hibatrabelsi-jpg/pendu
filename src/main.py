# ========================================
# Fichier principal - Lance le jeu
# ========================================
import pygame
from menu import menu_principal
from game_pygame import jouer_pygame
from scores import afficher_scores

def main():
    # Boucle pour revenir au menu après chaque action
    while True:
        choix = menu_principal()
        
        if choix == "jouer":
            jouer_pygame()
        elif choix == "scores":
            afficher_scores()

# Lancer le jeu
if __name__ == "__main__":
    main()