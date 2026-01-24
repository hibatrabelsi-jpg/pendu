"""Écran du menu principal."""
import pygame
from .base import BaseScreen
from ui.components import Button
from ui.renderer import draw_hangman
from config.theme import (
    COL_ACCENT, COL_ACCENT_LIGHT, COL_GOLD, COL_TEXT_DIM,
    COL_KEY_DEFAULT, COL_KEY_HOVER, COL_KEY_CORRECT
)
from config.settings import WIDTH


class MenuScreen(BaseScreen):
    """Écran du menu principal."""

    def __init__(self, game_state: dict):
        super().__init__(game_state)

        # Boutons du menu
        self.btn_jouer = Button(WIDTH // 2 - 150, 250, 300, 55, "Jouer",
                                COL_KEY_CORRECT, COL_ACCENT_LIGHT)
        self.btn_scores = Button(WIDTH // 2 - 150, 320, 300, 55, "Tableau des scores",
                                 COL_GOLD, (255, 220, 130))
        self.btn_ajouter = Button(WIDTH // 2 - 150, 390, 300, 55, "Ajouter un mot",
                                  (100, 100, 140), (130, 130, 170))
        self.btn_quitter = Button(WIDTH // 2 - 100, 480, 200, 45, "Quitter",
                                  COL_KEY_DEFAULT, COL_KEY_HOVER)

        self.buttons = [self.btn_jouer, self.btn_scores, self.btn_ajouter, self.btn_quitter]

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if self.btn_jouer.is_clicked(event):
            return "NAME_INPUT"
        elif self.btn_scores.is_clicked(event):
            return "SCORES"
        elif self.btn_ajouter.is_clicked(event):
            return "ADD_WORD"
        elif self.btn_quitter.is_clicked(event):
            return "QUIT"

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "QUIT"

        return None

    def update(self, dt: float, mouse_pos: tuple):
        for btn in self.buttons:
            btn.update(mouse_pos)

    def draw(self, surface: pygame.Surface, fonts: dict):
        # Titre
        title = fonts['title'].render("PENDU", True, COL_ACCENT)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        surface.blit(title, title_rect)

        # Sous-titre
        subtitle = fonts['subtitle'].render("Édition Deluxe", True, COL_TEXT_DIM)
        sub_rect = subtitle.get_rect(center=(WIDTH // 2, 155))
        surface.blit(subtitle, sub_rect)

        # Boutons
        for btn in self.buttons:
            btn.draw(surface, fonts['ui'])

        # Pendu décoratif
        draw_hangman(surface, 3, 150, 380)
