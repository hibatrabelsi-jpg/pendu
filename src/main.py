"""
Pendu - Édition Deluxe
Point d'entrée principal du jeu.
"""
import sys
import pygame

from config.settings import WIDTH, HEIGHT, FPS
from ui.renderer import draw_gradient_bg
from ui.screens import (
    MenuScreen, NameInputScreen, DifficultyScreen,
    GameScreen, ScoresScreen, AddWordScreen
)


def main():
    """Fonction principale du jeu."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pendu - Édition Deluxe")
    clock = pygame.time.Clock()

    # Polices
    fonts = {
        'title': pygame.font.SysFont("arial", 52, bold=True),
        'subtitle': pygame.font.SysFont("arial", 24),
        'ui': pygame.font.SysFont("arial", 20),
        'word': pygame.font.SysFont("arial", 36, bold=True),
        'key': pygame.font.SysFont("arial", 18, bold=True),
        'big': pygame.font.SysFont("arial", 38, bold=True),
        'score': pygame.font.SysFont("arial", 22),
    }

    # Pré-rendu du fond avec dégradé
    bg_surface = pygame.Surface((WIDTH, HEIGHT))
    draw_gradient_bg(bg_surface)

    # État partagé du jeu
    game_state = {
        'player_name': '',
        'difficulty': 'facile',
    }

    # Création des écrans
    screens = {
        'MENU': MenuScreen(game_state),
        'NAME_INPUT': NameInputScreen(game_state),
        'DIFFICULTY': DifficultyScreen(game_state),
        'GAME': GameScreen(game_state),
        'SCORES': ScoresScreen(game_state),
        'ADD_WORD': AddWordScreen(game_state),
    }

    current_screen = 'MENU'

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                next_screen = screens[current_screen].handle_event(event)
                if next_screen:
                    if next_screen == 'QUIT':
                        running = False
                    else:
                        # Actions spéciales lors du changement d'écran
                        if next_screen == 'NAME_INPUT':
                            screens['NAME_INPUT'].reset()
                        elif next_screen == 'ADD_WORD':
                            screens['ADD_WORD'].reset()
                        elif next_screen == 'GAME':
                            screens['GAME'].start_new_game()

                        current_screen = next_screen

        # Mise à jour
        screens[current_screen].update(dt, mouse_pos)

        # Rendu
        screen.blit(bg_surface, (0, 0))
        screens[current_screen].draw(screen, fonts)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
