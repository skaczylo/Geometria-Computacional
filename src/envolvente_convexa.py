"""
Implementaciones de varios algoritmos que calculan envolventes convexas
"""
from gcom import *
from itertools import combinations
import matplotlib.pyplot as plt

def envolvente_naif(pol :list[Punto]) ->list[Punto]:
    """
    Un punto p está en la frontera si y solo si no está en el interior de ningun triangulo cuyos vertices son puntos
    del poligono pol de n elementos

    Coste: O(n^4)
    """
    envolvente = set(pol)

    for triangulo in combinations(pol,3): #aprox n^3 iteraciones
        for p in pol: #n iteraciones
            t1,t2,t3 = triangulo
            if p != t1 and p != t2 and p != t3:
                if p in envolvente and punto_en_triangulo(p,triangulo):
                    envolvente.remove(p)

    
    return  ordena_angularmente(envolvente)


def gift_wrapping(pol: list[Punto]) ->list[Punto]:

    """
    Calculamos el primer vertice p0 de la envolvente y determinamos una dirección cualquiera pq.

    El siguiente punto q de la envolvente será aquel que forme el menor ángulo; sin embargo, esto es
    equivalente a coger aquel punto que esté más a la derecha (o la izquierda si se recorrer en sentido horario).

    Coste: O(n*h)
    """

    p0 = min(pol, key=lambda p: (p.y,p.x))

    envolvente = [p0]
    p = p0
    
    while True: #h iteraciones de h es el cardinal de la envolvente

        q  = pol[0] if pol[0] != p else pol[1] #q cualquiera
        for i in pol: #n iteraciones
            if i == p :
                continue
            
            #Al comparar con todos los puntos posibles, el último será siempre el que este más a la dercha
            if orient(p,q,i) == 1: 
                q = i
        

        if q == p0:
            break

        envolvente.append(q)
        p = q
        #plot_convex_hull(pol,envolvente)


        
    return envolvente #ya estan ordenados pues se insertan ordenados


def GrahamScan_algorithm(puntos: list[Punto]) -> list[Punto]:
    """
    Implementacion del algoritmo de Graham Scan para calcular la envolvente convexa

    Coste: O(n*long(n))
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


def divide_y_venceras(pol: list[Punto])->list[Punto]:
    """
    Algoritmo de divide y venceras para calcular la envolvente convexa
    """
    return





