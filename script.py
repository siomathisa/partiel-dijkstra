# --- Définition du Graphe et des Coordonnées ---

# [cite_start]Le graphe pondéré de l'exercice [cite: 7-22]
graph = {
    "A": [("B", 4), ("C", 2)],
    "B": [("C", 5), ("D", 10)],
    "C": [("E", 3)],
    "D": [("F", 11)],
    "E": [("D", 4)],
    "F": []
}

# [cite_start]Coordonnées cartésiennes (x, y) pour l'heuristique A* [cite: 28]
# Ces coordonnées sont hypothétiques car non fournies.
city_coordinates = {
    "A": (0, 0),
    "B": (3, 1),
    "C": (1, 3),
    "E": (3, 5),
    "D": (6, 4),
    "F": (10, 0)
}

# --- Fonction Utile (Partagée) ---

def get_path_from_predecessors(predecessors, start_node, end_node):
    """
    Reconstruit le chemin final en remontant le dictionnaire 'predecessors'
    depuis le nœud d'arrivée jusqu'au nœud de départ.
    """
    path = []
    current = end_node
    
    # Gestion du cas où l'arrivée n'est pas atteignable
    if end_node not in predecessors and start_node != end_node:
        if start_node in predecessors or start_node == end_node:
             if start_node == end_node:
                 path.append(start_node)
                 return path
        return None # Aucun chemin trouvé

    while current is not None:
        path.append(current)
        current = predecessors.get(current) # Remonte au prédécesseur
    
    path.reverse() # Inverse la liste pour avoir [départ -> ... -> arrivée]
    
    if path and path[0] == start_node:
        return path
    else:
        return None

# --- Algorithme 1: Dijkstra ---

def dijkstra(graph, start_node):
    """
    Implémentation de l'algorithme de Dijkstra.
    Calcule les distances les plus courtes depuis 'start_node' vers tous les autres.
    Utilise une recherche linéaire (O(N)) pour trouver le prochain nœud
    au lieu d'une file de priorité (O(log N)).
    """
    # Initialisation des distances à l'infini
    distances = {node: float('inf') for node in graph}
    # Dictionnaire pour la reconstruction du chemin
    predecessors = {node: None for node in graph}
    
    # Utilisation d'une liste pour stocker les nœuds visités (le "closed set")
    visited = [] 
    
    # Distance du départ à lui-même est 0
    distances[start_node] = 0

    # La boucle principale s'exécute N fois (N = nombre de nœuds)
    for _ in range(len(graph)):
        
        # --- Recherche du nœud non-visité avec la plus petite distance ---
        # Remplace l'extraction d'une file de priorité min-heap.
        current_node = None
        smallest_distance = float('inf')
        
        for node in distances:
            # Si le nœud n'est pas visité et a une distance plus faible
            if node not in visited and distances[node] < smallest_distance:
                smallest_distance = distances[node]
                current_node = node
        # --- Fin de la recherche ---

        # Si 'current_node' est None, les nœuds restants sont inatteignables
        if current_node is None:
            break
            
        # Ajoute le nœud sélectionné à la liste des visités
        visited.append(current_node)
        
        # Étape de relaxation des arêtes
        for neighbor, weight in graph[current_node]:
            new_distance = distances[current_node] + weight
            
            # Si un chemin plus court est trouvé vers le voisin
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance # Mise à jour de la distance
                predecessors[neighbor] = current_node # Mise à jour du chemin
        
    return distances, predecessors

# --- Algorithme 2: A* (A-Star) ---

def heuristic_distance(node, target):
    """
    [cite_start]Calcule l'heuristique (h(n)) : la distance euclidienne [cite: 28]
    entre le nœud 'node' et la cible 'target'.
    """
    x1, y1 = city_coordinates[node]
    x2, y2 = city_coordinates[target]
    # Formule : sqrt((x2-x1)^2 + (y2-y1)^2)
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def a_star(graph, start_node, end_node):
    """
    Implémentation de l'algorithme A*.
    Utilise une liste simple pour l'open list (nœuds à évaluer)
    et une recherche linéaire pour trouver le meilleur f_score.
    """
    
    # Initialisation de l'open list
    nodes_to_check = [start_node] 
    
    predecessors = {}
    
    # g(n): coût réel du départ à 'n'
    g_scores = {node: float('inf') for node in graph}
    g_scores[start_node] = 0
    
    # f(n) = g(n) + h(n): coût total estimé
    f_scores = {node: float('inf') for node in graph}
    f_scores[start_node] = heuristic_distance(start_node, end_node)

    # Tant que l'open list n'est pas vide
    while len(nodes_to_check) > 0:
        
        # --- Recherche du nœud dans l'open list avec le f_score le plus bas ---
        # Remplace l'extraction d'une file de priorité.
        current_node = None
        best_f_score = float('inf')
        
        for node in nodes_to_check:
            if f_scores[node] < best_f_score:
                best_f_score = f_scores[node]
                current_node = node
        # --- Fin de la recherche ---

        # Si la cible est atteinte, reconstruire le chemin et retourner
        if current_node == end_node:
            path = []
            current = end_node
            while current is not None:
                 path.append(current)
                 current = predecessors.get(current)
                 if current == start_node:
                     path.append(start_node)
                     break
            path.reverse()
            
            if path and path[0] == start_node:
                 return path, g_scores[end_node]
            elif start_node == end_node:
                 return [start_node], 0

        # Retrait du nœud actuel de l'open list (équivalent à 'closed set')
        nodes_to_check.remove(current_node)
        
        # Étape de relaxation des voisins
        for neighbor, weight in graph[current_node]:
            new_g_score = g_scores[current_node] + weight
            
            # Si un meilleur chemin (g_score) est trouvé vers ce voisin
            if new_g_score < g_scores[neighbor]:
                predecessors[neighbor] = current_node
                g_scores[neighbor] = new_g_score
                f_scores[neighbor] = new_g_score + heuristic_distance(neighbor, end_node)
                
                # Ajout du voisin à l'open list s'il n'y est pas déjà
                if neighbor not in nodes_to_check:
                    nodes_to_check.append(neighbor)
                    
    return None, float('inf') # Aucun chemin trouvé

