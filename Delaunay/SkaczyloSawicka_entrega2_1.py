"""PRACTICA 10 (A ENTREGAR): TRIANGULACIÓN DE DELAUNAY CON ALGORITMO INCREMENTAL
Instrucciones:
- Modifica el nombre de archivo para que comience por tus apellidos (ej. HernandezCorbato_entrega2_1.py)
- Trabaja en las funciones:
    (clase DCEL - otro archivo) localiza, flip, legaliza
    triangulacion_delaunay_polígono_convexo
    triangulacion_delaunay_incremental
- Para comprobar su funcionamiento ve al final del código y ejecuta la comprobación correspondiente
"""

import random
import math
import numpy as np
import matplotlib.pyplot as plt
ERROR = 1e-9

## CAMBIA ESTA INSTRUCCION SEGÚN MODIFIQUES EL NOMBRE DE TU ARCHIVO ####
from SkaczyloSawicka_entrega2_2 import *


def triangulacion_delaunay_poligono_convexo(puntos : list) -> DCEL:
    """"
    # Input: puntos son los vértices de un polígono convexo ordenados en sentido positivo
    # Output: triangulación de Delaunay de puntos almacenada en una DCEL
    """
    # Primero conseguimos que el triangulo puntos[0-1-2] sea no degenerado
    i = 0
    while alineados(puntos[i], puntos[(i + 1) % len(puntos)], puntos[(i + 2) % len(puntos)]): i = i + 1
    puntos = puntos[i:] + puntos[:i]
    # Ahora guardamos en la lista indices la sucesión de vértices para que al ir añadiendo no se formen triángulos degenerados
    j = 2
    while j + 1 < len(puntos) and alineados(puntos[j-1], puntos[j], puntos[j+1]):
        j = j + 1
    indices = list(range(3, j + 1)) + list(range(len(puntos) - 1, j, -1))

    # Inicializamos con el triángulo puntos[0,1,2]
    triangulacion = DCEL(puntos[0:3])
    i, j = len(puntos), 2
    for k in indices:
        """
        # Incorporamos el punto de índice k, se crea el triángulo que lo conecta con los puntos de indices i-j y legalizamos la arista i-j
        # Utiliza el método .añadir_triangulo_exterior de la clase DCEL
        # Después de añadir el triángulo tendrás que comprobar la legalidad de la arista que une puntos[i] y puntos[j]
        # utilizando el método .legaliza de la clase DCEL
        """
        
        """COMPLETA ESTE BUCLE"""
        # Buscamos la arista exterior que une puntos[i] con puntos[j]
        e_base = triangulacion.busca_arista(Arista(puntos[i % len(puntos)], puntos[j]))
        if e_base is None:
            e_base = triangulacion.busca_arista(Arista(puntos[j], puntos[i % len(puntos)]))
            if e_base is not None:
                e_base = e_base.gemela #vas de Vj a Vi pero lac
        triangulacion.añadir_triangulo_exterior(e_base, puntos[k])
        # Legalizamos la arista interior que conecta puntos[i] con puntos[j]
        e_interior = triangulacion.busca_arista(Arista(puntos[i % len(puntos)], puntos[j]))
        if e_interior is None:
            e_interior = triangulacion.busca_arista(Arista(puntos[j], puntos[i % len(puntos)]))
        triangulacion.legaliza(e_interior, puntos[k])

        """sin modificar estas dos últimas líneas"""
        if k == i - 1: i = k
        elif k == j + 1: j = k

    return triangulacion

def triangulacion_delaunay_incremental(puntos : list) -> DCEL:
    """
    # Input: lista con los puntos de la nube
    # Output: una triangulación de Delaunay de la nube de puntos guardada en una DCEL
    """
    n = len(puntos)
    hull = envolvente_convexa(puntos)
    
    # Inicializamos la triangulacipn triangulando la envolvente convexa
    triangulacion = triangulacion_delaunay_poligono_convexo(hull)     
    
    # Incorporamos el resto de puntos uno a uno a la triangulación
    puntos_restantes = set(puntos) - set(hull)
    for p in puntos_restantes:
       
        t = triangulacion.localiza(p) #triagnulo que contiene a p
       
        """ COMPLETA ESTE BUCLE """
        if t is None:
            continue
      
        aristas_t = t.lista_lados()[:] #crea una copia
        triangulacion.divide_triangulo(t, p)
        for e in aristas_t:
            
            e_actual = triangulacion.busca_arista(e) # Buscamos la arista actualizada en la DCEL 
            if e_actual is not None: #caso degenerado
                triangulacion.legaliza(e_actual, p)

    return triangulacion



def genera_nube_puntos(n, entero = False):
    size = 10    
    if entero: puntos = [Punto(random.randint(0, size), random.randint(0, size)) for _ in range(n)]
    else: puntos = [Punto(random.uniform(0, size), random.uniform(0, size)) for _ in range(n)]    
    return list(set(puntos))

def comprueba_triangulacion_nube(puntos):    
    triangulacion = triangulacion_delaunay_incremental(puntos)
    triangulacion.plot()

puntos = genera_nube_puntos(10, False)
comprueba_triangulacion_nube(puntos)

