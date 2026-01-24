"""Écran de saisie du nom du joueur."""
import pygame
from .base import BaseScreen
from ui.components import Button, TextInput
from config.theme import COL_ACCENT, COL_ACCENT_LIGHT, COL_TEXT_DIM, COL_KEY_DEFAULT, COL_KEY_HOVER, COL_KEY_CORRECT
from config.settings import WIDTH


class NameInputScreen(BaseScreen):
    """Écran de saisie du nom du joueur."""

    def __init__(self, game_state: dict):
        super().__init__(game_state)

        self.name_input = TextInput(WIDTH // 2 - 150, 320, 300, 50, "Entrez votre nom...")
        self.btn_retour = Button(20, 20, 120, 40, "← Retour", COL_KEY_DEFAULT, COL_KEY_HOVER)
        self.btn_valider = Button(WIDTH // 2 - 75, 400, 150, 45, "Valider",
                                  COL_KEY_CORRECT, COL_ACCENT_LIGHT)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if self.btn_retour.is_clicked(event):
            return "MENU"

        if self.name_input.handle_event(event) or self.btn_valider.is_clicked(event):
            if self.name_input.text.strip():
                self.game_state['player_name'] = self.name_input.text.strip()
                return "DIFFICULTY"

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "MENU"

        return None

    def update(self, dt: float, mouse_pos: tuple):
        self.btn_retour.update(mouse_pos)
        self.btn_valider.update(mouse_pos)
        self.name_input.update(dt)

    def draw(self, surface: pygame.Surface, fonts: dict):
        self.btn_retour.draw(surface, fonts['ui'])

        # Titre
        title = fonts['big'].render("Entrez votre nom", True, COL_ACCENT)
        surface.blit(title, title.get_rect(center=(WIDTH // 2, 200)))

        # Instruction
        instruction = fonts['ui'].render("Appuyez sur Entrée pour valider", True, COL_TEXT_DIM)
        surface.blit(instruction, instruction.get_rect(center=(WIDTH // 2, 260)))

        # Champ de saisie et bouton
        self.name_input.draw(surface, fonts['ui'])
        self.btn_valider.draw(surface, fonts['ui'])

    def reset(self):
        """Réinitialise le champ de saisie."""
        self.name_input.text = ""
