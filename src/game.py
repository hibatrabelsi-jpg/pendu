import random
from file_handler import charger_mots, sauvegarder_score

# Jeu en MODE CONSOLE (terminal)
# Affiche le mot avec des _ pour les lettres non trouvées
def afficher_mot(mot, lettres_ok):
    resultat = ""
    for lettre in mot:
        if lettre in lettres_ok:
            resultat += lettre + " "
        else:
            resultat += "_ "
    return resultat

# Fonction principale du jeu
def jouer():
    # Choisir un mot au hasard
    mots = charger_mots()
    mot = random.choice(mots).lower()
    
    # Initialiser les variables
    lettres_ok = []  # Lettres trouvées
    essais = []      # Toutes les lettres essayées
    erreurs = 0      # Nombre d'erreurs
    
    print("\n=== JEU DU PENDU ===")
    print(f"Mot de {len(mot)} lettres\n")
    
    # Boucle principale: jouer tant qu'on a pas 7 erreurs
    while erreurs < 7:
        # Afficher l'état actuel
        print(afficher_mot(mot, lettres_ok))
        print(f"Erreurs: {erreurs}/7")
        print(f"Essayé: {', '.join(essais)}\n")
        
        # Demander une lettre au joueur
        lettre = input("Lettre? ").lower()
        
        # Si déjà essayée, on recommence
        if lettre in essais:
            print("Déjà essayé!\n")
            continue
        
        # Ajouter aux lettres essayées
        essais.append(lettre)
        
        # Vérifier si la lettre est dans le mot
        if lettre in mot:
            lettres_ok.append(lettre)
            print("Bien!\n")
            
            # Vérifier si le mot est complet
            if all(l in lettres_ok for l in mot):
                print(f"GAGNÉ! C'était: {mot}")
                nom = input("Ton nom? ")
                score = (7 - erreurs) * 100
                sauvegarder_score(nom, score)
                break
        else:
            erreurs += 1
            print("Raté!\n")
    
    # Si on sort de la boucle sans avoir gagné
    else:
        print(f"PERDU! C'était: {mot}")

# Lancer le jeu si on exécute ce fichier
if __name__ == "__main__":
    jouer()