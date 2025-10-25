# Partiel - Algorithmie Avancée
## Distance la plus courte entre villes

---

## 📋 Description

Ce projet implémente trois algorithmes de recherche de chemin sur un graphe pondéré représentant un réseau de routes entre des villes :

1. **Dijkstra** - Calcul du chemin le plus court
2. **A*** - Version optimisée avec heuristique euclidienne
3. **DFS** - Recherche de tous les chemins possibles

---

## 🚀 Lancement du programme

Pour exécuter le programme, utilisez la commande suivante dans votre terminal :

```bash
python script.py
```

---

## 📊 Graphe utilisé

Le graphe représente les connexions suivantes entre villes :

```
A → B (4), C (2)
B → C (5), D (10)
C → E (3)
D → F (11)
E → D (4)
F → (fin)
```

---

## 💻 Utilisation

Le programme vous demandera de saisir :
1. Une **ville de départ** (ex: A)
2. Une **ville d'arrivée** (ex: F)

### Exemple d'exécution

```
--- Comparaison des Algorithmes de Recherche ---
Villes disponibles : A, B, C, D, E, F
----------------------------------------
Entrez la ville de DÉPART (ex: A) : A
Entrez la ville d'ARRIVÉE (ex: F) : F
```

---

## 📈 Résultats affichés

Le programme affiche successivement :

### 1. Résultat Dijkstra
- Chemin optimal trouvé
- Coût total du trajet

### 2. Résultat A*
- Chemin optimal avec heuristique euclidienne
- Coût total du trajet

### 3. Résultat DFS
- Liste complète de tous les chemins possibles
- Chemins triés par coût croissant
- Détail du coût cumulé à chaque étape

---

## 🔧 Algorithmes implémentés

### Dijkstra
- Recherche du plus court chemin depuis un nœud source
- Utilise une recherche linéaire au lieu d'une file de priorité
- Garantit le chemin optimal sur graphe sans poids négatifs

### A* (Question bonus)
- Extension de Dijkstra avec heuristique admissible
- Utilise la distance euclidienne pour guider la recherche
- Plus efficace que Dijkstra grâce à l'heuristique

### DFS (Tous les chemins)
- Parcours en profondeur récursif
- Trouve tous les chemins simples possibles
- Évite les cycles avec vérification anti-boucle

---

## 📝 Structure du code

```
djikstra.py
├── Définition du graphe et coordonnées
├── Fonction utilitaire (reconstruction de chemin)
├── Algorithme Dijkstra
├── Algorithme A* avec heuristique
├── Algorithme DFS (tous les chemins)
└── Programme principal
```

---

## 👨‍💻 Auteur

Ruben KABANGA MUYA, Mathis VIDUEIRA et Esdras TSHIALA KABANGU -
Algorithmie avancée

---

## 📌 Notes

- Les coordonnées cartésiennes utilisées pour l'heuristique A* sont hypothétiques
- Le programme gère automatiquement les cas où aucun chemin n'existe
- Validation automatique des entrées utilisateur