# Tarea 1: Juego de la Vida de Conway

**Curso:** Programación Paralela — LEAD University  
**Profesor:** Johansell Villalobos Cubillo  
**Fecha:** 2026-05-20

---

## Descripción

Implementación orientada a objetos del autómata celular de Conway en Python, con visualización de patrones clásicos y análisis empírico de rendimiento.

---

## Estructura del proyecto

```
.
├── game_of_life.py      # Clase principal GameOfLife + patrones predefinidos
├── visualizacion.py     # Generación de animaciones e imágenes
├── rendimiento.py       # Benchmark y gráficas de complejidad empírica
├── README.md
└── outputs/
    ├── output_patrones_clasicos.png
    ├── output_glider_evolucion.png
    ├── output_blinker_evolucion.png
    ├── output_grid_sizes.png
    ├── output_glider_animacion.gif
    └── output_rendimiento.png
```

---

## Requisitos

- Python 3.9+
- numpy
- matplotlib
- pillow (para guardar GIFs)

Instalar dependencias:

```bash
pip install numpy matplotlib pillow
```

---

## Cómo ejecutar

### 1. Usar la clase directamente

```python
from game_of_life import GameOfLife, make_glider

# Tablero aleatorio 50×50
game = GameOfLife(50, 50)
game.run(10)
print(game)

# Glider predefinido
glider = make_glider(30, 30)
glider.step()
estado = glider.get_state()
```

### 2. Generar las visualizaciones

```bash
python visualizacion.py
```

Genera:
- `output_patrones_clasicos.png` — los 4 patrones clásicos en su estado inicial
- `output_glider_evolucion.png` — secuencia de fotogramas del Glider
- `output_blinker_evolucion.png` — secuencia del Blinker
- `output_grid_sizes.png` — comparación de tamaños de grilla
- `output_glider_animacion.gif` — animación del Glider

### 3. Reproducir los experimentos de rendimiento

```bash
python rendimiento.py
```

Ejecuta el benchmark sobre grillas de 32×32 a 1024×1024, imprime la tabla de tiempos y genera `output_rendimiento.png` con las gráficas en escala lineal y log-log.

---

## Patrones predefinidos disponibles

| Función          | Patrón   | Tipo               |
|-----------------|----------|--------------------|
| `make_glider()` | Glider   | Nave espacial      |
| `make_blinker()` | Blinker | Oscilador (período 2) |
| `make_toad()`   | Toad     | Oscilador (período 2) |
| `make_block()`  | Block    | Estructura estática |

---

## Notas

- El tablero usa condiciones de borde toroidales (los extremos se conectan entre sí).
- La implementación usa `numpy` con operaciones vectorizadas para eficiencia.
- El conteo de vecinos se realiza con `np.roll` sobre los 8 desplazamientos de la vecindad de Moore.
