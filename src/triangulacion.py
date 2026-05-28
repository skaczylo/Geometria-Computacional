"""Implementación algoritmos de triangulación"""

from gcom import *
from utils import generate_random_polygon, plot_triangulacion

def corte_orejas(poligono):
    """
    Algoritmo de triangulación por Corte de Orejas.
    Se asume que el polígono de entrada está en orden antihorario y es simple.
    Debe devolver una lista de triángulos, donde cada triángulo es una lista de 3 Puntos.
    """
    
    if len(poligono) < 3:
        return []
    
    if len(poligono) == 3:
        return [poligono]
    
    triangulos = []
    
    # Hacemos una copia del polígono para ir eliminando vértices sin afectar la entrada original
    P = poligono[:]
    
    while len(P) > 3:
        n = len(P)
        
        for i in range(n):
            prev_i = (i - 1) % n  
            next_i = (i + 1) % n  
            
            v_prev = P[prev_i]
            v_curr = P[i]
            v_next = P[next_i]
            
            #vertice convexo sii girar a la izq
            if orient(v_prev, v_curr, v_next) ==1:
                
                triangulo_vacio = True
                for k in range(n):
                    if k in (prev_i, i, next_i):
                        continue 
                    
                    vk = P[k]
                    if punto_en_triangulo(vk, [v_prev, v_curr, v_next]):
                        triangulo_vacio = False
                        break # Si hay un punto dentro, no es oreja. Dejamos de buscar.
                
                # es una oreja
                if triangulo_vacio:
                    
                    triangulos.append([v_prev, v_curr, v_next])
                    P.pop(i)
                    break 
        
    # Al salir del bucle while (cuando len(P) == 3), quedan exactamente los 3 vértices del último triángulo
    if len(P) == 3:
        triangulos.append([P[0], P[1], P[2]])

    return triangulos

    


   
if __name__ == "__main__":

# Código de comprobación
    poligono_aleatorio = generate_random_polygon(12)
    triangulos_resultantes = corte_orejas(poligono_aleatorio)

    
    print(f"Vértices del polígono: {len(poligono_aleatorio)}")
    print(f"Triángulos generados: {len(triangulos_resultantes)}")

    plot_triangulacion(poligono_aleatorio, triangulos_resultantes, title="Triangulación de Polígono Aleatorio")
