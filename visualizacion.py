import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
from game_of_life import (
    GameOfLife,
    make_glider,
    make_blinker,
    make_toad,
    make_block,
)


# 1. Función genérica de animación
# ─────────────────────────────────────────────

def animate_game(game, steps=50, interval=150, title="Juego de la Vida",
                 save_path=None, cmap="binary"):
    """
    Lo que va a hacer es crear y mostrar una animación del Juego de la Vida

    Los parámetros son:
        game      : la instancia de GameOfLife ya fue inicializada
        steps     : es el número de generaciones a animar.
        interval  : son los milisegundos entre fotogramas.
        title     : el título de la ventana/figura.
        save_path : ruta para guardar el GIF (None = no guarda)
        cmap      : colormap de matplotlib
    """
    #va a cambiar el color de fodo de la ventana y el 'area de dibujo
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")
    #se evidencia el estado incial de la cuadriacula
    img = ax.imshow(
        game.get_state(),
        cmap=cmap,
        interpolation="nearest",
        vmin=0, vmax=1
    )
    ax.set_xticks([]) #ambas esconden los ejes por deducible exonerdo
    ax.set_yticks([])
    title_text = ax.set_title(
        f"{title} — Generacion 0",
        color="white", fontsize=13, pad=10
    )

    def update(frame):
        game.step()
        img.set_data(game.get_state())
        title_text.set_text( #se coloca el titulo original/existecial
            f"{title} — Generacion {game.generation}  "
            f"(vivas: {game.get_live_count()})"
        )
        return [img, title_text]

    ani = animation.FuncAnimation(
        fig, update, frames=steps,
        interval=interval, blit=True, repeat=False
    )

    if save_path:
        ani.save(save_path, writer="pillow", fps=1000 // interval)
        print(f"  Animación guardada en: {save_path}")

    plt.tight_layout()
    return fig, ani

# 2. Procede la secuencia de fotogramas para un patrón
# ─────────────────────────────────────────────

def plot_pattern_evolution(game, n_frames=6, title="Es la evolución del patrón",
                           save_path=None):
    """
    Aqui se evidencia una cuadrícula de fotogramas que ilustra la evolución del patrón

    Parámetros:
        game      : instancia de GameOfLife
        n_frames  : cuántos momentos hay x capturar
        title     : equivale al título de la figura
        save_path : ruta para guardar la imagen
    """
    cols = 3
    rows = (n_frames + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 3, rows * 3))
    fig.suptitle(title, fontsize=15, fontweight="bold", y=1.01)
    fig.patch.set_facecolor("#f7f7f7")

    axes = axes.flatten()

    #Fotograma 0 (estado inicial)
    axes[0].imshow(game.get_state(), cmap="Blues", interpolation="nearest",
                   vmin=0, vmax=1)
    axes[0].set_title(f"Gen {game.generation}", fontsize=10)
    axes[0].axis("off")

    #Fotogramas siguientes
    step_size = max(1, 10 // n_frames)  #va el spacing entre las capturas
    for i in range(1, n_frames):
        game.run(step_size)
        axes[i].imshow(game.get_state(), cmap="Blues", interpolation="nearest",
                       vmin=0, vmax=1)
        axes[i].set_title(f"Gen {game.generation}", fontsize=10)
        axes[i].axis("off")

    #Se ocultan los ejes que sobran
    for j in range(n_frames, len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  Imagen guardada en: {save_path}")

    return fig


# 3. Panel de comparación de patrones clásicos
# ─────────────────────────────────────────────

def plot_classic_patterns(save_path=None):
    """
    Aqui se va a montar los 4 patrones clásicos en su estado inicial en un solo panel
    """
    patterns = {
        "Glider\n(nave espacial)": make_glider(15, 15),
        "Blinker\n(oscilador)":    make_blinker(10, 10),
        "Toad\n(oscilador)":       make_toad(10, 10),
        "Block\n(estructura estática)": make_block(10, 10),
    }

    fig, axes = plt.subplots(1, 4, figsize=(14, 4))
    fig.suptitle("Patrones Clásicos — Estado Inicial",
                 fontsize=14, fontweight="bold")

    for ax, (name, game) in zip(axes, patterns.items()):
        ax.imshow(game.get_state(), cmap="Greens",
                  interpolation="nearest", vmin=0, vmax=1)
        ax.set_title(name, fontsize=10)
        ax.axis("off")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"  Imagen guardada en: {save_path}")

    return fig


# 4. Visualización en los diferentes tamaños de grilla
# ─────────────────────────────────────────────

def plot_grid_sizes(save_path=None):
    """
    Evidencia el estado inicial de grillas de distintos tamaños (aleatorios)
    """
    sizes = [32, 128, 512] #lista que incluye los tamaños de grilla que se van a comparar
    fig, axes = plt.subplots(1, 3, figsize=(15, 5)) #va a crear una figura con 3 gráficos en una sola fila
    
    #OG titulo 
    fig.suptitle("El estado inicial es aleatorio en distintos tamaños de grilla",
                 fontsize=13, fontweight="bold")

    #Recorre cada eje y cada tamaño de grilla
    for ax, size in zip(axes, sizes):
        game = GameOfLife(size, size) #nuevo juego + grilla cuadrada
        ax.imshow(  #estado inicial de la grilla
            game.get_state(), 
            cmap="binary", 
            interpolation="nearest", 
            vmin=0, vmax=1)
        ax.set_title(f"{size}×{size}", fontsize=12) #titulo evidenciando tamaño grilla
        ax.axis("off") #esconde los ejes con el fin de mejorar la visualización. 

    plt.tight_layout() #ajusta espacios gráficos

    if save_path: #en el caso de que se notifique una ruta se guarda la imagen
        plt.savefig(save_path, dpi=120, bbox_inches="tight")
        print(f"  Imagen guardada en: {save_path}")

    return fig

# Ejecución directa: genera todas las imágenes
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("Generando visualizaciones...\n")

    #Este es el panel de los patrones clásicos
    print("1. Panel de patrones clásicos")
    fig1 = plot_classic_patterns(save_path="output_patrones_clasicos.png")
    plt.close(fig1)

    # Evolución del Glider
    print("2. Evolución del Glider (secuencia de fotogramas)")
    glider = make_glider(25, 25)
    fig2 = plot_pattern_evolution(
        glider, n_frames=6, title="Evolución del Glider",
        save_path="output_glider_evolucion.png"
    )
    plt.close(fig2)

    # Evolución del Blinker
    print("3. Evolución del Blinker (oscilador)")
    blinker = make_blinker(12, 12)
    fig3 = plot_pattern_evolution(
        blinker, n_frames=4, title="Evolución del Blinker",
        save_path="output_blinker_evolucion.png"
    )
    plt.close(fig3)

    # Distintos tamaños de grilla
    print("4. Comparación de tamaños de grilla")
    fig4 = plot_grid_sizes(save_path="output_grid_sizes.png")
    plt.close(fig4)

    # Animación del Glider (GIF)
    print("5. Animación Glider (GIF)")
    glider2 = make_glider(30, 30)
    fig5, ani = animate_game(
        glider2, steps=40, interval=120,
        title="Glider", save_path="output_glider_animacion.gif"
    )
    plt.close(fig5)

    print("\nLos archivos generados fueron:")
    print("  output_patrones_clasicos.png")
    print("  output_glider_evolucion.png")
    print("  output_blinker_evolucion.png")
    print("  output_grid_sizes.png")
    print("  output_glider_animacion.gif")