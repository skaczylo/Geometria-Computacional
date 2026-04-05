import random
import math
import numpy as np
import matplotlib.pyplot as plt
from envolvente_convexa import envolvente_naif
from envolvente_convexa import gift_wrapping
from gcom import *
ERROR = 1e-9


def GrahamScan_algorithm(puntos: list[Punto]) -> list[Punto]:
    """
    Implementacion del algoritmo de Graham Scan para calcular la envolvente convexa
    """
    if len(puntos) <= 3:
        return puntos
    
    #Encontramos punto mínimo: mas abajo y a la izquierda
    p_min = min(puntos, key = lambda p: (p.y,p.x))

    def angulo(p: Punto)->float:
        angulo = math.atan2(p.y- p_min.y,p.x-p_min.x)
        distancia = (p.x-p_min.x) **2 + (p.y- p_min.y) **2
        return  (angulo,distancia)
    
    puntos.sort(key=angulo)

    #Eliminar puntos colineales
    puntos_no_colineales = [puntos[0]]
    for i in range(1,len(puntos)):

        while len(puntos_no_colineales) > 1 and orient(puntos_no_colineales[-2],puntos_no_colineales[-1],puntos[i]) == 0:
            puntos_no_colineales.pop()
        
        puntos_no_colineales.append(puntos[i])

    
    #Envolvente convexa

    puntos = puntos_no_colineales

    envolvente = [puntos[0]]
    envolvente.append(puntos[1]) #Es posible que se elimine

    for i in range(2,len(puntos)):
        
        while(len(envolvente) > 1 and orient(envolvente[-2],envolvente[-1],puntos[i]) == -1):
            envolvente.pop()
        
        envolvente.append(puntos[i])

    return envolvente



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

hull = gift_wrapping(puntos)
print(len(hull))
    

plot_convex_hull(puntos, hull)

