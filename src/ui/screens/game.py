"""Écran de jeu principal."""
import pygame
from .base import BaseScreen
from ui.components import Button, VirtualKeyboard
from ui.renderer import draw_hangman, draw_word_display, draw_panel, draw_message_popup
from core import charger_mots, choisir_mot, afficher_mot_masque, est_gagne, coeff_difficulte, enregistrer_score
from config.theme import (
    COL_ACCENT, COL_ACCENT_LIGHT, COL_TEXT, COL_TEXT_DIM, COL_DANGER,
    COL_KEY_DEFAULT, COL_KEY_HOVER
)
from config.settings import WIDTH, HEIGHT, MAX_ERRORS, WORDS_FILE, SCORES_FILE


class GameScreen(BaseScreen):
    """Écran de jeu principal."""

    def __init__(self, game_state: dict):
        super().__init__(game_state)

        self.btn_retour = Button(20, 20, 120, 40, "← Retour", COL_KEY_DEFAULT, COL_KEY_HOVER)
        self.btn_rejouer = Button(WIDTH // 2 - 100, 520, 200, 50, "Rejouer",
                                  COL_ACCENT, COL_ACCENT_LIGHT)
        self.keyboard = VirtualKeyboard(450, 480)

        # État du jeu
        self.mot = ""
        self.lettres_trouvees: set[str] = set()
        self.lettres_tentees: set[str] = set()
        self.erreurs = 0
        self.message = ""
        self.message_timer = 0.0

        # État de fin de partie
        self.game_over = False
        self.game_over_animation = 0.0
        self.game_over_message = ""
        self.game_over_type = ""

        # Animations
        self.letter_found_anim: dict[int, float] = {}

    def start_new_game(self):
        """Démarre une nouvelle partie."""
        mots = charger_mots(WORDS_FILE)
        difficulty = self.game_state.get('difficulty', 'facile')

        self.mot = choisir_mot(mots, difficulty)
        self.lettres_trouvees = set()
        self.lettres_tentees = set()
        self.erreurs = 0
        self.message = ""
        self.message_timer = 0
        self.game_over = False
        self.game_over_animation = 0
        self.game_over_message = ""
        self.game_over_type = ""
        self.letter_found_anim = {}
        self.keyboard.reset()

    def process_letter(self, ch: str):
        """Traite une lettre jouée."""
        if ch in self.lettres_tentees:
            self.message = "Déjà essayé !"
            self.message_timer = 1.5
            return

        self.lettres_tentees.add(ch)
        difficulty = self.game_state.get('difficulty', 'facile')
        player_name = self.game_state.get('player_name', 'Joueur')

        if ch in self.mot:
            self.lettres_trouvees.add(ch)
            self.keyboard.set_key_state(ch, "correct")
            self.message = "Bien joué !"
            self.message_timer = 1.5

            # Animation pour les lettres trouvées
            masked = afficher_mot_masque(self.mot, self.lettres_trouvees)
            for i, c in enumerate(masked):
                if c == ch:
                    self.letter_found_anim[i] = 1.0

            # Vérifier victoire
            if est_gagne(self.mot, self.lettres_trouvees):
                self.game_over = True
                self.game_over_type = "win"
                score = (MAX_ERRORS - self.erreurs) * coeff_difficulte(difficulty)
                enregistrer_score(SCORES_FILE, player_name, score, difficulty)
                self.game_over_message = f"VICTOIRE !\nMot : {self.mot.upper()}\nScore : {score} pts"
        else:
            self.erreurs += 1
            self.keyboard.set_key_state(ch, "wrong")
            self.message = "Raté..."
            self.message_timer = 1.5

            # Vérifier défaite
            if self.erreurs >= MAX_ERRORS:
                self.game_over = True
                self.game_over_type = "lose"
                enregistrer_score(SCORES_FILE, player_name, 0, difficulty)
                self.game_over_message = f"PERDU...\nMot : {self.mot.upper()}\nScore : 0 pts"

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if self.btn_retour.is_clicked(event):
            return "MENU"

        if self.game_over:
            if self.btn_rejouer.is_clicked(event):
                self.start_new_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_new_game()
                elif event.key == pygame.K_ESCAPE:
                    return "MENU"
        else:
            # Clic sur clavier virtuel
            clicked_letter = self.keyboard.handle_event(event)
            if clicked_letter:
                self.process_letter(clicked_letter)

            # Ou touche clavier physique
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"
                else:
                    ch = event.unicode.lower()
                    if len(ch) == 1 and ch.isalpha():
                        self.process_letter(ch)

        return None

    def update(self, dt: float, mouse_pos: tuple):
        self.btn_retour.update(mouse_pos)
        self.keyboard.update(mouse_pos)

        if self.game_over:
            self.game_over_animation = min(1.0, self.game_over_animation + dt * 3)
            self.btn_rejouer.update(mouse_pos)

        if self.message_timer > 0:
            self.message_timer -= dt

    def draw(self, surface: pygame.Surface, fonts: dict):
        self.btn_retour.draw(surface, fonts['ui'])

        # Info joueur et difficulté
        player_name = self.game_state.get('player_name', 'Joueur')
        difficulty = self.game_state.get('difficulty', 'facile')
        info_text = fonts['ui'].render(f"{player_name} | {difficulty.capitalize()}",
                                       True, COL_TEXT_DIM)
        surface.blit(info_text, (WIDTH - 200, 25))

        # Panneau gauche - Pendu
        panel_left = pygame.Rect(30, 80, 380, 380)
        draw_panel(surface, panel_left, "Le Pendu", fonts['ui'])
        draw_hangman(surface, self.erreurs, panel_left.centerx, panel_left.centery + 20)

        # Compteur d'erreurs
        err_text = fonts['ui'].render(f"Erreurs : {self.erreurs}/{MAX_ERRORS}", True,
                                      COL_DANGER if self.erreurs > 4 else COL_TEXT)
        surface.blit(err_text, (panel_left.x + 20, panel_left.bottom - 35))

        # Panneau droit - Mot
        panel_right = pygame.Rect(430, 80, 540, 150)
        draw_panel(surface, panel_right, "Mot à deviner", fonts['ui'])

        masked = afficher_mot_masque(self.mot, self.lettres_trouvees)
        draw_word_display(surface, masked, panel_right.x + 40, panel_right.y + 60,
                         fonts['word'], self.letter_found_anim)

        # Message temporaire
        if self.message_timer > 0 and not self.game_over:
            msg_color = COL_ACCENT if "joué" in self.message else COL_DANGER
            msg_surf = fonts['ui'].render(self.message, True, msg_color)
            surface.blit(msg_surf, (panel_right.x + 40, panel_right.bottom - 35))

        # Zone clavier
        panel_keyboard = pygame.Rect(430, 250, 540, 220)
        draw_panel(surface, panel_keyboard, "Clavier", fonts['ui'])
        self.keyboard.draw(surface, fonts['key'])

        # Aide
        help_text = fonts['ui'].render("Cliquez sur une lettre ou tapez au clavier",
                                       True, COL_TEXT_DIM)
        surface.blit(help_text, (450, HEIGHT - 40))

        # Popup de fin de partie
        if self.game_over:
            draw_message_popup(surface, self.game_over_message, self.game_over_type,
                             fonts['big'], self.game_over_animation)
            if self.game_over_animation > 0.8:
                self.btn_rejouer.draw(surface, fonts['ui'])
                hint = fonts['ui'].render("Entrée = Rejouer | Échap = Menu",
                                         True, COL_TEXT_DIM)
                surface.blit(hint, hint.get_rect(center=(WIDTH // 2, 590)))
