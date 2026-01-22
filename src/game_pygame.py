import pygame
import sys
import random
from file_handler import charger_mots, sauvegarder_score

# ========================================
# Paramètres de la fenêtre et couleurs
# ========================================
LARGEUR = 800
HAUTEUR = 600
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (220, 20, 60)
VERT = (60, 179, 113)

# ========================================
# Dessiner le bonhomme pendu selon les erreurs
# ========================================
def dessiner_pendu(ecran, erreurs):
    # Dessiner la potence (toujours visible)
    pygame.draw.line(ecran, NOIR, (100, 450), (250, 450), 5)  # Base
    pygame.draw.line(ecran, NOIR, (150, 450), (150, 100), 5)  # Poteau
    pygame.draw.line(ecran, NOIR, (150, 100), (250, 100), 5)  # Barre haut
    pygame.draw.line(ecran, NOIR, (250, 100), (250, 150), 5)  # Corde
    
    # Dessiner les parties du corps selon le nombre d'erreurs
    if erreurs >= 1:  # Tête
        pygame.draw.circle(ecran, NOIR, (250, 180), 30, 3)
    if erreurs >= 2:  # Corps
        pygame.draw.line(ecran, NOIR, (250, 210), (250, 300), 5)
    if erreurs >= 3:  # Bras gauche
        pygame.draw.line(ecran, NOIR, (250, 230), (200, 270), 5)
    if erreurs >= 4:  # Bras droit
        pygame.draw.line(ecran, NOIR, (250, 230), (300, 270), 5)
    if erreurs >= 5:  # Jambe gauche
        pygame.draw.line(ecran, NOIR, (250, 300), (220, 370), 5)
    if erreurs >= 6:  # Jambe droite
        pygame.draw.line(ecran, NOIR, (250, 300), (280, 370), 5)

# ========================================
# Fonction principale pour jouer
# ========================================
def jouer_pygame():
    # Initialiser Pygame et créer la fenêtre
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Pendu")
    horloge = pygame.time.Clock()
    
    # Charger un mot au hasard
    mots = charger_mots()
    mot = random.choice(mots).lower()
    
    # Variables du jeu
    lettres_ok = []   # Lettres trouvées
    essais = []       # Lettres essayées
    erreurs = 0       # Nombre d'erreurs
    fini = False      # Partie terminée?
    gagne = False     # Victoire?
    
    # Créer les polices
    grande = pygame.font.Font(None, 70)
    moyenne = pygame.font.Font(None, 45)
    petite = pygame.font.Font(None, 35)
    
    # Boucle principale du jeu
    while True:
        # Gérer les événements
        for event in pygame.event.get():
            # Fermer la fenêtre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Détecter les touches du clavier
            if event.type == pygame.KEYDOWN and not fini:
                if event.unicode.isalpha():
                    lettre = event.unicode.lower()
                    
                    # Si lettre pas encore essayée
                    if lettre not in essais:
                        essais.append(lettre)
                        
                        # Vérifier si la lettre est dans le mot
                        if lettre in mot:
                            lettres_ok.append(lettre)
                            # Vérifier si toutes les lettres sont trouvées
                            if all(l in lettres_ok for l in mot):
                                fini = True
                                gagne = True
                        else:
                            # Mauvaise lettre: ajouter erreur
                            erreurs += 1
                            if erreurs >= 7:
                                fini = True
            
            # ESPACE pour retour menu si partie finie
            # Retour menu si fini
            # Retour menu si fini
            if event.type == pygame.KEYDOWN and fini:
                if event.key == pygame.K_SPACE:
                    if gagne:
                        score = (7 - erreurs) * 100
                        try:
                            sauvegarder_score("Nelly", score)  # CHANGE "Joueur" → "Nelly"
                        except:
                            pass
                    return
        
        # ========================================
        # Dessiner tout à l'écran
        # ========================================
        ecran.fill(BLANC)
        
        # Dessiner le pendu
        dessiner_pendu(ecran, erreurs)
        
        # Afficher le mot avec _ pour lettres non trouvées
        affichage = " ".join([l if l in lettres_ok else "_" for l in mot])
        texte = grande.render(affichage, True, NOIR)
        ecran.blit(texte, (50, 500))
        
        # Afficher les erreurs
        info1 = moyenne.render(f"Erreurs: {erreurs}/7", True, NOIR)
        ecran.blit(info1, (450, 50))
        
        # Afficher les lettres essayées
        info2 = petite.render(f"Lettres: {', '.join(essais)}", True, NOIR)
        ecran.blit(info2, (450, 120))
        
        # Afficher victoire ou défaite si partie finie
        if fini:
            if gagne:
                msg = grande.render("GAGNÉ!", True, VERT)
                scr = moyenne.render(f"Score: {(7 - erreurs) * 100}", True, VERT)
                ecran.blit(scr, (280, 280))
            else:
                msg = grande.render("PERDU!", True, ROUGE)
                sol = moyenne.render(f"Mot: {mot}", True, ROUGE)
                ecran.blit(sol, (220, 280))
            
            ecran.blit(msg, (320, 200))
            aide = petite.render("ESPACE = menu", True, NOIR)
            ecran.blit(aide, (270, 350))
        
        # Mettre à jour l'écran
        pygame.display.flip()
        horloge.tick(60)