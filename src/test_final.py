# TEST COMPLET DU JEU PENDU
print("=" * 50)
print("🧪 TEST DU JEU DU PENDU")
print("=" * 50)

# Test 1: Import des modules
print("\n✅ TEST 1: Imports")
try:
    from file_handler import charger_mots, choisir_mot_aleatoire, sauvegarder_score, charger_scores
    print("✅ file_handler importé avec succès")
except Exception as e:
    print(f"❌ ERREUR: {e}")
    exit()

# Test 2: Charger les mots
print("\n✅ TEST 2: Chargement des mots")
try:
    mots = charger_mots()
    print(f"✅ {len(mots)} mots chargés")
    print(f"Exemples: {mots[:3]}")
except Exception as e:
    print(f"❌ ERREUR: {e}")

# Test 3: Mot aléatoire
print("\n✅ TEST 3: Sélection aléatoire")
try:
    mot1 = choisir_mot_aleatoire()
    mot2 = choisir_mot_aleatoire()
    print(f"✅ Mot 1: {mot1}")
    print(f"✅ Mot 2: {mot2}")
except Exception as e:
    print(f"❌ ERREUR: {e}")

# Test 4: Sauvegarder score
print("\n✅ TEST 4: Sauvegarde score")
try:
    sauvegarder_score("TEST", 999)
    print("✅ Score sauvegardé")
except Exception as e:
    print(f"❌ ERREUR: {e}")

# Test 5: Charger scores
print("\n✅ TEST 5: Leaderboard")
try:
    scores = charger_scores()
    print(f"✅ {len(scores)} scores trouvés")
    for i, (nom, score) in enumerate(scores[:3], 1):
        print(f"  {i}. {nom}: {score} points")
except Exception as e:
    print(f"❌ ERREUR: {e}")

# Test 6: Lancer le jeu
print("\n✅ TEST 6: Lancement du jeu graphique")
print("Tentative de lancement...")
try:
    import tkinter
    print("✅ Tkinter disponible")
    print("\n🎮 Lance maintenant: python src/pendu_graphique.py")
except:
    print("❌ Tkinter non disponible")

print("\n" + "=" * 50)
print("✅ TESTS TERMINÉS!")
print("=" * 50)