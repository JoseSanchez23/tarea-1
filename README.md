## Tarea 1: Juego de la Vida de Conway

**Curso:** Programación Paralela — LEAD University  
**Profesor:** Johansell Villalobos Cubillo  
**Fecha:** 21/5/26

---

## Descripción

Consiste en la implementación orientada a objetos del autómata celular de Conway en Python, con visualización de patrones clásicos y análisis empírico de rendimiento.

---

## Estructura del proyecto

```
.
├── game_of_life.py      #Clase principal GameOfLife + los patrones predefinidos
├── visualizacion.py     #Generación de animaciones e imágenes
├── rendimiento.py       #Benchmark y gráficas de complejidad empírica
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
- `output_glider_evolucion.png` — la secuencia de fotogramas del Glider
- `output_blinker_evolucion.png` — la secuencia del Blinker
- `output_grid_sizes.png` — la comparación de tamaños de grilla
- `output_glider_animacion.gif` — la animación del Glider

### 3. Reproducir los experimentos de rendimiento

```bash
python rendimiento.py
```

Ejecuta el benchmark sobre grillas de 32×32 a 1024×1024, se imprime la tabla de tiempos y además se genera `output_rendimiento.png` con las gráficas en escala lineal y log-log.

---

## Patrones predefinidos disponibles

| Función          | Patrón   | Tipo               |
|-----------------|----------|--------------------|
| `make_glider()` | Glider   | Nave espacial      |
| `make_blinker()` | Blinker | Oscilador (período 2) |
| `make_toad()`   | Toad     | Oscilador (período 2) |
| `make_block()`  | Block    | Estructura estática |

---

## Notas relevantes:

- El tablero utiliza condiciones de borde toroidales (los extremos se conectan entre sí)
- La implementación usa `numpy` con operaciones vectorizadas para eficiencia
- El conteo de vecinos se hace con `np.roll` sobre los 8 desplazamientos de la vecindad de Moore

---

## Análisis y Discusión de Resultados

### Resultados del benchmark

Las pruebas de rendimiento se ejecutaron variando el tamaño de la grilla desde 32×32 hasta 1024×1024, midiendo el tiempo promedio por iteración con 5 repeticiones cada una:

| Tamaño    | Celdas (n) | t̄ (ms/iter) |
|-----------|------------|-------------|
| 32×32     | 1,024      | 0.1111      |
| 64×64     | 4,096      | 0.1205      |
| 128×128   | 16,384     | 0.1528      |
| 256×256   | 65,536     | 0.2067      |
| 512×512   | 262,144    | 0.5220      |
| 1024×1024 | 1,048,576  | 3.1397      |

### Comportamiento observado

Al analizar los datos, el aumento en el tiempo no es completamente lineal ni tampoco cuadrático. Entre 1,024 y 1,048,576 celdas (un factor de ×1,024 en celdas), el tiempo aumentó de 0.11 ms a 3.14 ms (un factor de alrededor de ×28). Si fuese O(n) puro, anticiparíamos un factor de ×1,024; si fuese O(n²), anticiparíamos un factor de ×1,048,576. Esto indica que la implementación funciona mejor que O(n) en la práctica para tamaños pequeños y medianos, lo que se atribuye a la efectividad de las operaciones vectorizadas de numpy que utilizan instrucciones SIMD del procesador.

En la gráfica log-log se puede notar que la inclinación de la curva empírica tiende a O(n) para grillas grandes a partir de 256×256, lo que valida que el algoritmo crece de manera lineal con respecto al número de celdas cuando el tamaño es lo suficientemente grande como para superar el overhead fijo de Python.

### Escalabilidad en memoria

El uso de memoria se calcula directamente porque cada celda necesita 1 byte (dtype uint8). En la ejecución se conservan 2 matrices a la vez durante el cálculo de vecinos (el tablero actual y la matriz de conteos), por lo tanto, el uso real es cerca de 2 bytes por celda:

| Tamaño    | Memoria aproximada |
|-----------|--------------------|
| 32×32     | 2.0 KB             |
| 128×128   | 32.0 KB            |
| 512×512   | 512.0 KB           |
| 1024×1024 | 2.00 MB            |

La memoria aumenta de manera completamente lineal con la cantidad de celdas, lo que es previsible. Para cuadrículas de hasta 1024×1024, el uso es totalmente controlable (2 MB). Si se intentara escalar a grillas de 16384×16384, el consumo sería de aproximadamente 512 MB, lo cual ya constituiría una restricción real en dispositivos con poca RAM.

### Restricciones/limitaciones y cuellos de botella

La limitación más relevante identificada es el empleo de `np.roll` para el conteo de vecinos. Aunque es práctico y genera código claro, crea 8 copias desplazadas del tablero en cada generación, lo que conlleva un considerable uso de memoria. Para grillas extensas (1024×1024 o más) este traslado de datos se convierte en el verdadero cuello de botella, no el procesamiento en sí.

Otra restricción es que la ejecución es secuencial: utiliza un único núcleo del procesador. Puesto que el cálculo de cada celda es autónomo respecto a las otras (en la misma generación), este problema es naturalmente paralelizable. Una implementación utilizando NumPy + multiprocessing, CuPy (GPU) o Numba podría disminuir notablemente los tiempos en cuadrículas grandes.

### Conclusiones

La ejecución vectorizada utilizando numpy es bastante eficaz para las dimensiones necesarias en la tarea. El algoritmo tiene un escalado aproximadamente lineal O(n) con respecto al número de celdas en grillas grandes, lo que representa el mejor comportamiento teórico posible, puesto que cada celda debe ser evaluada exactamente una vez por cada generación. Las áreas clave para mejorar residen en la gestión de memoria en medio del conteo de vecinos y en la paralelización del cálculo.
