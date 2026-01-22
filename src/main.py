# ========================================
# Fichier principal - Lance le jeu
# ========================================
import pygame
from menu import menu_principal
from game_pygame import jouer_pygame
from file_handler import charger_scores

def main():
    while True:
        pygame.quit()  # Fermer proprement
        pygame.init()  # Réinitialiser
        
        choix = menu_principal()
        
        if choix == "jouer":
            jouer_pygame()
        elif choix == "scores":
            afficher_scores()

# Lancer le jeu
if __name__ == "__main__":
    main()