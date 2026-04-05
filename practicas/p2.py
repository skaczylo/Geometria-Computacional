"""PRACTICA 2: 04-02-2026
Instrucciones:
- Modifica el nombre de archivo para que comience por tus apellidos (ej. HernandezCorbato_p1.py)
- Trabaja en las funciones "puntos_tangencia_poligono" (línea 67), "es_poligono" (línea 75)
- Para comprobar su funcionamiento ve al final del código y ejecuta la comprobación correspondiente
- Sube el código .py a la tarea del CV al final de la clase
"""

import random
import math
import numpy as np
import matplotlib.pyplot as plt
from gcom import *


def puntos_tangencia_poligono(q: Punto, pol: list[Punto]) -> list:
    """Encuentra los dos puntos donde cortan las tangentes desde el Punto q al polígono pol.

    En caso de ambigüedad porque la tangente contenga un lado del polígono, elegimos el vértice más cercano a q"""
    # IMPORTANTE: q está en el semiplano {x < 0} y pol está en el semiplano {x >= 0} 
    # Input: q es un punto, pol es una lista de puntos que, en ese orden, son los vértices de un polígono (simple)
    # Output: lista con 2 Puntos (en cualquier orden)

    def angulo(p: Punto) -> float:
        return math.atan2(p.y-q.y,p.x-q.x)

    puntos = sorted(puntos,key=angulo)

    return [puntos[0],puntos[-1]]        
    
def es_poligono(pol: list[Punto]) -> bool:
    """Decide si una cadena poligonal (sin puntos consecutivos repetidos) es un polígono (simple)
    Input: lista de Puntos

    Output: True o False dependiendo de si es polígono o no
    """
    
    return True


def generate_random_polygon(n):
    # 1. Create random points
    points = [Punto(random.uniform(0,1), random.uniform(0,1)) for _ in range(n)]
    
    # 2. The "Untangling" loop
    swapped = True
    while swapped:
        swapped = False
        for i in range(n):
            for j in range(i + 2, n):
                # Don't check adjacent edges (they share a vertex)
                if i == 0 and j == n - 1: continue
                
                # Define the four points of the two edges we are checking
                p1, p2 = points[i], points[(i + 1) % n]
                p3, p4 = points[j], points[(j + 1) % n]
                
                if segmentos_se_cortan([p1, p2], [p3, p4]):
                    # 3. Swap the order of points between i+1 and j to uncross
                    points[i+1:j+1] = points[i+1:j+1][::-1]
                    swapped = True
    return points

def comprueba_puntos_tangencia_poligono(q = None, pol = None, n_vertices = 12):
    # --- Plotting ---
    if pol is None:
        pol = generate_random_polygon(n_vertices)
    # Close the polygon for plotting
    plot_data_x = [p.x for p in pol]
    plot_data_x.append(pol[0].x)
    plot_data_y = [p.y for p in pol]
    plot_data_y.append(pol[0].y)
    
    plt.figure(figsize=(6,6))
    plt.fill(plot_data_x, plot_data_y, alpha = 0.2, color = 'blue')

    if q is None: q = Punto(random.uniform(-2,-1), random.uniform(-.5,1.5))
    plt.plot(q.x, q.y, 'bo')
    res_tan = puntos_tangencia_poligono(q, pol)
    plt.plot([res_tan[0].x, q.x, res_tan[1].x], [res_tan[0].y, q.y, res_tan[1].y], 'ro-')
    plt.show()

def comprueba_es_poligono(pol = None):
    n_vertices = 10
    if pol is None:
        pol = generate_random_polygon(n_vertices)        
        pol[0], pol[1] = pol[1], pol[0]
        
    plot_data_x = [p.x for p in pol]
    plot_data_x.append(pol[0].x)
    plot_data_y = [p.y for p in pol]
    plot_data_y.append(pol[0].y)
    
    plt.plot(plot_data_x, plot_data_y, 'bo-')
    respuesta = es_poligono(pol)
    texto = 'Sí' if respuesta else 'No'
    texto = texto + ' es polígono'
    plt.title(texto)
    plt.show()

#%%
pol, q = None, None
# pol = [Punto(0,0), Punto(1,0), Punto(1,1), Punto(0,1)]
# q = Punto(-0.5, 0.5)
comprueba_puntos_tangencia_poligono(q, pol)
# comprueba_es_poligono(pol)
# %%
