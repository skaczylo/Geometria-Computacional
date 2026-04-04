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


def orient(a:Punto, b:Punto, c:Punto):
    """
    Orientación de 3 puntos.
    Si orientacion a la izquierda devuelve -1
    Si coolineares devuelve 0
    Si orientaacion a la derecha devuelve 1
    """
    d = det(a, b, c)
    if abs(d) < ERROR: return 0
    elif d > ERROR: return 1
    else: return -1


def punto_en_triangulo(p: Punto, triangulo: list[Punto]) -> bool:
    """
    Input: p Punto y triangulo lista con 3 Puntos, los vértices del triángulo
    Output: True/False si el punto p está en el interior del triángulo o no   
    """
    orients = []
    for i in range(len(triangulo)):
        orients.append(orient(triangulo[i-1],triangulo[i],p))

    if len(set(orients)) == 1: #Misma orientacion para cada lado
        return True
    
    return False

def punto_en_segmento(p, s):
    """
    p punto, s segmento = lista con dos puntos

    devuelve True si p está dentro del segmento, incluyendo sus extremos
    """

    if not alineados(p, s[0], s[1]):
        return False
    if abs(s[0].x - s[1].x) > ERROR:
        return min(s[0].x, s[1].x) - ERROR <= p.x <= max(s[0].x, s[1].x) + ERROR
    else:
        return min(s[0].y, s[1].y) - ERROR <= p.y <= max(s[0].y, s[1].y) + ERROR
    

def segmentos_se_cortan(s: list[Punto], t: list[Punto]) -> bool:
    """
    Input: s, t son listas con dos puntos, los extremos de los segmentos s y t.
    
    Output: True/False decidiendo si s y t se cortan (incluyendo solaparse o cortarse en un extremo)
    si los cuatro puntos están alineados
    """
    if alineados(s[0], s[1], t[0]) and alineados(s[0], s[1], t[1]):
        return punto_en_segmento(s[0], t) or punto_en_segmento(s[1], t) or punto_en_segmento(t[0], s) or punto_en_segmento(t[1], s)        
    #si tres puntos están alineados (y no los cuatro) devuelve True solo si uno está dentro del otro segmento
    for p in s:
        if alineados(p, t[0], t[1]): return punto_en_segmento(p, t)        
    for p in t:
        if alineados(p, s[0], s[1]): return punto_en_segmento(p, s)        
    #(sabemos que no hay tres alineados) usamos xor = '^' (True ^ False = True, F^T=T T^T=F, F^F=F)
    return (orient(s[0], s[1], t[0]) * orient(s[0], s[1], t[1]) == -1) and (orient(t[0], t[1], s[0]) * orient(t[0], t[1], s[1]) == -1)