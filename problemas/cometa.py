"""MODELO DE EJERCICIO DE EXAMEN PRACTICO 25/26
- Función cometa, línea 112
- Puedes usar toda la librería GCOM incluida en el archivo
- Zona de pruebas, línea 160
"""

import random
import math
import numpy as np
import matplotlib.pyplot as plt
ERROR = 1e-9

class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    # se puede definir un punto con coordenadas dadas así: p = Punto(2, 3)
    def __repr__(self):
        return "({0},{1})".format(self.x, self.y)  
    def __add__(self, other):
        return Punto(self.x + other.x, self.y + other.y)  
    def __sub__(self, other):
        return Punto(self.x - other.x, self.y - other.y)
    def __eq__(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) < ERROR
    def __hash__(self):
        return 1000000000*int(self.x) + 1000*int(self.y)


def prod_vect(u, v):
    return u.x * v.y - u.y * v.x
def det(a, b, c):
    return prod_vect(b - a, c - a)

def alineados(a: Punto, b: Punto, c: Punto) -> bool:
    # Devuelve True/False si los puntos a, b, c están alineados/no lo están
    return abs(det(a, b, c)) < ERROR

def orient(a: Punto, b: Punto, c: Punto) -> int:
    # 1/0/-1 si c a la izquierda/alineado/a la derecha de ab    
    d = det(a, b, c)
    if abs(d) < ERROR: return 0
    elif d > ERROR: return 1
    else: return -1

def ordena_angularmente(puntos: list[Punto]) -> list[Punto]:
    # Input: puntos es una lista de Punto
    # Output: lista de puntos ordenada angularmente (según el ángulo desde el origen)
    # Sugerencia: usar una función de comparación auxiliar como la esbozada
    def angulo(p: Punto) -> float:
        return math.atan2(p.y, p.x)
    return sorted(puntos, key = angulo)

def punto_en_triangulo(p: Punto, triangulo: list[Punto]) -> bool:
    # Input: p Punto y triangulo lista con 3 Puntos, los vértices del triángulo, que suponemos no alineados
    # Output: True/False si el punto p está en el interior del triángulo o no
    if orient(triangulo[0], triangulo[1], triangulo[2]) == -1:
        return punto_en_triangulo(p, triangulo[::-1])
    for i in range(len(triangulo)):
        if orient(triangulo[i-1], triangulo[i], p) != 1:
            return False
    return True

def punto_en_segmento(p, s):
    #p punto, s segmento = lista con dos puntos
    #devuelve True si p está dentro del segmento, incluyendo sus extremos
    if not alineados(p, s[0], s[1]):
        return False
    if abs(s[0].x - s[1].x) > ERROR:
        return min(s[0].x, s[1].x) - ERROR <= p.x <= max(s[0].x, s[1].x) + ERROR
    else:
        return min(s[0].y, s[1].y) - ERROR <= p.y <= max(s[0].y, s[1].y) + ERROR
    
def segmentos_se_cortan(s: list[Punto], t: list[Punto]) -> bool:
    # Input: s, t son listas con dos puntos, los extremos de los segmentos s y t.
    # Output: True/False decidiendo si s y t se cortan (incluyendo solaparse o cortarse en un extremo)
    # si los cuatro puntos están alineados
    if alineados(s[0], s[1], t[0]) and alineados(s[0], s[1], t[1]):
        return punto_en_segmento(s[0], t) or punto_en_segmento(s[1], t) or punto_en_segmento(t[0], s) or punto_en_segmento(t[1], s)        
    #si tres puntos están alineados (y no los cuatro) devuelve True solo si uno está dentro del otro segmento
    for p in s:
        if alineados(p, t[0], t[1]): return punto_en_segmento(p, t)        
    for p in t:
        if alineados(p, s[0], s[1]): return punto_en_segmento(p, s)        
    #(sabemos que no hay tres alineados) usamos xor = '^' (True ^ False = True, F^T=T T^T=F, F^F=F)
    return (orient(s[0], s[1], t[0]) * orient(s[0], s[1], t[1]) == -1) and (orient(t[0], t[1], s[0]) * orient(t[0], t[1], s[1]) == -1)

