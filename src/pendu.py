import random
from pathlib import Path


# Chemins des fichiers
BASE_DIR = Path(__file__).resolve().parent.parent
WORDS_FILE = BASE_DIR / "data" / "liste_mots.txt"


def charger_mots(fichier: Path) -> list[str]:
    """
    Lit un fichier texte (1 mot par ligne) et retourne une liste de mots propres.
    - enlève les espaces
    - met en minuscule
    - ignore les lignes vides
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
    Choisit un mot selon une difficulté simple :
    - facile  : mots de 4 à 6 lettres
    - moyen   : mots de 7 à 9 lettres
    - difficile : mots de 10 lettres et +
    Si aucun mot ne correspond, on choisit au hasard dans toute la liste.
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
    
    #Renvoie une version masquée du mot. Exemple : "voyage" + {'v','a'} -> "v _ _ a _ _
    affichage = []
    for lettre in mot:
        if lettre in lettres_trouvees:
            affichage.append(lettre)
        else:
            affichage.append("_")
    return " ".join(affichage)


def est_gagne(mot: str, lettres_trouvees: set[str]) -> bool:
    #Vrai si toutes les lettres du mot sont trouvées.
    return all(lettre in lettres_trouvees for lettre in mot)


def demander_lettre() -> str:
    #Demande une lettre à l'utilisateur.1 seul caractère - alphabétique uniquement
    
    while True:
        entree = input("Choisis une lettre: ").strip().lower()
        if len(entree) != 1:
            print("X Une seule lettre.")
            continue
        if not entree.isalpha():
            print("X Une lettre (a-z) seulement.")
            continue
        return entree


def jouer_console():

    #Version console pour tester la logique.
    
    mots = charger_mots(WORDS_FILE)

    difficulte = input("Difficulté (facile/moyen/difficile): ").strip().lower()
    mot = choisir_mot(mots, difficulte)

    erreurs_max = 7  # correspond aux 7 étapes du pendu du sujet
    erreurs = 0

    lettres_trouvees: set[str] = set()
    lettres_tentees: set[str] = set()

    print("\nPartie lancée !")

    while True:
        print("\nMot :", afficher_mot_masque(mot, lettres_trouvees))
        print("Tentées :", " ".join(sorted(lettres_tentees)) if lettres_tentees else "(aucune)")
        print(f"Erreurs : {erreurs}/{erreurs_max}")

        lettre = demander_lettre()

        if lettre in lettres_tentees:
            print(" X Déjà tenté.")
            continue

        lettres_tentees.add(lettre)

        if lettre in mot:
            lettres_trouvees.add(lettre)
            print("Bien vu !")
        else:
            erreurs += 1
            print("X Raté.")

        if est_gagne(mot, lettres_trouvees):
            print("\n🏆 Gagné ! Le mot était:", mot)
            break

        if erreurs >= erreurs_max:
            print("\nPerdu... Le mot était:", mot)
            break


if __name__ == "__main__":
    jouer_console()
