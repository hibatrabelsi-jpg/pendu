import tkinter as tk
from tkinter import messagebox, simpledialog
from file_handler import choisir_mot_aleatoire, sauvegarder_score, charger_scores
import winsound
import random

class PenduGraphique:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🎮 JEU DU PENDU - Par Nelly")
        self.window.geometry("850x650")
        self.window.configure(bg='#1a1a2e')
        
        self.mot_secret = ""
        self.lettres_trouvees = []
        self.lettres_ratees = []
        self.erreurs = 0
        self.max_erreurs = 7
        
        self.afficher_menu()
        
    def jouer_son(self, type_son):
        try:
            if type_son == "victoire":
                winsound.Beep(800, 200)
                winsound.Beep(1000, 200)
                winsound.Beep(1200, 300)
            elif type_son == "defaite":
                winsound.Beep(400, 300)
                winsound.Beep(300, 400)
            elif type_son == "correct":
                winsound.Beep(600, 100)
            elif type_son == "erreur":
                winsound.Beep(300, 150)
        except:
            pass
        
    def afficher_menu(self):
        self.clear_window()
        
        canvas = tk.Canvas(self.window, width=850, height=650, 
                          bg='#1a1a2e', highlightthickness=0)
        canvas.pack()
        
        canvas.create_text(425, 100, text="🎮 JEU DU PENDU", 
                          font=("Arial", 48, "bold"), 
                          fill='#16213e')
        canvas.create_text(425, 102, text="🎮 JEU DU PENDU", 
                          font=("Arial", 48, "bold"), 
                          fill='#0f3460')
        canvas.create_text(425, 100, text="🎮 JEU DU PENDU", 
                          font=("Arial", 48, "bold"), 
                          fill='#e94560')
        
        canvas.create_text(425, 180, text="Créé par Nelly", 
                          font=("Arial", 16, "italic"), 
                          fill='#94a1b2')
        
        btn_jouer = tk.Button(self.window, text="▶ JOUER", 
                            font=("Arial", 22, "bold"),
                            bg='#e94560', fg='white', bd=0,
                            width=18, height=2, cursor="hand2",
                            activebackground='#c23854',
                            command=self.nouvelle_partie)
        canvas.create_window(425, 300, window=btn_jouer)
        
        btn_scores = tk.Button(self.window, text="🏆 SCORES", 
                              font=("Arial", 22, "bold"),
                              bg='#0f3460', fg='white', bd=0,
                              width=18, height=2, cursor="hand2",
                              activebackground='#16213e',
                              command=self.afficher_scores)
        canvas.create_window(425, 400, window=btn_scores)
        
        btn_quitter = tk.Button(self.window, text="❌ QUITTER", 
                               font=("Arial", 22, "bold"),
                               bg='#533483', fg='white', bd=0,
                               width=18, height=2, cursor="hand2",
                               activebackground='#3d2862',
                               command=self.window.quit)
        canvas.create_window(425, 500, window=btn_quitter)
        
    def nouvelle_partie(self):
        self.mot_secret = choisir_mot_aleatoire().upper()
        self.lettres_trouvees = []
        self.lettres_ratees = []
        self.erreurs = 0
        self.afficher_jeu()
        
    def afficher_jeu(self):
        self.clear_window()
        
        self.canvas = tk.Canvas(self.window, width=850, height=650, 
                               bg='#1a1a2e', highlightthickness=0)
        self.canvas.pack()
        
        self.canvas.create_rectangle(50, 50, 350, 350, 
                                    fill='white', outline='#e94560', width=3)
        self.dessiner_pendu()
        
        affichage = ' '.join(l if l in self.lettres_trouvees else '_' 
                            for l in self.mot_secret)
        self.canvas.create_text(200, 400, text=affichage,
                              font=("Courier", 36, "bold"),
                              fill='#e94560')
        
        self.canvas.create_text(200, 470, 
                              text=f"Erreurs: {self.erreurs}/{self.max_erreurs}",
                              font=("Arial", 18, "bold"),
                              fill='#ff6b6b' if self.erreurs > 3 else '#94a1b2')
        
        lettres_txt = ' '.join(sorted(self.lettres_trouvees + self.lettres_ratees))
        self.canvas.create_text(425, 520, text=f"Lettres: {lettres_txt}",
                              font=("Arial", 14), fill='#94a1b2')
        
        lettres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        x_start, y_start = 450, 80
        for i, lettre in enumerate(lettres):
            row, col = i // 7, i % 7
            x = x_start + col * 55
            y = y_start + row * 60
            
            if lettre in self.lettres_trouvees:
                couleur = '#27ae60'
            elif lettre in self.lettres_ratees:
                couleur = '#e74c3c'
            else:
                couleur = '#0f3460'
                
            btn = tk.Button(self.window, text=lettre,
                          font=("Arial", 14, "bold"),
                          width=3, height=1, bd=0,
                          bg=couleur, fg='white',
                          cursor="hand2",
                          activebackground='#16213e',
                          command=lambda l=lettre: self.essayer_lettre(l))
            self.canvas.create_window(x, y, window=btn)
            
        btn_menu = tk.Button(self.window, text="↩ MENU",
                           font=("Arial", 14, "bold"),
                           bg='#533483', fg='white', bd=0,
                           width=12, height=1, cursor="hand2",
                           command=self.afficher_menu)
        self.canvas.create_window(650, 600, window=btn_menu)
        
    def essayer_lettre(self, lettre):
        if lettre in self.lettres_trouvees or lettre in self.lettres_ratees:
            return
            
        if lettre in self.mot_secret:
            self.lettres_trouvees.append(lettre)
            self.jouer_son("correct")
            if all(l in self.lettres_trouvees for l in self.mot_secret):
                self.victoire()
                return
        else:
            self.lettres_ratees.append(lettre)
            self.erreurs += 1
            self.jouer_son("erreur")
            if self.erreurs >= self.max_erreurs:
                self.defaite()
                return
                
        self.afficher_jeu()
        
    def dessiner_pendu(self):
        x, y = 200, 100
        
        self.canvas.create_line(80, 320, 200, 320, width=4, fill='#2d3436')
        self.canvas.create_line(140, 320, 140, 100, width=4, fill='#2d3436')
        self.canvas.create_line(140, 100, 230, 100, width=4, fill='#2d3436')
        self.canvas.create_line(230, 100, 230, 130, width=3, fill='#e74c3c')
        
        if self.erreurs >= 1:
            self.canvas.create_oval(210, 130, 250, 170, width=3, outline='#e74c3c')
            self.canvas.create_oval(220, 145, 225, 150, fill='black')
            self.canvas.create_oval(235, 145, 240, 150, fill='black')
            self.canvas.create_arc(220, 150, 240, 160, start=0, extent=-180, width=2)
            
        if self.erreurs >= 2:
            self.canvas.create_line(230, 170, 230, 240, width=3, fill='#e74c3c')
            
        if self.erreurs >= 3:
            self.canvas.create_line(230, 190, 200, 210, width=3, fill='#e74c3c')
            
        if self.erreurs >= 4:
            self.canvas.create_line(230, 190, 260, 210, width=3, fill='#e74c3c')
            
        if self.erreurs >= 5:
            self.canvas.create_line(230, 240, 210, 280, width=3, fill='#e74c3c')
            
        if self.erreurs >= 6:
            self.canvas.create_line(230, 240, 250, 280, width=3, fill='#e74c3c')
            
    def victoire(self):
        self.jouer_son("victoire")
        score = (7 - self.erreurs) * 100
        nom = simpledialog.askstring("🎉 GAGNÉ!", 
                                    f"BRAVO! Score: {score} points\n\nEntre ton nom:")
        if nom:
            sauvegarder_score(nom, score)
        messagebox.showinfo("🎉 VICTOIRE!", 
                          f"Mot: {self.mot_secret}\nScore: {score} points")
        self.afficher_menu()
        
    def defaite(self):
        self.jouer_son("defaite")
        messagebox.showinfo("😢 PERDU!", 
                          f"Le mot était: {self.mot_secret}")
        self.afficher_menu()
        
    def afficher_scores(self):
        self.clear_window()
        
        canvas = tk.Canvas(self.window, width=850, height=650, 
                          bg='#1a1a2e', highlightthickness=0)
        canvas.pack()
        
        canvas.create_text(425, 80, text="🏆 LEADERBOARD", 
                          font=("Arial", 40, "bold"), 
                          fill='#f39c12')
        
        scores = charger_scores()
        y = 160
        if scores:
            for i, (nom, score) in enumerate(scores[:10], 1):
                if i == 1:
                    couleur, medal = '#ffd700', '🥇'
                elif i == 2:
                    couleur, medal = '#c0c0c0', '🥈'
                elif i == 3:
                    couleur, medal = '#cd7f32', '🥉'
                else:
                    couleur, medal = '#94a1b2', f'{i}.'
                    
                canvas.create_text(425, y, 
                                 text=f"{medal} {nom}: {score} points",
                                 font=("Arial", 20, "bold"),
                                 fill=couleur)
                y += 45
        else:
            canvas.create_text(425, 300, 
                             text="Aucun score enregistré!",
                             font=("Arial", 18),
                             fill='#94a1b2')
            
        btn_retour = tk.Button(self.window, text="↩ RETOUR",
                              font=("Arial", 18, "bold"),
                              bg='#0f3460', fg='white', bd=0,
                              width=15, height=2, cursor="hand2",
                              command=self.afficher_menu)
        canvas.create_window(425, 580, window=btn_retour)
        
    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()
            
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    jeu = PenduGraphique()
    jeu.run()