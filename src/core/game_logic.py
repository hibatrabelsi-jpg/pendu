"""Logique métier du jeu de pendu."""
import random
from pathlib import Path


def charger_mots(fichier: Path) -> list[str]:
    """
    Lit un fichier texte (1 mot par ligne) et retourne une liste de mots propres.
    Enlève les espaces, met en minuscule, ignore les lignes vides.
    """
    if not fichier.exists():
        raise FileNotFoundError(f"Fichier introuvable: {fichier}")

    mots: list[str] = []
    for ligne in fichier.read_text(encoding="utf-8").splitlines():
        mot = ligne.strip().lower()
        if mot:
            mots.append(mot)

    if len(mots) < 1:
        raise ValueError("La liste de mots est vide.")

    return mots


def choisir_mot(mots: list[str], difficulte: str) -> str:
    """
    Choisit un mot selon une difficulté:
    - facile: mots de 4 à 6 lettres
    - moyen: mots de 7 à 9 lettres
    - difficile: mots de 10 lettres et +

    Si aucun mot ne correspond, choisit au hasard dans toute la liste.
    """
    difficulte = difficulte.lower()

    if difficulte == "facile":
        filtres = [m for m in mots if 4 <= len(m) <= 6]
    elif difficulte == "moyen":
        filtres = [m for m in mots if 7 <= len(m) <= 9]
    elif difficulte == "difficile":
        filtres = [m for m in mots if len(m) >= 10]
    else:
        filtres = mots

    return random.choice(filtres if filtres else mots)


def afficher_mot_masque(mot: str, lettres_trouvees: set[str]) -> str:
    """
    Renvoie une version masquée du mot.
    Exemple: "voyage" + {'v','a'} -> "v _ _ a _ _"
    """
    affichage = []
    for lettre in mot:
        if lettre in lettres_trouvees:
            affichage.append(lettre)
        else:
            affichage.append("_")
    return " ".join(affichage)


def est_gagne(mot: str, lettres_trouvees: set[str]) -> bool:
    """Vrai si toutes les lettres du mot sont trouvées."""
    return all(lettre in lettres_trouvees for lettre in mot)


def ajouter_mot(fichier: Path, mot: str) -> tuple[bool, str]:
    """
    Ajoute un mot au fichier.
    Retourne (succès, message).
    """
    mot = mot.strip().lower()

    if not mot:
        return False, "Le mot ne peut pas être vide"

    if not mot.isalpha():
        return False, "Lettres uniquement (a-z)"

    try:
        mots_existants = charger_mots(fichier)
        if mot in mots_existants:
            return False, "Ce mot existe déjà"

        with fichier.open("a", encoding="utf-8") as f:
            f.write(mot + "\n")

        return True, f"'{mot}' ajouté avec succès !"
    except Exception as e:
        return False, f"Erreur: {str(e)}"


def coeff_difficulte(difficulte: str) -> int:
    """Retourne le coefficient multiplicateur selon la difficulté."""
    difficulte = difficulte.strip().lower()
    if difficulte == "facile":
        return 1
    if difficulte == "moyen":
        return 2
    if difficulte == "difficile":
        return 3
    return 1
