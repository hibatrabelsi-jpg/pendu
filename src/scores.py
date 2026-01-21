# ========================================
# Afficher le tableau des scores
# ========================================
import pygame
import sys

LARGEUR = 800
HAUTEUR = 600
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (70, 130, 180)

# Charger les scores depuis le fichier
def charger_scores():
    try:
        with open('data/scores.txt', 'r') as f:
            lignes = f.readlines()
            scores = []
            for ligne in lignes:
                if ',' in ligne:
                    nom, score = ligne.strip().split(',')
                    scores.append((nom, int(score)))
            # Trier du meilleur au moins bon
            scores.sort(key=lambda x: x[1], reverse=True)
            return scores[:10]  # Top 10
    except:
        return []

# Afficher l'écran des scores
def afficher_scores():
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Scores")
    
    # Polices
    titre_font = pygame.font.Font(None, 70)
    score_font = pygame.font.Font(None, 42)
    info_font = pygame.font.Font(None, 32)
    
    scores = charger_scores()
    
    # Boucle d'affichage
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # ESPACE ou ESC pour retour menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    return
        
        # Dessiner
        ecran.fill(BLANC)
        
        # Titre
        titre = titre_font.render("MEILLEURS SCORES", True, BLEU)
        ecran.blit(titre, (150, 50))
        
        # Afficher les scores
        y = 150
        for i, (nom, score) in enumerate(scores, 1):
            texte = score_font.render(f"{i}. {nom}: {score}", True, NOIR)
            ecran.blit(texte, (200, y))
            y += 50
        
        # Si aucun score
        if not scores:
            texte = score_font.render("Aucun score", True, NOIR)
            ecran.blit(texte, (300, 250))
        
        # Info retour
        info = info_font.render("ESPACE = retour menu", True, NOIR)
        ecran.blit(info, (240, 550))
        
        pygame.display.flip()