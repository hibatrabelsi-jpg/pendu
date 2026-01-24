"""Écran de choix de la difficulté."""
import pygame
from .base import BaseScreen
from ui.components import Button
from config.theme import (
    COL_ACCENT, COL_ACCENT_LIGHT, COL_GOLD, COL_TEXT_DIM,
    COL_KEY_DEFAULT, COL_KEY_HOVER, COL_KEY_CORRECT, COL_DANGER, COL_DANGER_LIGHT
)
from config.settings import WIDTH


class DifficultyScreen(BaseScreen):
    """Écran de choix de la difficulté."""

    def __init__(self, game_state: dict):
        super().__init__(game_state)

        self.btn_retour = Button(20, 20, 120, 40, "← Retour", COL_KEY_DEFAULT, COL_KEY_HOVER)
        self.btn_facile = Button(WIDTH // 2 - 150, 300, 300, 55, "Facile",
                                 COL_KEY_CORRECT, COL_ACCENT_LIGHT)
        self.btn_moyen = Button(WIDTH // 2 - 150, 370, 300, 55, "Moyen",
                                COL_GOLD, (255, 220, 130))
        self.btn_difficile = Button(WIDTH // 2 - 150, 440, 300, 55, "Difficile",
                                    COL_DANGER, COL_DANGER_LIGHT)

        self.difficulty_buttons = [self.btn_facile, self.btn_moyen, self.btn_difficile]

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if self.btn_retour.is_clicked(event):
            return "NAME_INPUT"
        elif self.btn_facile.is_clicked(event):
            self.game_state['difficulty'] = "facile"
            return "GAME"
        elif self.btn_moyen.is_clicked(event):
            self.game_state['difficulty'] = "moyen"
            return "GAME"
        elif self.btn_difficile.is_clicked(event):
            self.game_state['difficulty'] = "difficile"
            return "GAME"

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "NAME_INPUT"

        return None

    def update(self, dt: float, mouse_pos: tuple):
        self.btn_retour.update(mouse_pos)
        for btn in self.difficulty_buttons:
            btn.update(mouse_pos)

    def draw(self, surface: pygame.Surface, fonts: dict):
        self.btn_retour.draw(surface, fonts['ui'])

        # Titre de bienvenue
        player_name = self.game_state.get('player_name', 'Joueur')
        title = fonts['big'].render(f"Bienvenue {player_name} !", True, COL_ACCENT)
        surface.blit(title, title.get_rect(center=(WIDTH // 2, 180)))

        # Sous-titre
        subtitle = fonts['ui'].render("Choisissez une difficulté", True, COL_TEXT_DIM)
        surface.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 240)))

        # Boutons de difficulté
        for btn in self.difficulty_buttons:
            btn.draw(surface, fonts['ui'])

        # Info sur les difficultés
        info_y = 520
        info1 = fonts['ui'].render("Facile: 4-6 lettres (×1)", True, COL_KEY_CORRECT)
        info2 = fonts['ui'].render("Moyen: 7-9 lettres (×2)", True, COL_GOLD)
        info3 = fonts['ui'].render("Difficile: 10+ lettres (×3)", True, COL_DANGER)
        surface.blit(info1, info1.get_rect(center=(WIDTH // 2, info_y)))
        surface.blit(info2, info2.get_rect(center=(WIDTH // 2, info_y + 25)))
        surface.blit(info3, info3.get_rect(center=(WIDTH // 2, info_y + 50)))
