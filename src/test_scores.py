from file_handler import sauvegarder_score, charger_scores

# Sauvegarder plusieurs scores avec TON nom
print("=== AJOUT DE SCORES DE TEST ===")
sauvegarder_score("Nelly", 85)
sauvegarder_score("Nelly", 120)
sauvegarder_score("Nelly", 95)
sauvegarder_score("Marie", 75)
sauvegarder_score("Jean", 60)

# Charger et afficher
print("\n=== LEADERBOARD ===")
scores = charger_scores()
for i, (nom, score) in enumerate(scores, 1):
    print(f"{i}. {nom}: {score} points")