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


def ordena_angularmente(puntos: list[Punto],foco) -> list[Punto]:
    # Input: puntos es una lista de Punto
    # Output: lista de puntos ordenada angularmente (según el ángulo desde el origen)
    # Sugerencia: usar una función de comparación auxiliar como la esbozada
    def angulo(p: Punto) -> float:
        return math.atan2(p.y,p.x)
    
    return sorted(puntos,key=angulo)




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



# 1️⃣ Función para generar puntos aleatorios
def generate_random_puntos(num_points, x_range=(-10, 10), y_range=(-10, 10)):
    """
    Genera una lista de objetos Punto con coordenadas aleatorias.
    """
    return [Punto(random.randint(x_range[0], x_range[1]),
                  random.randint(y_range[0], y_range[1]))
            for _ in range(num_points)]

# 2️⃣ Función para graficar puntos y la envolvente convexa
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

# 3️⃣ Ejemplo de uso
if __name__ == "__main__":
    # Generamos un conjunto de 20 puntos aleatorios
    puntos = generate_random_puntos(20, x_range=(-20, 20), y_range=(-20, 20))
    
    # Calculamos la envolvente convexa
    hull = GrahamScan_algorithm(puntos)
    print(len(hull))
    
    # Graficamos
    plot_convex_hull(puntos, hull)














