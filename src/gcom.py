ERROR = 1e-9
import math
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
    

def producto_vectorial(a: Punto, b:Punto):
    """
    Calcula tercera componente del producto vectorial
    """

    return a.x*b.y - a.y*b.x


def det(a:Punto, b:Punto,c:Punto):
    return producto_vectorial(b-a,c-a)

def alineados(a: Punto, b: Punto, c: Punto) -> bool:
    """
    Devuelve True/False si los puntos a, b, c están alineados/no lo están
    """
    #(a,b,c alineados) sii (ab paralelo bc) sii (rectas paralelas) sii (rectas cortan en infinito)

    if abs(det(a,b,c)) < ERROR:
        return True
    
    return False

def ordena_angularmente(puntos: list[Punto]) -> list[Punto]:
    """
    Input: puntos es una lista de Punto
    Output: lista de puntos ordenada angularmente (según el ángulo desde el origen)
    Sugerencia: usar una función de comparación auxiliar como la esbozada
    """
   
    def angulo(p: Punto) -> float:
        return math.atan2(p.y,p.x)
    
    return sorted(puntos,key=angulo) 


def orientacion(a:Punto, b:Punto, c:Punto):
    """
    Orientación de 3 puntos.
    Si orientacion a la izquierda devuelve -1
    Si coolineares devuelve 0
    Si orientaacion a la derecha devuelve 1
    """

    if alineados(a,b,c):
        return 0
    elif det(a,b,c) < 0:
        return -1
    else:
        return 1


def punto_en_triangulo(p: Punto, triangulo: list[Punto]) -> bool:
    """
    Input: p Punto y triangulo lista con 3 Puntos, los vértices del triángulo
    Output: True/False si el punto p está en el interior del triángulo o no   
    """
    orients = []
    for i in range(len(triangulo)):
        orients.append(orientacion(triangulo[i-1],triangulo[i],p))

    if len(set(orients)) == 1: #Misma orientacion para cada lado
        return True
    
    return False