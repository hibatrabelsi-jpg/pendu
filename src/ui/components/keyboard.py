"""Composants clavier virtuel."""
import pygame
from config.theme import (
    COL_KEY_DEFAULT, COL_KEY_HOVER, COL_KEY_CORRECT,
    COL_KEY_WRONG, COL_KEY_TEXT
)
from utils.animation import AnimatedValue


class KeyboardKey:
    """Touche du clavier virtuel."""

    def __init__(self, x: int, y: int, size: int, letter: str):
        self.rect = pygame.Rect(x, y, size, size)
        self.letter = letter
        self.state = "default"  # default, correct, wrong
        self.is_hovered = False
        self.scale = AnimatedValue(1.0, 0.25)
        self.pop_animation = 0.0

    def update(self, mouse_pos: tuple):
        """Met à jour l'état de la touche."""
        if self.state == "default":
            self.is_hovered = self.rect.collidepoint(mouse_pos)
            self.scale.set_target(1.1 if self.is_hovered else 1.0)
        else:
            self.is_hovered = False
            self.scale.set_target(1.0)
        self.scale.update()

        if self.pop_animation > 0:
            self.pop_animation -= 0.1

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        """Dessine la touche."""
        scale = self.scale.get() + self.pop_animation * 0.2
        size = int(self.rect.width * scale)

        if self.state == "correct":
            color = COL_KEY_CORRECT
        elif self.state == "wrong":
            color = COL_KEY_WRONG
        else:
            color = COL_KEY_HOVER if self.is_hovered else COL_KEY_DEFAULT

        key_rect = pygame.Rect(
            self.rect.centerx - size // 2,
            self.rect.centery - size // 2,
            size, size
        )
        pygame.draw.rect(surface, color, key_rect, border_radius=8)

        if self.state == "default":
            highlight = pygame.Rect(key_rect.x + 3, key_rect.y + 3, key_rect.width - 6, 4)
            highlight_color = tuple(min(c + 25, 255) for c in color)
            pygame.draw.rect(surface, highlight_color, highlight, border_radius=2)

        alpha = 150 if self.state != "default" else 255
        text_surf = font.render(self.letter.upper(), True, COL_KEY_TEXT)
        text_surf.set_alpha(alpha)
        text_rect = text_surf.get_rect(center=key_rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        """Retourne True si la touche a été cliquée."""
        if self.state != "default":
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

    def trigger(self):
        """Déclenche l'animation pop."""
        self.pop_animation = 1.0


class VirtualKeyboard:
    """Clavier virtuel complet A-Z en disposition AZERTY."""

    def __init__(self, x: int, y: int, key_size: int = 42, spacing: int = 6):
        self.keys: dict[str, KeyboardKey] = {}
        self.x = x
        self.y = y

        # Disposition AZERTY
        rows = [
            "AZERTYUIOP",
            "QSDFGHJKLM",
            "WXCVBN"
        ]

        for row_idx, row in enumerate(rows):
            row_offset = row_idx * 20
            for col_idx, letter in enumerate(row):
                kx = x + row_offset + col_idx * (key_size + spacing)
                ky = y + row_idx * (key_size + spacing)
                self.keys[letter.lower()] = KeyboardKey(kx, ky, key_size, letter)

    def update(self, mouse_pos: tuple):
        """Met à jour toutes les touches."""
        for key in self.keys.values():
            key.update(mouse_pos)

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        """Dessine toutes les touches."""
        for key in self.keys.values():
            key.draw(surface, font)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Retourne la lettre cliquée ou None."""
        for letter, key in self.keys.items():
            if key.is_clicked(event):
                key.trigger()
                return letter
        return None

    def set_key_state(self, letter: str, state: str):
        """Change l'état d'une touche (correct/wrong)."""
        if letter in self.keys:
            self.keys[letter].state = state
            self.keys[letter].trigger()

    def reset(self):
        """Réinitialise toutes les touches à l'état par défaut."""
        for key in self.keys.values():
            key.state = "default"
