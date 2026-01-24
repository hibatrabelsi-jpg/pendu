"""Fonctions de rendu graphique."""
import math
import pygame
from config.settings import WIDTH, HEIGHT
from config.theme import (
    COL_BG, COL_BG_GRADIENT, COL_PANEL, COL_PANEL_LIGHT,
    COL_TEXT, COL_TEXT_DIM, COL_ACCENT, COL_DANGER,
    COL_HANGMAN, COL_HANGMAN_STRUCTURE, COL_DANGER_LIGHT
)


def draw_gradient_bg(surface: pygame.Surface):
    """Dessine un fond avec dégradé subtil."""
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(COL_BG[0] + (COL_BG_GRADIENT[0] - COL_BG[0]) * ratio)
        g = int(COL_BG[1] + (COL_BG_GRADIENT[1] - COL_BG[1]) * ratio)
        b = int(COL_BG[2] + (COL_BG_GRADIENT[2] - COL_BG[2]) * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))


def draw_panel(surface: pygame.Surface, rect: pygame.Rect,
               title: str = "", font: pygame.font.Font = None):
    """Dessine un panneau avec effet de profondeur."""
    # Ombre
    shadow_rect = rect.copy()
    shadow_rect.x += 5
    shadow_rect.y += 5
    pygame.draw.rect(surface, (20, 20, 30), shadow_rect, border_radius=20)

    # Panneau principal
    pygame.draw.rect(surface, COL_PANEL, rect, border_radius=20)

    # Bordure lumineuse en haut
    highlight_rect = pygame.Rect(rect.x + 2, rect.y + 2, rect.width - 4, 3)
    pygame.draw.rect(surface, COL_PANEL_LIGHT, highlight_rect, border_radius=2)

    # Titre si présent
    if title and font:
        title_surf = font.render(title, True, COL_TEXT_DIM)
        surface.blit(title_surf, (rect.x + 20, rect.y + 15))


def draw_hangman(surface: pygame.Surface, errors: int, center_x: int, center_y: int,
                 max_errors: int = 7):
    """Dessine le pendu avec des formes pygame."""
    base_y = center_y + 120
    pole_height = 280
    beam_width = 120
    rope_length = 40

    structure_color = COL_HANGMAN_STRUCTURE
    body_color = COL_HANGMAN

    # Structure (toujours visible)
    # Base
    pygame.draw.rect(surface, structure_color,
                     (center_x - 80, base_y, 160, 15), border_radius=4)
    # Poteau vertical
    pygame.draw.rect(surface, structure_color,
                     (center_x - 60, base_y - pole_height, 15, pole_height), border_radius=3)
    # Poutre horizontale
    pygame.draw.rect(surface, structure_color,
                     (center_x - 60, base_y - pole_height, beam_width, 12), border_radius=3)
    # Corde
    pygame.draw.rect(surface, structure_color,
                     (center_x + beam_width - 70, base_y - pole_height + 12, 4, rope_length))

    # Point d'attache de la tête
    head_x = center_x + beam_width - 68
    head_y = base_y - pole_height + 12 + rope_length + 25

    # Parties du corps selon le nombre d'erreurs
    if errors >= 1:
        # Tête
        pygame.draw.circle(surface, body_color, (head_x, head_y), 25, 4)
        # Yeux
        if errors >= max_errors:
            # X pour les yeux
            pygame.draw.line(surface, COL_DANGER, (head_x - 12, head_y - 8),
                           (head_x - 4, head_y), 3)
            pygame.draw.line(surface, COL_DANGER, (head_x - 12, head_y),
                           (head_x - 4, head_y - 8), 3)
            pygame.draw.line(surface, COL_DANGER, (head_x + 4, head_y - 8),
                           (head_x + 12, head_y), 3)
            pygame.draw.line(surface, COL_DANGER, (head_x + 4, head_y),
                           (head_x + 12, head_y - 8), 3)
        else:
            # Yeux normaux
            pygame.draw.circle(surface, body_color, (head_x - 8, head_y - 5), 4, 2)
            pygame.draw.circle(surface, body_color, (head_x + 8, head_y - 5), 4, 2)

        # Bouche
        if errors >= max_errors:
            # Bouche triste
            pygame.draw.arc(surface, COL_DANGER,
                          (head_x - 10, head_y + 5, 20, 15),
                          math.pi * 0.1, math.pi * 0.9, 2)
        elif errors >= 5:
            # Bouche inquiète
            pygame.draw.line(surface, body_color,
                           (head_x - 7, head_y + 10), (head_x + 7, head_y + 12), 2)
        else:
            # Bouche neutre
            pygame.draw.line(surface, body_color,
                           (head_x - 6, head_y + 10), (head_x + 6, head_y + 10), 2)

    body_top = head_y + 25
    body_bottom = body_top + 70

    if errors >= 2:
        # Corps
        pygame.draw.line(surface, body_color,
                        (head_x, body_top), (head_x, body_bottom), 4)

    if errors >= 3:
        # Bras gauche
        pygame.draw.line(surface, body_color,
                        (head_x, body_top + 15), (head_x - 35, body_top + 45), 4)

    if errors >= 4:
        # Bras droit
        pygame.draw.line(surface, body_color,
                        (head_x, body_top + 15), (head_x + 35, body_top + 45), 4)

    if errors >= 5:
        # Jambe gauche
        pygame.draw.line(surface, body_color,
                        (head_x, body_bottom), (head_x - 30, body_bottom + 50), 4)

    if errors >= 6:
        # Jambe droite
        pygame.draw.line(surface, body_color,
                        (head_x, body_bottom), (head_x + 30, body_bottom + 50), 4)

    if errors >= 7:
        # Chapeau
        pygame.draw.ellipse(surface, COL_DANGER_LIGHT,
                           (head_x - 20, head_y - 45, 40, 12))
        pygame.draw.rect(surface, COL_DANGER_LIGHT,
                        (head_x - 12, head_y - 60, 24, 20), border_radius=3)


