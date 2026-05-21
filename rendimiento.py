import numpy as np
import matplotlib.pyplot as plt
import time

from game_of_life import GameOfLife

# 1. Función de benchmark
# ─────────────────────────────────────────────

def benchmark(sizes, repetitions=5, steps_per_run=10):
    """
    Esto mide el tiempo promedio de ejecución por iteración para los distintos tamaños de grilla

    Los parámetros son:
        sizes: es la lista de tamaños N para grillas N*N.
        repetitions: cuántas veces se va a repetir cada prueba con el fin de promediar
        steps_per_run: son los pasos por ejecución en cada repetición

    Regresa:
        n_cells (list): es el número total de celdas N*N por tamaño
        avg_times (list): es el tiempo promedio por iteración (los segundos)
        std_times (list): es la desv. estándar del tiempo por cada iteración
    """
    n_cells    = []
    avg_times  = []
    std_times  = []

    print(f"{'Tamaño':>10}  {'Celdas':>10}  {'t̄ (ms/iter)':>14}  {'σ (ms)':>10}")
    print("-" * 52)

    for N in sizes:
        times_per_iter = [] #Es la lista donde se va a guardar el tiempo promedio por iteración para cada repetición

        for _ in range(repetitions):
            game = GameOfLife(N, N)  #nuevo estado aleatorio cada vez
            start = time.perf_counter() #se encarga de guardar el estado inicial antes de ejecutar
            game.run(steps_per_run) #ejecuta simulación por x cantidad de pasos
            elapsed = time.perf_counter() - start #cuánto duró la simulación
            #tiempo promedio por iteración en esta repetición
            times_per_iter.append(elapsed / steps_per_run)

        mean_t = np.mean(times_per_iter) #tiempo promedio total entre todas las repeticiones
        std_t  = np.std(times_per_iter) #desv. standar con el fin de medir cuanto cambian los tiempos que se obtuvieron

        n_cells.append(N * N) #guarda cant total de celulas de la grilla
        avg_times.append(mean_t) #guarda tiempo promedio
        std_times.append(std_t) #guarda desv. estandar

        print(
            f"{N:>7}×{N:<3}  {N*N:>10,}  "
            f"{mean_t * 1000:>14.4f}  {std_t * 1000:>10.4f}"
        )

    return n_cells, avg_times, std_times #retorna listas con resultados obtenidos


# 2. Curvas teóricas de referencia
# ─────────────────────────────────────────────

def theoretical_curves(n_cells, avg_times):
    """
    Se generan las curvas teóricas escaladas al primer punto de datos para una comparación visual

    Luego retorna un dict {nombre: array de tiempos teóricos}
    """
    n = np.array(n_cells, dtype=float)
    t0 = avg_times[0]  #ancla al primer punto
    n0 = n[0]

    curves = {
        "O(n)":t0 * (n / n0), #el tiempo crece proporcionalmente al tamaño
        "O(n log n)": t0 * (n * np.log(n)) / (n0 * np.log(n0)), #crecimiento + rápido que linea sin embargo - a cuadratico
        "O(n²)": t0 * (n / n0) ** 2, #tiempo aumenta mucho mas rapido 
    }
    return curves

# 3. Gráficas de rendimiento
# ─────────────────────────────────────────────

