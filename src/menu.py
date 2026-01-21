import pygame
import sys

# === INITIALISATION ===
pygame.init()

# Constantes
LARGEUR = 800
HAUTEUR = 600
FPS = 60

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (70, 130, 180)
VERT = (60, 179, 113)
ROUGE = (220, 20, 60)

# === CLASSE BOUTON ===
class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, couleur):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur = couleur
        self.couleur_survol = (couleur[0] + 30, couleur[1] + 30, couleur[2] + 30)
    
    def dessiner(self, ecran, police):
        # Vérifier si souris survole
        souris = pygame.mouse.get_pos()
        if self.rect.collidepoint(souris):
            pygame.draw.rect(ecran, self.couleur_survol, self.rect, border_radius=10)
        else:
            pygame.draw.rect(ecran, self.couleur, self.rect, border_radius=10)
        
        # Dessiner le texte
        texte_surface = police.render(self.texte, True, BLANC)
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        ecran.blit(texte_surface, texte_rect)
    
    def est_clique(self, pos):
        return self.rect.collidepoint(pos)

# === FONCTION MENU ===
def menu_principal():
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Jeu du Pendu")
    horloge = pygame.time.Clock()
    
    # Polices
    police_titre = pygame.font.Font(None, 72)
    police_bouton = pygame.font.Font(None, 48)
    
    # Créer les boutons
    bouton_jouer = Bouton(250, 200, 300, 70, "JOUER", VERT)
    bouton_scores = Bouton(250, 300, 300, 70, "SCORES", BLEU)
    bouton_quitter = Bouton(250, 400, 300, 70, "QUITTER", ROUGE)
    
    # Boucle principale
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if bouton_jouer.est_clique(pos):
                    print("Jouer cliqué!")
                    return "jouer"
                
                elif bouton_scores.est_clique(pos):
                    print("Scores cliqué!")
                    return "scores"
                
                elif bouton_quitter.est_clique(pos):
                    pygame.quit()
                    sys.exit()
        
        # Dessiner
        ecran.fill(BLANC)
        
        # Titre
        titre = police_titre.render("JEU DU PENDU", True, NOIR)
        titre_rect = titre.get_rect(center=(LARGEUR // 2, 100))
        ecran.blit(titre, titre_rect)
        
        # Boutons
        bouton_jouer.dessiner(ecran, police_bouton)
        bouton_scores.dessiner(ecran, police_bouton)
        bouton_quitter.dessiner(ecran, police_bouton)
        
        pygame.display.flip()
        horloge.tick(FPS)

# === TEST ===
if __name__ == "__main__":
    choix = menu_principal()
    print(f"Choix: {choix}")