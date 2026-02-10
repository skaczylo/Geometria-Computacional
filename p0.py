"""PRACTICA 0: 21-01-2026
Instrucciones:
- Modifica el nombre de archivo para que comience por tus apellidos (ej. HernandezCorbato_p0.py)
- Trabaja en las funciones "alineados" (línea 25), "ordena_angularmente" (línea 29)
- Para comprobar su funcionamiento ve al final del código y ejecuta la comprobación correspondiente
- Sube el código .py a la tarea del CV al final de la clase
"""
import random
import math
import matplotlib.pyplot as plt
import numpy as np
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


def alineados(a: Punto, b: Punto, c: Punto) -> bool:
    # Devuelve True/False si los puntos a, b, c están alineados/no lo están

    A = np.array([[a.x, a.y,1],[b.x,b.y,1],[c.x,c.y,1]]) #matriz puntos
    det = np.linalg.det(A)

    if(abs(det) < ERROR):
        return True

    return False
    
def ordena_angularmente(puntos: list[Punto]) -> list[Punto]:
    # Input: puntos es una lista de Punto
    # Output: lista de puntos ordenada angularmente (según el ángulo desde el origen)
    # Sugerencia: usar una función de comparación auxiliar como la esbozada

    def angulo(p: Punto) -> float:
        return math.atan2(p.y, p.x) #ata2 devuelve el arcotangente 
    

    return sorted(puntos, key = angulo)

def punto_en_triangulo(p: Punto, triangulo: list[Punto]) -> bool:
    # Input: p Punto y triangulo lista con 3 Puntos, los vértices del triángulo
    # Output: True/False si el punto p está en el interior del triángulo o no    
    return 


def comprueba_alineados(puntos = None):
    if puntos is None:
        puntos = [Punto(random.randint(0,3), random.randint(0,3)) for _ in range(3)]
    color = 'go' if alineados(puntos[0], puntos[1], puntos[2]) else 'ro'
    plt.plot([p.x for p in puntos], [p.y for p in puntos], color)
    plt.show()
    return True

def comprueba_ordena_angularmente(puntos = None):
    if puntos is None:
        puntos = [Punto(random.uniform(-1,1), random.uniform(-1,1)) for _ in range(10)]
    puntos = ordena_angularmente(puntos)
    for i in range(len(puntos)):
        plt.plot([0, puntos[i].x], [0, puntos[i].y], 'blue')
        plt.text(puntos[i].x, puntos[i].y, str(i))
    plt.show()

def comprueba_punto_en_triangulo (p = None, triangulo = None, respuesta_esperada = None):
    if p is None:
        p = Punto(random.uniform(-1,1), random.uniform(-1, 1))
    if triangulo is None:
        triangulo = [Punto(random.uniform(-1,1), random.uniform(-1,1)) for _ in range(3)]  
    if respuesta_esperada is not None:
        while punto_en_triangulo(p, triangulo) != respuesta_esperada:
            p = Punto(random.uniform(-1,1), random.uniform(-1, 1))
    
    respuesta = punto_en_triangulo(p, triangulo)
    
    triangulo = triangulo[:] + triangulo[:1]
    plt.plot([v.x for v in triangulo], [v.y for v in triangulo], 'blue')
    plt.plot(p.x, p.y, 'ro')
    s = 'Dentro' if respuesta else 'Fuera'
    plt.text(p.x, p.y, s)
    plt.show()

comprueba_alineados([Punto(1,1), Punto(2,2), Punto(3,3)])
comprueba_alineados()# prueba con 3 puntos de coordenadas enteras pequeñas al azar
comprueba_ordena_angularmente()
# comprueba_punto_en_triangulo()