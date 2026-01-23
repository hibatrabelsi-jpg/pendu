import sys
from pathlib import Path
import pygame

# On reutilise ta logique console
from pendu import charger_mots, choisir_mot, afficher_mot_masque, est_gagne, WORDS_FILE

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets" / "images"

# --- Theme A (Voyage chic) ---
COL_BG = (246, 239, 230)
COL_PANEL = (239, 227, 211)
COL_TEXT = (31, 31, 31)
COL_ACCENT = (47, 93, 80)
COL_GOLD = (182, 141, 64)
COL_DANGER = (200, 75, 75)
COL_BTN = (255, 255, 255)
COL_BTN_HOVER = (231, 240, 237)

# --- Window ---
WIDTH, HEIGHT = 900, 600
FPS = 60

# --- Game rules ---
MAX_ERRORS = 7


def load_hangman_sprites(folder: Path) -> list[pygame.Surface | None]:
    """
    Load hangman0.png ... hangman7.png from assets/images
    Return a list length 8. If a file is missing, put None.
    """
    sprites: list[pygame.Surface | None] = []
    for i in range(MAX_ERRORS + 1):
        p = folder / f"hangman{i}.png"
        if p.exists():
            img = pygame.image.load(str(p)).convert_alpha()
            sprites.append(img)
        else:
            sprites.append(None)
    return sprites


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pendu - Voyage")
    clock = pygame.time.Clock()

    font_title = pygame.font.SysFont("arial", 48, bold=True)
    font_ui = pygame.font.SysFont("arial", 22)
    font_big = pygame.font.SysFont("arial", 32, bold=True)

    hangman_sprites = load_hangman_sprites(ASSETS_DIR)

    # --- Load words once ---
    mots = charger_mots(WORDS_FILE)

    # --- Basic state machine ---
    state = "MENU"  # MENU / GAME / SCORES

    # --- Game state ---
    difficulte = "facile"
    mot = ""
    lettres_trouvees: set[str] = set()
    lettres_tentees: set[str] = set()
    erreurs = 0
    message = ""

    def start_new_game(diff: str):
        nonlocal difficulte, mot, lettres_trouvees, lettres_tentees, erreurs, message
        difficulte = diff
        mot = choisir_mot(mots, difficulte)
        lettres_trouvees = set()
        lettres_tentees = set()
        erreurs = 0
        message = ""

    start_new_game(difficulte)

    running = True
    while running:
        clock.tick(FPS)

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # For now: press keys to test quickly
            if state == "MENU" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    start_new_game("facile")
                    state = "GAME"
                elif event.key == pygame.K_2:
                    start_new_game("moyen")
                    state = "GAME"
                elif event.key == pygame.K_3:
                    start_new_game("difficile")
                    state = "GAME"
                elif event.key == pygame.K_ESCAPE:
                    running = False

            if state == "GAME" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "MENU"
                else:
                    # Only letters
                    ch = event.unicode.lower()
                    if len(ch) == 1 and ch.isalpha():
                        if ch in lettres_tentees:
                            message = "Deja tente."
                        else:
                            lettres_tentees.add(ch)
                            if ch in mot:
                                lettres_trouvees.add(ch)
                                message = "Bien vu!"
                            else:
                                erreurs += 1
                                message = "Rate."

        # --- Draw ---
        screen.fill(COL_BG)

        if state == "MENU":
            title = font_title.render("PENDU - VOYAGE", True, COL_ACCENT)
            screen.blit(title, (50, 50))

            help1 = font_ui.render("1: Jouer facile", True, COL_TEXT)
            help2 = font_ui.render("2: Jouer moyen", True, COL_TEXT)
            help3 = font_ui.render("3: Jouer difficile", True, COL_TEXT)
            help4 = font_ui.render("ESC: Quitter", True, COL_TEXT)
            screen.blit(help1, (60, 160))
            screen.blit(help2, (60, 195))
            screen.blit(help3, (60, 230))
            screen.blit(help4, (60, 265))

        elif state == "GAME":
            # Left panel: hangman sprite
            panel_rect = pygame.Rect(40, 40, 360, 520)
            pygame.draw.rect(screen, COL_PANEL, panel_rect, border_radius=18)

            sprite = hangman_sprites[min(erreurs, MAX_ERRORS)]
            if sprite is not None:
                # Fit inside panel area
                img = sprite
                img_rect = img.get_rect()
                img_rect.center = (panel_rect.centerx, panel_rect.centery)
                screen.blit(img, img_rect)
            else:
                # Fallback if sprites missing
                t = font_big.render(f"ERREURS: {erreurs}/{MAX_ERRORS}", True, COL_DANGER)
                screen.blit(t, (panel_rect.x + 40, panel_rect.y + 240))

            # Right panel: word + tries
            panel2 = pygame.Rect(430, 40, 430, 520)
            pygame.draw.rect(screen, COL_PANEL, panel2, border_radius=18)

            masked = afficher_mot_masque(mot, lettres_trouvees)
            txt_word = font_big.render(masked, True, COL_TEXT)
            screen.blit(txt_word, (panel2.x + 30, panel2.y + 60))

            tried = " ".join(sorted(lettres_tentees)) if lettres_tentees else "(aucune)"
            txt_tried = font_ui.render(f"Tentees: {tried}", True, COL_TEXT)
            screen.blit(txt_tried, (panel2.x + 30, panel2.y + 120))

            txt_msg = font_ui.render(message, True, COL_ACCENT if "Bien" in message else COL_DANGER)
            screen.blit(txt_msg, (panel2.x + 30, panel2.y + 160))

            # Win/lose check
            if est_gagne(mot, lettres_trouvees):
                win = font_big.render("GAGNE! (ESC = menu)", True, COL_ACCENT)
                screen.blit(win, (panel2.x + 30, panel2.y + 220))
            elif erreurs >= MAX_ERRORS:
                lose = font_big.render(f"PERDU! Mot: {mot}", True, COL_DANGER)
                screen.blit(lose, (panel2.x + 30, panel2.y + 220))

            hint = font_ui.render("Tape une lettre. ESC = menu", True, COL_TEXT)
            screen.blit(hint, (panel2.x + 30, panel2.y + 470))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
