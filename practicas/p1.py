"""PRACTICA 1: 28-01-2026
Instrucciones:
- Modifica el nombre de archivo para que comience por tus apellidos (ej. HernandezCorbato_p1.py)
- Trabaja en las funciones "segmentos_se_cortan" (línea 44), "punto_en_poligono" (línea 49)
- Para comprobar su funcionamiento ve al final del código y ejecuta la comprobación correspondiente
- Sube el código .py a la tarea del CV al final de la clase
"""

import random
import math
import numpy as np
import matplotlib.pyplot as plt
from gcom import ERROR
from gcom import Punto
from gcom import orient
from gcom import alineados
import gcom


def punto_en_segmento(p: Punto, s:list[Punto])->bool:
    s1,s2 = s

    if orient(s1,s2,p) != 0:
        return False
    
    return min(s1.x,s2.x) <= p.x and p.x <= max(s1.x,s2.x) and min(s1.y,s2.y) <= p.y and p.y <= max(s1.y,s2.y)


def segmentos_se_cortan(s: list[Punto], t: list[Punto]) -> bool:
    """
    Input: s, t son listas con dos puntos, los extremos de los segmentos s y t.

    Output: True/False decidiendo si s y t se cortan (incluyendo solaparse o cortarse en un extremo)
    """
    s1,s2 = s[0],s[1]
    t1,t2 = t[0],t[1]

    o1 = orient(s1,s2,t1) #lado de t1 respecto de s
    o2 = orient(s1,s2,t2) #lado t2 respecto de s
    o3 = orient(t1,t2,s1) #lado s1 respecto de t
    o4 = orient(t1,t2,s2) #lado s2 respecto de t


    if o1 != 0 and o2 != 0 and o3 != 0 and o4 != 0: #No colineales

        if o1*o2 < 0 and o3*o4 < 0: #equivalente a o1 != o2 and o3 != o4
            return True
        else:
            return False

    if o1 == 0 and punto_en_segmento(t1,s):
        return True
    
    if o2 == 0 and punto_en_segmento(t2,s):
        return True
    
    if o3 == 0 and punto_en_segmento(s1,t):
        return True
    if o4 == 0 and punto_en_segmento(s2,t):
        return True
    

    return False

def punto_en_poligono(q: Punto, pol: list[Punto]) -> bool:
    """
    Input: q es un punto, pol es una lista de puntos que, en ese orden, son los vértices de un polígono (simple)
    
    Output: True/False decidiendo si q está dentro de pol (incluyendo la frontera)
    """

    contador = 0 #num veces interseca con un lado

    maxcoord = max(p.x for p in pol)
    t = [q, Punto(maxcoord + 1, random.uniform(-1, 1))]
      # El segmento acaba en un punto cuya coordenada x es mayor que las de los vértices del polígono y su coordenada y es un real aleatorio
    
    for i in range(len(pol)):
        # Nos avisa si se da la improbable situación en que el segmento pasa por un vértice de pol (en cuyo caso no bastaría con contar intersecciones)
        # y empezamos de nuevo
        if alineados(t[0], t[1], pol[i-1]):
            return punto_en_poligono(q, pol)
        
        # Si q está encima de un lado del polígono puede fallar la cuenta de intersecciones pero la función debe devolver True
        if punto_en_segmento(q, [pol[i-1], pol[i]]): return True
        if segmentos_se_cortan([pol[i-1], pol[i]], t):
            contador = contador + 1
    return (contador % 2 == 1) 



def comprueba_segmentos_se_cortan(s = None, t = None, size = 2, entero = False):
    def punto_aleatorio():
        if entero:
            return Punto(random.randint(0, size), random.randint(0, size))
        else:
            return Punto(random.uniform(0, size), random.uniform(0, size))
    if s is None:
        s = [punto_aleatorio(), punto_aleatorio()]
    if t is None:
        t = [punto_aleatorio(), punto_aleatorio()]
    respuesta = segmentos_se_cortan(s, t)
    plt.plot([p.x for p in s], [p.y for p in s], 'blue')
    plt.plot([p.x for p in t], [p.y for p in t], 'red')
    texto = 'Sí se cortan' if respuesta else 'NO se cortan'
    texto = 'Los segmentos ' + texto
    plt.title(texto)
    plt.show()
    return

def comprueba_punto_en_poligono(q = None, pol = None, n_vertices = 12):
    def intersects(p1, p2, p3, p4):
        """Check if line segment (p1,p2) intersects with (p3,p4)."""
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
        
        # Standard line intersection formula
        return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

    def generate_random_polygon(n):
        # 1. Create random points
        points = np.random.rand(n, 2)
        
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
                    
                    if intersects(p1, p2, p3, p4):
                        # 3. Swap the order of points between i+1 and j to uncross
                        points[i+1:j+1] = points[i+1:j+1][::-1]
                        swapped = True
        return points

    # --- Plotting ---
    if pol is None:
        poly_points = generate_random_polygon(n_vertices)
    else:
        poly_points = np.array([[p.x, p.y] for p in pol])
    # Close the polygon for plotting
    plot_data = np.vstack([poly_points, poly_points[0]])

    plt.figure(figsize=(6,6))
    plt.plot(plot_data[:,0], plot_data[:,1], 'ro-')
    plt.fill(plot_data[:,0], plot_data[:,1], alpha=0.2, color='blue')
    
    if q is None: q = Punto(random.uniform(0,1), random.uniform(0,1))
    plt.plot(q.x, q.y, 'bo')
    pol = [Punto(*row) for row in poly_points]
    respuesta = punto_en_poligono(q, pol)
    texto = 'dentro' if respuesta else 'fuera'
    texto = 'El punto está ' + texto
    plt.title(texto)
    plt.show()


comprueba_segmentos_se_cortan()
# Segmentos que se cortan:
# %%
comprueba_segmentos_se_cortan([Punto(0,1), Punto(2,1)], [Punto(1,0), Punto(1,2)])
# Segmentos que se cortan:
# %%
comprueba_segmentos_se_cortan([Punto(0,1), Punto(2,1)], [Punto(0,1), Punto(1,2)])

# comprueba_punto_en_poligono()

# Polígono = cuadrado y punto definido
# pol = [Punto(0,0), Punto(1,0), Punto(1,1), Punto(0,1)]
# q = Punto(0.5, 0.5)
# comprueba_punto_en_poligono(q, pol)

# %%
