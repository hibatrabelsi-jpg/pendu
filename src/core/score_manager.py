"""Gestion des scores du jeu."""
from pathlib import Path


def charger_scores(fichier: Path) -> list[tuple[str, int, str]]:
    """
    Charge les scores depuis le fichier.
    Retourne une liste de tuples (nom, score, difficulté).
    """
    scores: list[tuple[str, int, str]] = []

    if not fichier.exists():
        return scores

    for ligne in fichier.read_text(encoding="utf-8").splitlines():
        ligne = ligne.strip()
        if not ligne:
            continue

        morceaux = ligne.split(";")
        if len(morceaux) != 3:
            continue

        nom, score_str, difficulte = morceaux
        try:
            score = int(score_str)
        except ValueError:
            continue

        scores.append((nom, score, difficulte))

    return scores


def enregistrer_score(fichier: Path, nom: str, score: int, difficulte: str) -> None:
    """Enregistre un score dans le fichier."""
    nom = nom.strip().lower()
    difficulte = difficulte.strip().lower()

    with fichier.open("a", encoding="utf-8") as f:
        f.write(f"{nom};{score};{difficulte}\n")


def effacer_scores(fichier: Path) -> tuple[bool, str]:
    """
    Efface tous les scores.
    Retourne (succès, message).
    """
    try:
        with fichier.open("w", encoding="utf-8") as f:
            f.write("")
        return True, "Historique effacé !"
    except Exception as e:
        return False, f"Erreur: {str(e)}"
