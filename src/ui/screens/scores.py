"""Écran du tableau des scores."""
import pygame
from .base import BaseScreen
from ui.components import Button
from ui.renderer import draw_panel
from core import charger_scores, effacer_scores
from config.theme import (
    COL_ACCENT, COL_GOLD, COL_TEXT, COL_TEXT_DIM, COL_PANEL,
    COL_KEY_DEFAULT, COL_KEY_HOVER, COL_DANGER, COL_DANGER_LIGHT
)
from config.settings import WIDTH, HEIGHT, SCORES_FILE


class ScoresScreen(BaseScreen):
    """Écran du tableau des scores."""

    def __init__(self, game_state: dict):
        super().__init__(game_state)

        self.btn_retour = Button(20, 20, 120, 40, "← Retour", COL_KEY_DEFAULT, COL_KEY_HOVER)
        self.btn_effacer = Button(WIDTH // 2 - 100, 620, 200, 40, "Effacer historique",
                                  COL_DANGER, COL_DANGER_LIGHT)
        self.btn_confirmer = Button(WIDTH // 2 - 170, 400, 150, 45, "Confirmer",
                                    COL_DANGER, COL_DANGER_LIGHT)
        self.btn_annuler = Button(WIDTH // 2 + 20, 400, 150, 45, "Annuler",
                                  COL_KEY_DEFAULT, COL_KEY_HOVER)

        # État
        self.confirm_delete = False
        self.message = ""
        self.message_timer = 0.0
        self.message_success = False

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if self.confirm_delete:
            if self.btn_confirmer.is_clicked(event):
                success, msg = effacer_scores(SCORES_FILE)
                self.message = msg
                self.message_success = success
                self.message_timer = 3.0
                self.confirm_delete = False
            elif self.btn_annuler.is_clicked(event):
                self.confirm_delete = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.confirm_delete = False
        else:
            if self.btn_retour.is_clicked(event):
                self.message = ""
                return "MENU"
            elif self.btn_effacer.is_clicked(event):
                self.confirm_delete = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "MENU"

        return None

    def update(self, dt: float, mouse_pos: tuple):
        self.btn_retour.update(mouse_pos)
        self.btn_effacer.update(mouse_pos)
        if self.confirm_delete:
            self.btn_confirmer.update(mouse_pos)
            self.btn_annuler.update(mouse_pos)
        if self.message_timer > 0:
            self.message_timer -= dt

    def draw(self, surface: pygame.Surface, fonts: dict):
        self.btn_retour.draw(surface, fonts['ui'])

        # Titre
        title = fonts['big'].render("Tableau des Scores", True, COL_GOLD)
        surface.blit(title, title.get_rect(center=(WIDTH // 2, 80)))

        # Charger et afficher les scores
        scores = charger_scores(SCORES_FILE)
        scores_tries = sorted(scores, key=lambda x: x[1], reverse=True)[:10]

        if not scores_tries:
            no_score = fonts['ui'].render("Aucun score enregistré", True, COL_TEXT_DIM)
            surface.blit(no_score, no_score.get_rect(center=(WIDTH // 2, 300)))
        else:
            # Panneau
            panel = pygame.Rect(150, 130, 700, 450)
            draw_panel(surface, panel)

            # En-têtes
            header_y = 160
            headers = ["#", "Joueur", "Score", "Difficulté"]
            header_x = [200, 320, 520, 680]
            for i, h in enumerate(headers):
                h_surf = fonts['score'].render(h, True, COL_ACCENT)
                surface.blit(h_surf, (header_x[i], header_y))

            # Ligne de séparation
            pygame.draw.line(surface, COL_TEXT_DIM, (180, 195), (820, 195), 1)

            # Scores
            for i, (nom, score, diff) in enumerate(scores_tries):
                y = 210 + i * 40

                # Couleur selon le rang (or, argent, bronze)
                if i == 0:
                    color = COL_GOLD
                elif i == 1:
                    color = (200, 200, 210)
                elif i == 2:
                    color = (205, 127, 50)
                else:
                    color = COL_TEXT

                rank = fonts['score'].render(f"{i + 1}", True, color)
                name_surf = fonts['score'].render(nom[:15], True, color)
                score_surf = fonts['score'].render(str(score), True, color)
                diff_surf = fonts['score'].render(diff.capitalize(), True, color)

                surface.blit(rank, (210, y))
                surface.blit(name_surf, (320, y))
                surface.blit(score_surf, (530, y))
                surface.blit(diff_surf, (680, y))

        # Bouton effacer
        self.btn_effacer.draw(surface, fonts['ui'])

        # Message
        if self.message_timer > 0:
            msg_color = COL_ACCENT if self.message_success else COL_DANGER
            msg_surf = fonts['ui'].render(self.message, True, msg_color)
            surface.blit(msg_surf, msg_surf.get_rect(center=(WIDTH // 2, 660)))

        # Popup de confirmation
        if self.confirm_delete:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            surface.blit(overlay, (0, 0))

            box_rect = pygame.Rect(WIDTH // 2 - 200, 250, 400, 200)
            pygame.draw.rect(surface, COL_PANEL, box_rect, border_radius=20)
            pygame.draw.rect(surface, COL_DANGER, box_rect, width=3, border_radius=20)

            confirm_title = fonts['big'].render("Confirmation", True, COL_DANGER)
            surface.blit(confirm_title, confirm_title.get_rect(center=(WIDTH // 2, 290)))

            confirm_text = fonts['ui'].render("Effacer tout l'historique des scores ?", True, COL_TEXT)
            surface.blit(confirm_text, confirm_text.get_rect(center=(WIDTH // 2, 350)))

            self.btn_confirmer.draw(surface, fonts['ui'])
            self.btn_annuler.draw(surface, fonts['ui'])
