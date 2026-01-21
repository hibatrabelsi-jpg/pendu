# === IMPORTS ===
import random
import os

#=== FONCTION: Charger les mots ===
def charger_mots(fichier='data/liste_mots.txt'):
    chemin = os.path.join(os.path.dirname(__file__), '..', fichier)
    with open(chemin, 'r', encoding='utf-8') as f:
        mots = f.read().splitlines()
    return [mot for mot in mots if mot]

#=== FONCTION: Choisir un mot ===
def choisir_mot_aleatoire(fichier='data/liste_mots.txt'):
    mots = charger_mots(fichier)
    return random.choice(mots)

#=== FONCTION: Sauvegarder score ===
def sauvegarder_score(nom_joueur, score, fichier='data/scores.txt'):
    chemin = os.path.join(os.path.dirname(__file__), '..', fichier)
    with open(chemin, 'a', encoding='utf-8') as f:
        f.write(f"{nom_joueur},{score}\n")

#  TEST - JOUR 1
# ======================     
if __name__ == "__main__":
    liste_mots = charger_mots()
    print("Mots disponibles:", liste_mots)
    print("Total:", len(liste_mots))
    mot_choisi = choisir_mot_aleatoire()
    print("Mot sélectionné:", mot_choisi)     