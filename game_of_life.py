import numpy as np
import time


class GameOfLife:
    """
    Esto lo que hace es la implementación del juego de la vida de Conway usando numpy

    En este caso, el tablero es una grilla bidimensional donde cada celda puede estar
    viva (1) o muerta (0). El sistema evoluciona de acuerdo con las cuatro reglas de Conway.
    """

    def __init__(self, rows, cols, initial_state=None):
        """
        Lo que va a hacer es inicializar el tablero del juego

        Los parámetros son los siguientes:
            rows (int): el número de filas de la grilla
            cols (int): el número de columnas de la grilla
            initial_state (np.ndarray, opcional): es el estado inicial del tablero
                En caso de que no se proporcione, se va a generar uno de manera aleatoria
        """
        self.rows = rows
        self.cols = cols
        self.generation = 0  #este es el contador de las generaciones

        if initial_state is not None:
            #Aqui se verifica que el estado inicial posea las dimensiones correctas
            assert initial_state.shape == (rows, cols), (
                f"El estado inicial tiene que tener dimensiones ({rows}, {cols}), "
                f"sin embargo se recibió {initial_state.shape}"
            )
            self.board = initial_state.astype(np.uint8)
        else:
            #Entra el estado aleatorio, donde hay aproximadamente 30% de celdas vivas
            self.board = np.random.choice(
                [0, 1], size=(rows, cols), p=[0.7, 0.3]
            ).astype(np.uint8)

    def step(self):
        """
        En este paso se va a calcular y aplicar una generación en base a las reglas de Conway

        Estas son las reglas:
          1. Superpoblación: celda viva con más de 3 vecinos vivos muere
          2. Soledad: celda viva con menos de 2 vecinos vivos muere
          3. Supervivencia: celda viva con 2 o 3 vecinos vivos permanece viva (sobrevive)
          4. Reproducción: celda muerta con exactamente 3 vecinos vivos se convierte en celda viva (nace)
        """
        #Se cuentan los vecinos vivos usando np.roll (con desplazamientos en los 8 ejes)
        #Lo cual es equivalente a un tablero toroidal ya que los bordes se conectan
        neighbors = self._count_neighbors()

        #Luego se aplican las reglas de Conway con las operaciones vectorizadas
        #Regla 3 supervivencia: estaba viva y sí tiene dos o tres vecinos
        survival = (self.board == 1) & ((neighbors == 2) | (neighbors == 3))
        #Regla 4 reproducción: estaba muerta y posee exactamente tres vecinos
        birth = (self.board == 0) & (neighbors == 3)

        #El nuevo tablero va a combinar las supervivencias y los nacimientos
        self.board = (survival | birth).astype(np.uint8)
        self.generation += 1

    def _count_neighbors(self):
        """
        Lo que esto hace es contar los vecinos vivos de cada celda, para ello usa desplazamientos de numpy
        Va a devolver:
            np.ndarray: Una matriz con el conteo de vecinos vivos por celda
        """
        #Suma los 8 desplazamientos posibles (vecindad de Moore)
        neighbors = np.zeros((self.rows, self.cols), dtype=np.uint8)

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  #no se cuenta esa celda como tal
                #np.roll va a hacer que el desplazamiento sea de forma toroidal
                neighbors += np.roll(np.roll(self.board, dr, axis=0), dc, axis=1)

        return neighbors

    def run(self, steps):
        """
        Se van a ejecutar varias iteraciones del juego
        Parámetros:
            steps (int): Equivale al número de generaciones que se deben simular

        Y se retorna:
            float: Este es el tiempo total de ejecución en segundos
        """
        start = time.perf_counter()
        for _ in range(steps):
            self.step()
        elapsed = time.perf_counter() - start
        return elapsed

    def get_state(self):
        """
        Va a retornar el estado actual del tablero

        Devuelve:
            np.ndarray: Es la copia del tablero actual (filas x cols), valores 0 o 1
        """
        return self.board.copy()

    def get_live_count(self):
        """Retorna el número de celdas vivas en el estado actual"""
        return int(self.board.sum())

    def reset(self, initial_state=None):
        """
        Va a reiniciaf el tablero a un nuevo estado

        Los parámetros:
            initial_state (np.ndarray, opcional): Nuevo estado inicial
                Si no se proporciona, se va a generar uno de manera aleatoria
        """
        self.generation = 0
        if initial_state is not None:
            self.board = initial_state.astype(np.uint8)
        else:
            self.board = np.random.choice(
                [0, 1], size=(self.rows, self.cols), p=[0.7, 0.3]
            ).astype(np.uint8)

    def __repr__(self):
        return (
            f"GameOfLife(rows={self.rows}, cols={self.cols}, "
            f"generation={self.generation}, "
            f"live_cells={self.get_live_count()})"
        )
#─────────────────────────────────────────────
# Patrones clásicos predefinidos

def make_glider(rows=20, cols=20):
    """Se va a crear un tablero con un Glider en la esquina superior izquierda"""
    board = np.zeros((rows, cols), dtype=np.uint8)
    #Este es el patrón del glider (5 celdas)
    glider = np.array([
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1]
    ], dtype=np.uint8)
    board[1:4, 1:4] = glider
    return GameOfLife(rows, cols, initial_state=board)


def make_blinker(rows=10, cols=10):
    """Va a crear un tablero con un Blinker (oscilador de periodo 2) en el centro"""
    board = np.zeros((rows, cols), dtype=np.uint8)
    cx, cy = rows // 2, cols // 2
    board[cx, cy - 1] = 1
    board[cx, cy]     = 1
    board[cx, cy + 1] = 1
    return GameOfLife(rows, cols, initial_state=board)


def make_toad(rows=10, cols=10):
    """CSe va a crear un tablero con un Toad (oscilador de periodo 2)"""
    board = np.zeros((rows, cols), dtype=np.uint8)
    cx, cy = rows // 2, cols // 2
    #Esta es la fila superior
    board[cx,     cy]     = 1
    board[cx,     cy + 1] = 1
    board[cx,     cy + 2] = 1
    #Y esta la fila inferior
    board[cx + 1, cy - 1] = 1
    board[cx + 1, cy]     = 1
    board[cx + 1, cy + 1] = 1
    return GameOfLife(rows, cols, initial_state=board)


def make_block(rows=10, cols=10):
    """Se va a crear un tablero con un Block (estructura estática)"""
    board = np.zeros((rows, cols), dtype=np.uint8)
    cx, cy = rows // 2, cols // 2
    board[cx:cx+2, cy:cy+2] = 1
    return GameOfLife(rows, cols, initial_state=board)


# Prueba cuando se ejecuta el archivo directamente
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("------ Prueba  GameOfLife ------\n")

    #Este es el tablero aleatorio pequeño
    gol = GameOfLife(10, 10)
    print(f"Estado inicial: {gol}")
    print(f"Tablero:\n{gol.get_state()}\n")

    elapsed = gol.run(5)
    print(f"Después de 5 generaciones: {gol}")
    print(f"Tiempo total: {elapsed:.6f} s\n")

    #Se procede a probar el Glider
    glider = make_glider(20, 20)
    print(f"Glider inicial: {glider}")
    glider.run(10)
    print(f"Glider después de 10 generaciones: {glider}")