def punto_en_poligono(q: Punto, pol: list[Punto]) -> bool:
    # Input: q es un punto, pol es una lista de puntos que, en ese orden, son los vértices de un polígono (simple)
    # Output: True/False decidiendo si q está dentro de pol (incluyendo la frontera)
    # Contamos el número de cortes del polígono con un segmento que comienza en q y acaba fuera del polígono.
    # Si es par q está fuera y si es impar está dentro del polígono
    maxcoord = max(p.x for p in pol)
    # El segmento acaba en un punto cuya coordenada x es mayor que las de los vértices del polígono y su coordenada y es un real aleatorio
    t = [q, Punto(maxcoord + 1, random.uniform(-1, 1))]
    count = 0
    n = len(pol)
    for i in range(n):
        # Nos avisa si se da la improbable situación en que el segmento pasa por un vértice de pol (en cuyo no bastaría con contar intersecciones)
        # y empezamos de nuevo
        if alineados(t[0], t[1], pol[i]):
            # print(t[0], t[1], pol[i], "El rayo pasa por un vértice")
            return punto_en_poligono(q, pol)
        # Si q está encima de un lado del polígono puede fallar la cuenta de intersecciones pero la función debe devolver True
        if punto_en_segmento(q, [pol[i], pol[(i+1)%n]]): return True
        if segmentos_se_cortan([pol[i], pol[(i+1)%n]], t):
            count = count + 1
    return (count % 2 == 1)    

################################ FIN LIBRERÍA GCOM ##########################################


def cometa(pol: list[Punto]) -> list[Punto]:

    puntos_cometa = []

    n = len(pol)

    if n <=5:
        return None
    
    k = 0
    puntos_cometa.append(pol[0]) #v_i0
    puntos_cometa.append(pol[1]) #v_i1
    puntos_cometa.append(pol[2]) #v_i2

    def es_diagonal(diagonal:list[Punto])->bool:

        v_j, v_i = diagonal

        for k in range(n):
            e1 = pol[k]
            e2 = pol[(k+1)%n]
            arista = [e1,e2]


            if v_j == e1 or v_j == e2 or v_i == e1 or v_i == e2:
                continue

            if segmentos_se_cortan(diagonal,arista):
                return False
            
            #Diagonal no corta => dentro o fuera poligono

        m = Punto((v_j.x+v_i.x)/2,(v_j.y+v_i.y)/2)

        if punto_en_poligono(m,pol) : return True


        return False


    for i in range(3,len(pol)):

        v_j= pol[(i+1)%n]

        diagonal1 = [v_j,puntos_cometa[2]]
        diagonal2 = [v_j,puntos_cometa[0]]


        if es_diagonal(diagonal1) and es_diagonal(diagonal2):
            puntos_cometa.append(v_j)

            #Comprobar orientacion
            area = 0
            for k in range(3):
                area += prod_vect(puntos_cometa[k], puntos_cometa[k+1])

            if area > 0:
                return puntos_cometa
            puntos_cometa.pop()
        
        #Desplazar cometa
        puntos_cometa[0] = puntos_cometa[1]
        puntos_cometa[1] = puntos_cometa[2]
        puntos_cometa[2] = pol[i]


    if len(puntos_cometa) == 3:
        puntos_cometa = None

    
    return puntos_cometa


def generate_random_polygon(n, entero = False):
    # 1. Create random points
    if entero:
        points = list(set([Punto(random.randint(0,10), random.randint(0,10)) for _ in range(n)]))
        n = len(points)
    else: points = [Punto(random.uniform(0,1), random.uniform(0,1)) for _ in range(n)]
    
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
    area = 0
    for i in range(n):
        area += prod_vect(points[i], points[(i + 1) % n])
    if area < 0: return points[::-1]
    else: return points
    
def comprueba_cometa(pol, n, entero):
    if pol is None: pol = generate_random_polygon(n, entero)
    puntos_cometa = cometa(pol)  
    
    #dibuja el polígono (en azul) y encima la cometa (en rojo)
    pol.append(pol[0])
    plt.plot([p.x for p in pol], [p.y for p in pol], 'bo-')
    #plt.show()
    if puntos_cometa is not None:
        puntos_cometa.append(puntos_cometa[0])
        plt.plot([p.x for p in puntos_cometa], [p.y for p in puntos_cometa], 'ro-')
    plt.show() 

# ZONA DE PRUEBAS
# n es el tamaño del polígono y entero un booleano (False -> coord. reales, True -> coord. enteras)
pol, n, entero = None, 10, False
comprueba_cometa(pol, n, entero)