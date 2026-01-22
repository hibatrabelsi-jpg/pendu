# Jeu du Pendu - Version Terminal Simple
from file_handler import choisir_mot_aleatoire, sauvegarder_score
import os

def clear_screen():
    """Efface l'écran"""
    os.system('cls' if os.name == 'nt' else 'clear')

def dessiner_pendu(erreurs):
    """Dessine le pendu selon le nombre d'erreurs"""
    stages = [
        """
           --------
           |      |
           |      
           |     
           |      
           |     
        """,
        """
           --------
           |      |
           |      O
           |     
           |      
           |     
        """,
        """
           --------
           |      |
           |      O
           |      |
           |      
           |     
        """,
        """
           --------
           |      |
           |      O
           |     /|
           |      
           |     
        """,
        """
           --------
           |      |
           |      O
           |     /|\\
           |      
           |     
        """,
        """
           --------
           |      |
           |      O
           |     /|\\
           |     / 
           |     
        """,
        """
           --------
           |      |
           |      O
           |     /|\\
           |     / \\
           |     
        """
    ]
    return stages[min(erreurs, 6)]

def afficher_mot(mot, lettres_trouvees):
    """Affiche le mot avec _ pour lettres non trouvées"""
    affichage = ""
    for lettre in mot:
        if lettre.upper() in lettres_trouvees:
            affichage += lettre.upper() + " "
        else:
            affichage += "_ "
    return affichage

def jouer():
    """Lance une partie de pendu"""
    # Choisir un mot
    mot_secret = choisir_mot_aleatoire().upper()
    
    # Variables du jeu
    lettres_trouvees = []
    lettres_ratees = []
    erreurs = 0
    max_erreurs = 6
    
    print("\n" + "="*50)
    print("🎮 JEU DU PENDU")
    print("="*50)
    
    # Boucle de jeu
    while erreurs < max_erreurs:
        clear_screen()
        
        # Affichage
        print(dessiner_pendu(erreurs))
        print(f"\nMot: {afficher_mot(mot_secret, lettres_trouvees)}")
        print(f"\nErreurs: {erreurs}/{max_erreurs}")
        print(f"Lettres essayées: {' '.join(sorted(lettres_trouvees + lettres_ratees))}")
        
        # Vérifier victoire
        if all(lettre in lettres_trouvees for lettre in mot_secret):
            print("\n" + "="*50)
            print("🎉 GAGNÉ!")
            print(f"Le mot était: {mot_secret}")
            score = (7 - erreurs) * 100
            print(f"Score: {score} points")
            print("="*50)
            
            # Demander le nom
            nom = input("\nEntre ton nom: ").strip()
            if not nom:
                nom = "Joueur"
            sauvegarder_score(nom, score)
            print(f"\n✅ Score de {nom} sauvegardé!")
            return
        
        # Demander une lettre
        lettre = input("\n💡 Propose une lettre: ").strip().upper()
        
        # Vérifications
        if len(lettre) != 1 or not lettre.isalpha():
            input("❌ Entre une seule lettre! (Appuie sur ENTER)")
            continue
        
        if lettre in lettres_trouvees or lettre in lettres_ratees:
            input("⚠️ Lettre déjà essayée! (Appuie sur ENTER)")
            continue
        
        # Vérifier la lettre
        if lettre in mot_secret:
            lettres_trouvees.append(lettre)
            print(f"✅ Oui! '{lettre}' est dans le mot!")
        else:
            lettres_ratees.append(lettre)
            erreurs += 1
            print(f"❌ Non! '{lettre}' n'est pas dans le mot!")
        
        input("(Appuie sur ENTER pour continuer)")
    
    # Perdu
    clear_screen()
    print(dessiner_pendu(erreurs))
    print("\n" + "="*50)
    print("😢 PERDU!")
    print(f"Le mot était: {mot_secret}")
    print("="*50)

def menu():
    """Menu principal"""
    while True:
        clear_screen()
        print("\n" + "="*50)
        print("🎮 PENDU - MENU PRINCIPAL")
        print("="*50)
        print("\n1. Jouer")
        print("2. Voir les scores")
        print("3. Quitter")
        
        choix = input("\nChoisis une option (1-3): ").strip()
        
        if choix == "1":
            jouer()
            input("\nAppuie sur ENTER pour retourner au menu...")
        elif choix == "2":
            from file_handler import charger_scores
            clear_screen()
            print("\n" + "="*50)
            print("🏆 LEADERBOARD")
            print("="*50)
            scores = charger_scores()
            if scores:
                for i, (nom, score) in enumerate(scores[:10], 1):
                    print(f"{i}. {nom}: {score} points")
            else:
                print("\nAucun score enregistré!")
            input("\nAppuie sur ENTER pour retourner au menu...")
        elif choix == "3":
            print("\n👋 Au revoir!")
            break
        else:
            print("\n❌ Choix invalide!")
            input("Appuie sur ENTER...")

if __name__ == "__main__":
    menu()