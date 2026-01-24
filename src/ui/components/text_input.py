"""Composant champ de saisie de texte."""
import pygame
from config.theme import COL_INPUT_BG, COL_INPUT_BORDER, COL_TEXT, COL_TEXT_DIM


class TextInput:
    """Champ de saisie de texte."""

    def __init__(self, x: int, y: int, width: int, height: int,
                 placeholder: str = "", max_length: int = 20):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.placeholder = placeholder
        self.max_length = max_length
        self.active = True
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Gère les événements clavier.
        Retourne True si Enter est pressé.
        """
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < self.max_length and event.unicode.isprintable():
                    self.text += event.unicode
        return False

    def update(self, dt: float):
        """Met à jour le clignotement du curseur."""
        self.cursor_timer += dt
        if self.cursor_timer >= 0.5:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        """Dessine le champ de saisie."""
        # Fond
        pygame.draw.rect(surface, COL_INPUT_BG, self.rect, border_radius=10)
        # Bordure
        border_color = COL_INPUT_BORDER if self.active else COL_TEXT_DIM
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=10)

        # Texte ou placeholder
        if self.text:
            text_surf = font.render(self.text, True, COL_TEXT)
        else:
            text_surf = font.render(self.placeholder, True, COL_TEXT_DIM)

        text_rect = text_surf.get_rect(midleft=(self.rect.x + 15, self.rect.centery))
        surface.blit(text_surf, text_rect)

        # Curseur
        if self.active and self.cursor_visible:
            if self.text:
                cursor_x = text_rect.right + 2
            else:
                cursor_x = self.rect.x + 15
            pygame.draw.line(surface, COL_TEXT,
                           (cursor_x, self.rect.y + 10),
                           (cursor_x, self.rect.bottom - 10), 2)
