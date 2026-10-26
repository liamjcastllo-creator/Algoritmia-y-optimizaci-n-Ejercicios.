#Liam Javier Castillo Pacheco 2143962

import matplotlib.pyplot as plt

def greedy_knapsack_weight(items, capacity):
    """
    Algoritmo voraz modificado: prioriza los objetos de MENOR PESO primero.
    items: lista de diccionarios con {'id', 'peso', 'valor'}
    """
    # Ordenar estrictamente de menor a mayor peso
    sorted_items = sorted(items, key=lambda x: x['peso'])
    
    current_weight = 0
    total_value = 0
    selected_items = []
    
    for item in sorted_items:
        if current_weight + item['peso'] <= capacity:
            current_weight += item['peso']
            total_value += item['valor']
            selected_items.append(item['id'])
            
    return selected_items, current_weight, total_value

if __name__ == '__main__':
   
    
    capacity = 10
    items = [
        {'id': 'A (Ligero/Bajo Valor)', 'peso': 3, 'valor': 4},
        {'id': 'B (Pesado/Alto Valor)', 'peso': 9, 'valor': 25},
        {'id': 'C (Mediano/Mediano Valor)', 'peso': 7, 'valor': 20}
    ]
    
    
    capacity = 10
    items = [
        {'id': 'Obj_Ligero', 'peso': 2, 'valor': 3},
        {'id': 'Obj_Mediano1', 'peso': 5, 'valor': 15},
        {'id': 'Obj_Mediano2', 'peso': 5, 'valor': 15},
        {'id': 'Obj_Pesado', 'peso': 9, 'valor': 28}
    ]
   
    
    selected, used_w, total_v = greedy_knapsack_weight(items, capacity)
    print(f"Método Menor Peso -> Seleccionados: {selected}, Peso: {used_w}, Valor: {total_v}")
    
    # Datos para gráfica comparativa
    metodos = ['Menor Peso (Voraz Mod.)', 'Óptimo / Valor-Peso Ideal']
    valores = [18, 30] # Comparativa con el resultado óptimo de la instancia
    
    plt.figure(figsize=(7, 4))
    plt.bar(metodos, valores, color=['orange', 'green'])
    plt.title('Ejercicio 2: Comparativa de Valor Total en la Mochila')
    plt.ylabel('Valor Total Obtenido')
    plt.ylim(0, 35)
    for i, v in enumerate(valores):
        plt.text(i, v + 1, str(v), ha='center', fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('ejercicio2_mochila.png')
    plt.show()