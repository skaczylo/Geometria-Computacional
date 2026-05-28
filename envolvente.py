import random
import math
import numpy as np
import matplotlib.pyplot as plt
from src.envolvente_convexa import *
from src.gcom import *
ERROR = 1e-9




# Función para generar puntos aleatorios
def generate_random_puntos(num_points, x_range=(-10, 10), y_range=(-10, 10)):
    """
    Genera una lista de objetos Punto con coordenadas aleatorias.
    """
    return [Punto(random.randint(x_range[0], x_range[1]),
                  random.randint(y_range[0], y_range[1]))
            for _ in range(num_points)]

# Función para graficar puntos y la envolvente convexa
def plot_convex_hull(puntos, hull):
    """
    Dibuja los puntos y la envolvente convexa.
    """
    # Extraer coordenadas de los puntos
    x_p, y_p = zip(*[(p.x, p.y) for p in puntos])
    plt.scatter(x_p, y_p, color='blue', label='Puntos')

    # Extraer coordenadas de la envolvente y cerrar el polígono
    hx, hy = zip(*[(p.x, p.y) for p in hull + [hull[0]]])
    plt.plot(hx, hy, color='red', label='Envolvente Convexa', linewidth=2)

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Envolvente Convexa con Graham Scan")
    plt.legend()
    plt.grid(True)
    plt.show()

puntos = generate_random_puntos(20, x_range=(-20, 20), y_range=(-20, 20))

hull = naif2(puntos)
print(len(hull))
    

plot_convex_hull(puntos, hull)