def plot_performance(n_cells, avg_times, std_times, save_path=None):
    """
    Se generan 2 gráficas:
      (a) Escala lineal: es el tiempo vs las celdas con curvas teóricas
      (b) Escala log-log: para identificar el orden de complejidad
    """
    n   = np.array(n_cells)
    t   = np.array(avg_times) * 1000   #pasar a milisegundos
    std = np.array(std_times) * 1000

    curves = theoretical_curves(n_cells, avg_times)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(
        "Rendimiento empírico del Juego de la Vida de Conway",
        fontsize=14, fontweight="bold"
    )

    #colores para las curvas teóricas
    colors = {"O(n)": "#2ca02c", "O(n log n)": "#ff7f0e", "O(n²)": "#d62728"}

    #(a) Escala lineal-----
    ax = axes[0]

    #grafica los tiempos medidos experimentalmente usando barras de error (desv estandar)
    ax.errorbar(
        n, t, yerr=std,
        fmt="o-", 
        color="#1f77b4", 
        linewidth=2, 
        markersize=6,
        label="Medición empírica", 
        capsize=4, #tamaño de las barras de error
        zorder=5 #prioridad visual
    )

    #grafica curvas teoricas
    for name, curve in curves.items():
        ax.plot(
            n, 
            curve * 1000, 
            linestyle="--",
            color=colors[name], 
            label=name, 
            alpha=0.8
        )
    
    #etiqueta eje x
    ax.set_xlabel(
        "Número de celdas (N×N)", 
        fontsize=11
    )
    #etiqueta eje y
    ax.set_ylabel(
        "Tiempo promedio por iteración (ms)", 
        fontsize=11
    )

    ax.set_title("Escala lineal", fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.4)

    #formato de eje x con separador de miles
    ax.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, _: f"{int(x):,}")
    )

    #(b) Escala log-log----

    #elige el segundo subplot
    ax2 = axes[1]
    ax2.errorbar( #grafica de nuevo los datos experimentales 
        n, t, yerr=std,
        fmt="o-", 
        color="#1f77b4", 
        linewidth=2, 
        markersize=6,
        label="Medición empírica", 
        capsize=4, 
        zorder=5
    )

    #grafica las curvas teoricas
    for name, curve in curves.items():
        ax2.plot(
            n, 
            curve * 1000, 
            linestyle="--",
            color=colors[name], 
            label=name, 
            alpha=0.8
        )
#convierte eje x escala logaritmica
    ax2.set_xscale("log")
#convierte eje y escala logaritmica
    ax2.set_yscale("log")
    ax2.set_xlabel("Número de celdas (N×N) — escala log", fontsize=11)
    ax2.set_ylabel("Tiempo promedio por iteración (ms) — escala log", fontsize=11)
    ax2.set_title("Escala log-log", fontsize=12)
    ax2.legend(fontsize=9)
    ax2.grid(True, which="both", linestyle="--", alpha=0.4)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  Gráfica guardada en: {save_path}")

    return fig

# 4. Análisis de uso de memoria
# ─────────────────────────────────────────────

def memory_usage_table(sizes):
    """
    Lo que hace es estimar el uso de memoria del tablero para distintos tamaños
    (numpy uint8: 1 byte por celda)
    """
    print("\n=== Uso de memoria estimado ===")
    print(f"{'Tamaño':>10}  {'Celdas':>10}  {'Memoria':>10}")
    print("-" * 35)
    for N in sizes:
        cells = N * N
        #2 matrices uint8 (tablero actual + vecinos) ≈ 2 bytes/celda
        mem_bytes = cells * 2
        if mem_bytes < 1024:
            mem_str = f"{mem_bytes} B"
        elif mem_bytes < 1024**2:
            mem_str = f"{mem_bytes/1024:.1f} KB"
        else:
            mem_str = f"{mem_bytes/1024**2:.2f} MB"
        print(f"{N:>7}×{N:<3}  {cells:>10,}  {mem_str:>10}")

# Ejecución principal
# ─────────────────────────────────────────────

if __name__ == "__main__":
    #tamaños de grilla a medir
    SIZES = [32, 64, 128, 256, 512, 1024]

    print("=" * 55)
    print("  Benchmark: Juego de la Vida de Conway")
    print("=" * 55)
    print(f"  Grillas: {SIZES}")
    print(f"  Repeticiones por tamaño: 5")
    print(f"  Pasos por repetición:    10")
    print("=" * 55 + "\n")

    #ejecutar benchmark
    n_cells, avg_times, std_times = benchmark(
        SIZES, repetitions=5, steps_per_run=10
    )

    #tabla de memoria
    memory_usage_table(SIZES)

    #gráficas
    print("\nSe están generando las gráficas de rendimiento")
    fig = plot_performance(
        n_cells, avg_times, std_times,
        save_path="output_rendimiento.png"
    )
    plt.close(fig)

    print("\Finalizado")
