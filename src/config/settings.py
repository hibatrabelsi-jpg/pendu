"""Configuration générale du jeu."""
from pathlib import Path

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
WORDS_FILE = DATA_DIR / "liste_mots.txt"
SCORES_FILE = DATA_DIR / "scores.txt"

# --- Window ---
WIDTH = 1000
HEIGHT = 700
FPS = 60

# --- Game rules ---
MAX_ERRORS = 7
