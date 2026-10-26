import random
import math
import itertools
import matplotlib.pyplot as plt

def calculate_total_distance(route, cities):
    distance = 0
    n = len(route)
    for i in range(n):
        c1 = cities[route[i]]
        c2 = cities[route[(i + 1) % n]]
        distance += math.hypot(c1[0] - c2[0], c1[1] - c2[1])
    return distance

def get_exact_optimal(cities):
    """Calcula el costo óptimo exacto usando fuerza bruta (N=9 es pequeño)."""
    n = len(cities)
    best_cost = float('inf')
    # Fijar el nodo 0 para evitar permutaciones cíclicas repetidas
    other_nodes = list(range(1, n))
    for perm in itertools.permutations(other_nodes):
        route = [0] + list(perm)
        cost = calculate_total_distance(route, cities)
        if cost < best_cost:
            best_cost = cost
    return best_cost

def mst_tsp_approximation(cities):
    """Algoritmo de aproximación basado en MST (Preorder traversal)."""
    n = len(cities)
    # 1. Construir MST usando Prim simple
    visited = [False] * n
    parent = [-1] * n
    key = [float('inf')] * n
    key[0] = 0
    
    for _ in range(n):
        u = min((v for v in range(n) if not visited[v]), key=lambda x: key[x])
        visited[u] = True
        for v in range(n):
            if not visited[v]:
                d = math.hypot(cities[u][0] - cities[v][0], cities[u][1] - cities[v][1])
                if d < key[v]:
                    key[v] = d
                    parent[v] = u
                    
    # Representar MST como lista de adyacencia
    adj = {i: [] for i in range(n)}
    for i in range(1, n):
        adj[parent[i]].append(i)
        adj[i].append(parent[i])
        
    # Recorrido Preorden (Preorder walk)
    tour = []
    def preorder(u):
        tour.append(u)
        for neighbor in adj[u]:
            if neighbor not in tour:
                preorder(neighbor)
    preorder(0)
    
    cost = calculate_total_distance(tour, cities)
    return tour, cost

if __name__ == '__main__':
    random.seed(42)
    ratios = []
    mst_costs = []
    
    print("Ejecutando 100 instancias aleatorias para MST TSP...")
    for _ in range(100):
        # 9 ciudades aleatorias
        cities = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(9)]
        
        opt_cost = get_exact_optimal(cities)
        _, mst_cost = mst_tsp_approximation(cities)
        
        ratio = mst_cost / opt_cost if opt_cost > 0 else 1.0
        ratios.append(ratio)
        mst_costs.append(mst_cost)
        
    # Visualización 1: Histograma de la razón de aproximación
    plt.figure(figsize=(8, 4.5))
    plt.hist(ratios, bins=15, color='teal', edgecolor='black', alpha=0.7)
    plt.axvline(2.0, color='red', linestyle='--', linewidth=2, label='Límite Teórico (2.0)')
    plt.title('Ejercicio 5: Histograma de la Razón de Aproximación (MST / Óptimo)')
    plt.xlabel('Razón de Aproximación ($C_{obtenido} / C_{óptimo}$)')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('ejercicio5_histograma.png', dpi=300, bbox_inches='tight')
    print("Gráfica 1 guardada como 'ejercicio5_histograma.png'")