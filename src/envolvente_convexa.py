"""
Implementaciones de varios algoritmos que calculan envolventes convexas
"""
from .gcom import *
from itertools import combinations,permutations


def naif1(P: list[Punto]) -> list[Punto]:
    """
    Un punto p está en la frontera si y solo si no está en el interior de ningún triángulo
    cuyos vértices son puntos de P.
    Input: P lista de Puntos
    Output: lista de vértices de la envolvente convexa ordenada angularmente
    Coste total O(n⁵)
    """
    V = P
    triangulos = combinations(P,3)

    for t in triangulos: #n³ iteraciones

        for p in P: #n iteraciones

            if not p in t:
                if punto_en_triangulo(p,list(t)):
                    V.remove(p) #Coste O(n)
    V = ordena_angularmente(V)
    return V


def naif2(P: list[Punto]) -> list[Punto]:
    """
    Segmento [p,q] es un lado de la envolvente convexa si y solo si todos los demás
    puntos están al mismo lado de la recta que pasa por p y q o alineados con ella.
    Input: P lista de Puntos
    Output: lista de vértices de la envolvente convexa ordenada angularmente
    """
    V = []
    aristas = permutations(P,2) #Realizamos permutaciones para que se consideren tanto [p,q] como [q,p]

    for arista in aristas:

        lado = True #Comprueba si todos estan en el mismo lado

        for r in P:
            if not r  in arista:

                p,q = arista
                if orient(p,q,r) == 1:
                    lado = False
                    break

        if lado ==True:
            p,q = arista
            V.append(p)
            V.append(q)

    V = ordena_angularmente(V)
    return V


def grahams_scan(puntos: list[Punto]) -> list[Punto]:
    """
    Input: lista de Puntos
    Output: lista ordenada positivamente de los puntos que componen la envolvente convexa
    """
    if len(puntos) <= 3:
        return puntos

    p_inicial = min(puntos, key=lambda p: (p.y, p.x))

    def angulo(p: Punto) -> float:
        angulo = math.atan2(p.y - p_inicial.y, p.x - p_inicial.x)
        distancia = (p.x - p_inicial.x) ** 2 + (p.y - p_inicial.y) ** 2
        return (angulo, distancia)

    puntos.sort(key=angulo)

    puntos_ = [puntos[0]]

    for i in range(1, len(puntos)):

        while len(puntos_) > 1 and orient(puntos_[-2], puntos_[-1], puntos[i]) == 0:
            puntos_.pop()

        puntos_.append(puntos[i])

    puntos = puntos_

    envolvente = [puntos[0]]
    envolvente.append(puntos[1])  #se añade pero puede eliminarse si queda a la derecha

    for i in range(2, len(puntos)):

        while (len(envolvente) > 1 and orient(envolvente[-2], envolvente[-1], puntos[i]) == -1):
            envolvente.pop()

        envolvente.append(puntos[i])

    return envolvente


    










