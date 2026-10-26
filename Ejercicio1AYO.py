#Liam Javier Castillo Pacheco 2143962

import time
import random
import multiprocessing
import matplotlib.pyplot as plt

def monte_carlo_pi_part(num_samples):
    """Calcula puntos dentro del círculo en un subconjunto de muestras."""
    inside = 0
    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1.0:
            inside += 1
    return inside

def run_experiment(total_samples, num_processes):
    """Ejecuta la simulación dividiendo las muestras entre los procesos dados."""
    samples_per_process = total_samples // num_processes
    
    start_time = time.time()
    
    if num_processes == 1:
        inside_total = monte_carlo_pi_part(total_samples)
    else:
        with multiprocessing.Pool(processes=num_processes) as pool:
            results = pool.map(monte_carlo_pi_part, [samples_per_process] * num_processes)
            inside_total = sum(results)
            
    end_time = time.time()
    elapsed_time = end_time - start_time
    pi_est = 4 * inside_total / total_samples
    return elapsed_time, pi_est

if __name__ == '__main__':
    TOTAL_SAMPLES = 10_000_000
    process_counts = [1, 2, 4, 8]
    times = []
    
    print("Ejecutando experimentos de aceleración paralela...")
    for p in process_counts:
        t, pi_val = run_experiment(TOTAL_SAMPLES, p)
        times.append(t)
        print(f"Procesos: {p} | Tiempo: {t:.4f}s | Est. Pi: {pi_val:.5f}")
        
    # Cálculo del Speedup: T(1) / T(p)
    baseline_time = times[0]
    speedups = [baseline_time / t for t in times]
    
    # Generación de la gráfica requerida
    plt.figure(figsize=(8, 5))
    plt.plot(process_counts, speedups, marker='o', linestyle='-', color='b', label='Speedup Real')
    plt.plot(process_counts, process_counts, linestyle='--', color='r', label='Speedup Ideal (Lineal)')
    plt.title('Ejercicio 1: Aceleración Paralela (Monte Carlo Pi)')
    plt.xlabel('Número de Procesos')
    plt.ylabel('Aceleración (Speedup)')
    plt.xticks(process_counts)
    plt.grid(True)
    plt.legend()
    plt.savefig('ejercicio1_speedup.png')
    plt.show()