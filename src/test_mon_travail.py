# Test complet de ton travail sans Pygame
from file_handler import charger_mots, choisir_mot_aleatoire, sauvegarder_score, charger_scores

print("=" * 50)
print("🎮 TEST DE TON TRAVAIL - PENDU")
print("=" * 50)

# TEST 1: Charger les mots
print("\n📖 TEST 1: Chargement des mots")
mots = charger_mots()
print(f"✅ {len(mots)} mots chargés")
print(f"Premiers mots: {mots[:5]}")

# TEST 2: Choisir un mot aléatoire
print("\n🎲 TEST 2: Sélection aléatoire")
for i in range(3):
    mot = choisir_mot_aleatoire()
    print(f"  Mot {i+1}: {mot}")

# TEST 3: Sauvegarder des scores
print("\n💾 TEST 3: Sauvegarde de scores")
sauvegarder_score("Nelly", 100)
sauvegarder_score("Nelly", 85)
sauvegarder_score("Nelly", 120)
sauvegarder_score("Marie", 75)
sauvegarder_score("Jean", 90)
print("✅ 5 scores sauvegardés")

# TEST 4: Charger et afficher les scores
print("\n🏆 TEST 4: Leaderboard")
scores = charger_scores()
print(f"Total: {len(scores)} scores")
print("\n--- TOP 10 ---")
for i, (nom, score) in enumerate(scores[:10], 1):
    print(f"{i}. {nom}: {score} points")

# TEST 5: Simuler une partie
print("\n" + "=" * 50)
print("🎯 TEST 5: Simulation d'une partie")
print("=" * 50)

mot_secret = choisir_mot_aleatoire()
print(f"\nMot secret: {mot_secret.upper()}")
print(f"Longueur: {len(mot_secret)} lettres")

# Simuler 3 erreurs
erreurs = 3
vies_restantes = 7 - erreurs
score_final = vies_restantes * 100

print(f"\nErreurs: {erreurs}/7")
print(f"Vies restantes: {vies_restantes}")
print(f"Score calculé: {score_final} points")

# Sauvegarder le score de cette partie
sauvegarder_score("Nelly", score_final)
print(f"\n✅ Score de Nelly ({score_final}) sauvegardé!")

# Afficher le nouveau leaderboard
print("\n🏆 LEADERBOARD FINAL:")
scores = charger_scores()
for i, (nom, score) in enumerate(scores[:5], 1):
    if nom == "Nelly" and score == score_final:
        print(f"👉 {i}. {nom}: {score} points ⭐ NOUVEAU!")
    else:
        print(f"   {i}. {nom}: {score} points")

print("\n" + "=" * 50)
print("✅ TOUS LES TESTS RÉUSSIS!")
print("=" * 50)