# --- Algorithme 3: Trouver Tous les Chemins (DFS) ---

def find_all_paths_recursive(graph, end_node, current_path_with_costs, all_paths_list):
    """
    Fonction récursive (basée sur le parcours en profondeur / DFS)
    pour trouver tous les chemins simples de 'start_node' à 'end_node'.
    """
    
    # Extrait le nœud et le coût actuels
    current_node, current_cost = current_path_with_costs[-1]

    # Condition de base : la cible est atteinte
    if current_node == end_node:
        all_paths_list.append(current_path_with_costs) # Ajoute le chemin trouvé
        return # Arrête cette branche de récursion

    # Exploration des voisins
    for neighbor, weight in graph[current_node]:
        
        # --- Vérification anti-cycle ---
        # S'assure que le voisin n'est pas déjà dans le chemin actuel
        # pour éviter les boucles infinies.
        is_visited_in_this_path = False
        for node, cost in current_path_with_costs:
            if node == neighbor:
                is_visited_in_this_path = True
                break
        # --- Fin de la vérification ---
        
        # Si le voisin n'est pas dans le chemin, continuer l'exploration récursive
        if not is_visited_in_this_path:
            new_cost = current_cost + weight
            # Crée une *nouvelle* liste pour le chemin de la branche récursive
            new_path = current_path_with_costs + [(neighbor, new_cost)]
            find_all_paths_recursive(graph, end_node, new_path, all_paths_list)

def find_all_paths(graph, start_node, end_node):
    """Fonction principale qui initialise et lance la recherche de tous les chemins."""
    all_paths_list = [] # Liste pour stocker les résultats
    start_path = [(start_node, 0)] # Chemin initial (nœud de départ, coût 0)
    find_all_paths_recursive(graph, end_node, start_path, all_paths_list)
    return all_paths_list

# --- Fonction d'Input ---

def get_valid_city_input(prompt_message):
    """Demande à l'utilisateur une ville et vérifie sa validité."""
    valid_cities = list(graph.keys())
    while True:
        city = input(prompt_message).upper()
        if city in valid_cities:
            return city
        else:
            print(f"Erreur : '{city}' n'est pas une ville valide. Villes valides : {', '.join(valid_cities)}")

# --- Exécution Principale (Sans Menu) ---

print("--- Comparaison des Algorithmes de Recherche ---")
print(f"Villes disponibles : {', '.join(graph.keys())}")
print("-" * 40)

# 1. Demander les villes une seule fois
start_city = get_valid_city_input("Entrez la ville de DÉPART (ex: A) : ")
end_city = get_valid_city_input("Entrez la ville d'ARRIVÉE (ex: F) : ")
print("=" * 40)

# 2. Exécuter Dijkstra
print(f"--- 1. Résultat Dijkstra (Chemin le plus court) ---")
distances, path_tracker = dijkstra(graph, start_city)
path_dijkstra = get_path_from_predecessors(path_tracker, start_city, end_city)
cost_dijkstra = distances.get(end_city, float('inf'))

if path_dijkstra:
    print(f"Chemin trouvé de {start_city} à {end_city} (Coût: {cost_dijkstra}):")
    print(f"  {' -> '.join(path_dijkstra)}")
else:
    print(f"Aucun chemin trouvé de {start_city} à {end_city}.")

print("\n" + "=" * 40)

# 3. Exécuter A*
print(f"--- 2. Résultat A* (Chemin le plus court) ---")
path_astar, cost_astar = a_star(graph, start_city, end_city)

if path_astar:
    print(f"Chemin trouvé de {start_city} à {end_city} (Coût: {cost_astar}):")
    print(f"  {' -> '.join(path_astar)}")
else:
    print(f"Aucun chemin trouvé de {start_city} à {end_city}.")

print("\n" + "=" * 40)

# 4. Exécuter la recherche de tous les chemins
print(f"--- 3. Résultat DFS (Tous les chemins possibles) ---")
all_paths = find_all_paths(graph, start_city, end_city)

if not all_paths:
    print(f"Aucun chemin trouvé de {start_city} à {end_city}.")
else:
    print(f"--- {len(all_paths)} chemin(s) trouvé(s) de {start_city} à {end_city} ---")
    
    # Trie les chemins par coût total (du moins cher au plus cher)
    all_paths.sort(key=lambda path: path[-1][1]) 
    
    for i, path in enumerate(all_paths):
        total_cost = path[-1][1] # Coût total (dernier élément du chemin)
        print(f"\nChemin #{i+1} (Coût total: {total_cost}):")
        
        # Formatage pour afficher le coût cumulé à chaque étape
        path_steps = [f"{node} (coût: {cost})" for node, cost in path]
        print(f"  {' -> '.join(path_steps)}")