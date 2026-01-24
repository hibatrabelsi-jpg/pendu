"""Composant bouton interactif."""
import pygame
from config.theme import COL_TEXT
from utils.animation import AnimatedValue


class Button:
    """Bouton interactif avec hover et animations."""

    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 color: tuple, hover_color: tuple, text_color: tuple = COL_TEXT):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.scale = AnimatedValue(1.0, 0.2)

    def update(self, mouse_pos: tuple):
        """Met à jour l'état du bouton selon la position de la souris."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.scale.set_target(1.05 if self.is_hovered else 1.0)
        self.scale.update()

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        """Dessine le bouton sur la surface."""
        scale = self.scale.get()
        w = int(self.rect.width * scale)
        h = int(self.rect.height * scale)

        color = self.hover_color if self.is_hovered else self.color

        btn_rect = pygame.Rect(
            self.rect.centerx - w // 2,
            self.rect.centery - h // 2,
            w, h
        )
        pygame.draw.rect(surface, color, btn_rect, border_radius=12)

        border_color = tuple(min(c + 30, 255) for c in color)
        pygame.draw.rect(surface, border_color, btn_rect, width=2, border_radius=12)

        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=btn_rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        """Retourne True si le bouton a été cliqué."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False
