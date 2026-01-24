"""Écran d'ajout de mot."""
import pygame
from .base import BaseScreen
from ui.components import Button, TextInput
from core import charger_mots, ajouter_mot
from config.theme import (
    COL_ACCENT, COL_ACCENT_LIGHT, COL_TEXT_DIM, COL_DANGER,
    COL_KEY_DEFAULT, COL_KEY_HOVER, COL_KEY_CORRECT
)
from config.settings import WIDTH, WORDS_FILE


class AddWordScreen(BaseScreen):
    """Écran d'ajout de mot."""

    def __init__(self, game_state: dict):
        super().__init__(game_state)

        self.word_input = TextInput(WIDTH // 2 - 150, 320, 300, 50, "Nouveau mot...")
        self.btn_retour = Button(20, 20, 120, 40, "← Retour", COL_KEY_DEFAULT, COL_KEY_HOVER)
        self.btn_valider = Button(WIDTH // 2 - 75, 400, 150, 45, "Valider",
                                  COL_KEY_CORRECT, COL_ACCENT_LIGHT)

        # État
        self.message = ""
        self.message_timer = 0.0
        self.message_success = False

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if self.btn_retour.is_clicked(event):
            return "MENU"

        if self.word_input.handle_event(event) or self.btn_valider.is_clicked(event):
            if self.word_input.text.strip():
                success, msg = ajouter_mot(WORDS_FILE, self.word_input.text)
                self.message = msg
                self.message_success = success
                self.message_timer = 3.0
                if success:
                    self.word_input.text = ""

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "MENU"

        return None

    def update(self, dt: float, mouse_pos: tuple):
        self.btn_retour.update(mouse_pos)
        self.btn_valider.update(mouse_pos)
        self.word_input.update(dt)
        if self.message_timer > 0:
            self.message_timer -= dt

    def draw(self, surface: pygame.Surface, fonts: dict):
        self.btn_retour.draw(surface, fonts['ui'])

        # Titre
        title = fonts['big'].render("Ajouter un mot", True, COL_ACCENT)
        surface.blit(title, title.get_rect(center=(WIDTH // 2, 180)))

        # Instruction
        instruction = fonts['ui'].render("Entrez un mot (lettres uniquement, sans accent)",
                                         True, COL_TEXT_DIM)
        surface.blit(instruction, instruction.get_rect(center=(WIDTH // 2, 240)))

        # Champ de saisie et bouton
        self.word_input.draw(surface, fonts['ui'])
        self.btn_valider.draw(surface, fonts['ui'])

        # Message
        if self.message_timer > 0:
            msg_color = COL_ACCENT if self.message_success else COL_DANGER
            msg_surf = fonts['ui'].render(self.message, True, msg_color)
            surface.blit(msg_surf, msg_surf.get_rect(center=(WIDTH // 2, 480)))

        # Nombre de mots
        try:
            mots = charger_mots(WORDS_FILE)
            count_text = fonts['ui'].render(f"Mots dans la liste : {len(mots)}",
                                           True, COL_TEXT_DIM)
            surface.blit(count_text, count_text.get_rect(center=(WIDTH // 2, 550)))
        except:
            pass

    def reset(self):
        """Réinitialise le champ de saisie."""
        self.word_input.text = ""
        self.message = ""