def draw_word_display(surface: pygame.Surface, masked_word: str,
                      x: int, y: int, font: pygame.font.Font,
                      letter_found_anim: dict[int, float],
                      max_width: int = 480):
    """Affiche le mot avec animations pour chaque lettre."""
    # Compter les lettres (sans les espaces)
    letters_only = [c for c in masked_word if c != ' ']
    num_letters = len(letters_only)

    # Adapter l'espacement selon la longueur du mot
    if num_letters <= 10:
        letter_spacing = 45
        line_width = 30
    elif num_letters <= 14:
        letter_spacing = 35
        line_width = 25
    else:
        letter_spacing = 28
        line_width = 20

    # Centrer le mot si possible
    total_width = num_letters * letter_spacing
    start_x = x + max(0, (max_width - total_width) // 2)

    letter_index = 0
    for i, char in enumerate(masked_word):
        if char == ' ':
            continue

        lx = start_x + letter_index * letter_spacing
        ly = y

        # Animation si la lettre vient d'être trouvée
        anim = letter_found_anim.get(i, 0)
        if anim > 0:
            ly -= int(anim * 15)
            letter_found_anim[i] = max(0, anim - 0.05)

        if char == '_':
            pygame.draw.line(surface, COL_TEXT_DIM,
                           (lx, ly + 35), (lx + line_width, ly + 35), 3)
        else:
            color = COL_ACCENT if anim > 0 else COL_TEXT
            text = font.render(char.upper(), True, color)
            text_rect = text.get_rect(center=(lx + line_width // 2, ly + 15))
            surface.blit(text, text_rect)
            pygame.draw.line(surface, COL_ACCENT,
                           (lx, ly + 35), (lx + line_width, ly + 35), 3)

        letter_index += 1


def draw_message_popup(surface: pygame.Surface, message: str, msg_type: str,
                       font: pygame.font.Font, animation: float):
    """Affiche un message animé (victoire, défaite, etc.)."""
    from config.theme import COL_GOLD, COL_DANGER_LIGHT

    if animation <= 0:
        return

    if msg_type == "win":
        text_color = COL_GOLD
    elif msg_type == "lose":
        text_color = COL_DANGER_LIGHT
    else:
        text_color = COL_TEXT

    # Overlay semi-transparent
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, int(150 * animation)))
    surface.blit(overlay, (0, 0))

    # Boîte de message
    box_width = 500
    box_height = 220
    box_x = (WIDTH - box_width) // 2
    box_y = (HEIGHT - box_height) // 2 - int((1 - animation) * 50)

    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
    pygame.draw.rect(surface, COL_PANEL, box_rect, border_radius=25)
    pygame.draw.rect(surface, text_color, box_rect, width=4, border_radius=25)

    # Texte
    lines = message.split('\n')
    for i, line in enumerate(lines):
        text_surf = font.render(line, True, text_color)
        text_rect = text_surf.get_rect(center=(WIDTH // 2, box_y + 50 + i * 45))
        surface.blit(text_surf, text_rect)
