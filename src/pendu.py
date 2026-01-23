import random
from pathlib import Path


# Chemins des fichiers
BASE_DIR = Path(__file__).resolve().parent.parent
WORDS_FILE = BASE_DIR / "data" / "liste_mots.txt"


def charger_mots(fichier: Path) -> list[str]:

    #Lit un fichier texte (1 mot par ligne) et retourne une liste de mots propres. 
    # enlève les espaces, met en minuscule, ignore les lignes vides

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

    #Choisit un mot selon une difficulté simple : facile  : mots de 4 à 6 lettres, moyen   : mots de 7 à 9 lettres, difficile : mots de 10 lettres et +, Si aucun mot ne correspond, on choisit au hasard dans toute la liste.

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

def ajouter_mot(fichier: Path) -> None:
    
    #Permet d'ajouter un mot dans le fichier liste_mots.txt
    #(sans accent, lettres uniquement, pas de doublon)
    mots_existants = charger_mots(fichier)

    while True:
        nouveau_mot = input("Entre un nouveau mot (sans accent) : ").strip().lower()

        if not nouveau_mot.isalpha():
            print(" Lettres uniquement (a-z).")
            continue

        if nouveau_mot in mots_existants:
            print("Ce mot existe déjà.")
            continue

        with fichier.open("a", encoding="utf-8") as f:
            f.write(nouveau_mot + "\n")

        print(f"Mot '{nouveau_mot}' ajouté avec succès.")
        mots_existants.append(nouveau_mot)
        break

SCORES_FILE = BASE_DIR / "data" / "scores.txt"

def enregistrer_score(fichier: Path, nom: str, score: int, difficulte: str) -> None:
    nom = nom.strip().lower()
    difficulte = difficulte.strip().lower()

    with fichier.open("a", encoding="utf-8") as f:
        f.write(f"{nom};{score};{difficulte}\n")


def charger_scores(fichier: Path) -> list[tuple[str, int, str]]:
    scores: list[tuple[str, int, str]] = []

    if not fichier.exists():
        return scores  #pas encore de fichier = pas de scores

    for ligne in fichier.read_text(encoding="utf-8").splitlines():
        ligne = ligne.strip()
        if not ligne:
            continue

        morceaux = ligne.split(";")
        if len(morceaux) != 3:
            continue  #ligne mal formée, on l'ignore

        nom, score_str, difficulte = morceaux
        try:
            score = int(score_str)
        except ValueError:
            continue  #score pas convertible -> on ignore

        scores.append((nom, score, difficulte))

    return scores


def afficher_scores(fichier: Path, top: int = 10) -> None:
    scores = charger_scores(fichier)

    if not scores:
        print("Aucun score enregistré pour le moment.")
        return

    #tri du plus grand score au plus petit
    scores_tries = sorted(scores, key=lambda x: x[1], reverse=True)

    print("\nTOP SCORES")
    for i, (nom, score, difficulte) in enumerate(scores_tries[:top], start=1):
        print(f"{i}. {nom} - {score} ({difficulte})")

def coeff_difficulte(difficulte: str) -> int:
    difficulte = difficulte.strip().lower()
    if difficulte == "facile":
        return 1
    if difficulte == "moyen":
        return 2
    if difficulte == "difficile":
        return 3
    return 1


def demander_difficulte() -> str:
    while True:
        d = input("Difficulté (facile/moyen/difficile): ").strip().lower()
        if d in ("facile", "moyen", "difficile"):
            return d
        print("X Choisis: facile, moyen, ou difficile.")


def demander_nom_joueur() -> str:
    while True:
        nom = input("Nom du joueur: ").strip()
        if nom:
            return nom
        print("X Le nom ne peut pas être vide.")


def jouer_partie_console() -> None:
    # 1) Préparation
    nom = demander_nom_joueur()
    difficulte = demander_difficulte()

    mots = charger_mots(WORDS_FILE)
    mot = choisir_mot(mots, difficulte)

    erreurs_max = 7
    erreurs = 0
    lettres_trouvees: set[str] = set()
    lettres_tentees: set[str] = set()

    print("\nPartie lancée !")

    # 2) Boucle de jeu
    while True:
        print("\nMot :", afficher_mot_masque(mot, lettres_trouvees))
        print("Tentées :", " ".join(sorted(lettres_tentees)) if lettres_tentees else "(aucune)")
        print(f"Erreurs : {erreurs}/{erreurs_max}")

        lettre = demander_lettre()

        if lettre in lettres_tentees:
            print("⚠️ Déjà tenté.")
            continue

        lettres_tentees.add(lettre)

        if lettre in mot:
            lettres_trouvees.add(lettre)
            print("Bien vu !")
        else:
            erreurs += 1
            print("X Raté.")

        # 3) Conditions de fin
        if est_gagne(mot, lettres_trouvees):
            vies_restantes = erreurs_max - erreurs
            score = vies_restantes * coeff_difficulte(difficulte)

            print(f"\n🏆 Gagné ! Le mot était: {mot}")
            print(f"Score: {vies_restantes} vies restantes × coeff = {score}")

            enregistrer_score(SCORES_FILE, nom, score, difficulte)
            print(" Score enregistré.")
            break

        if erreurs >= erreurs_max:
            print(f"\n Perdu... Le mot était: {mot}")
            print("Score: 0")
            enregistrer_score(SCORES_FILE, nom, 0, difficulte)
            print("Score enregistré.")
            break


def menu_console() -> None:
    while True:
        print("\n=== MENU PENDU ===")
        print("1) Jouer")
        print("2) Ajouter un mot")
        print("3) Voir les scores")
        print("4) Quitter")

        choix = input("Ton choix: ").strip()

        if choix == "1":
            jouer_partie_console()
        elif choix == "2":
            ajouter_mot(WORDS_FILE)
        elif choix == "3":
            afficher_scores(SCORES_FILE, top=10)
        elif choix == "4":
            print("Au revoir 👋")
            break
        else:
            print("X Choix invalide.")

if __name__ == "__main__":
    menu_console()
