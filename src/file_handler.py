import random
import os

def charger_mots(fichier='mots.txt'):
    chemin = os.path.join(os.path.dirname(__file__), '..', 'data', fichier)
    with open(chemin, 'r', encoding='utf-8') as f:
        mots = f.read().splitlines()
    return [mot for mot in mots if mot]

def choisir_mot_aleatoire(fichier='mots.txt'):
    mots = charger_mots(fichier)
    return random.choice(mots)

def sauvegarder_score(nom_joueur, score, fichier='scores.txt'):
    chemin = os.path.join(os.path.dirname(__file__), '..', 'data', fichier)
    with open(chemin, 'a', encoding='utf-8') as f:
        f.write(f"{nom_joueur},{score}\n")

def charger_scores(fichier='scores.txt'):
    chemin = os.path.join(os.path.dirname(__file__), '..', 'data', fichier)
    try:
        with open(chemin, 'r', encoding='utf-8') as f:
            lignes = f.read().splitlines()
            scores = []
            for ligne in lignes:
                if ligne:
                    nom, score = ligne.split(',')
                    scores.append((nom, int(score)))
            scores.sort(key=lambda x: x[1], reverse=True)
            return scores
    except FileNotFoundError:
        return []