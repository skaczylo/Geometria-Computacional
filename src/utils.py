import random
import math
import matplotlib.pyplot as plt
from gcom import Punto

def generate_random_puntos(num_points, x_range=(-20, 20), y_range=(-20, 20)):
    """Genera una lista de objetos Punto con coordenadas aleatorias."""
    return [Punto(random.randint(x_range[0], x_range[1]),
                  random.randint(y_range[0], y_range[1]))
            for _ in range(num_points)]

def generate_random_polygon(num_points, x_range=(-20, 20), y_range=(-20, 20)):
    """Genera un polígono simple aleatorio (estrellado respecto a su baricentro)."""
    puntos = generate_random_puntos(num_points, x_range, y_range)
    # Calculamos el baricentro para ordenar angularmente y asegurar que sea simple
    cx = sum(p.x for p in puntos) / num_points
    cy = sum(p.y for p in puntos) / num_points
    puntos.sort(key=lambda p: math.atan2(p.y - cy, p.x - cx))
    return puntos

def plot_triangulacion(poligono, triangulos, title="Triangulación de Polígono"):
    """Dibuja el polígono y su triangulación."""
    plt.figure(figsize=(8, 8))
    
    # Dibujar el polígono (cerrado)
    px = [p.x for p in poligono] + [poligono[0].x]
    py = [p.y for p in poligono] + [poligono[0].y]
    plt.plot(px, py, color='black', linewidth=2, label='Polígono', zorder=2)

    # Dibujar los triángulos
    for i, tri in enumerate(triangulos):
        tx = [p.x for p in tri] + [tri[0].x]
        ty = [p.y for p in tri] + [tri[0].y]
        plt.plot(tx, ty, color='blue', linestyle='--', linewidth=0.8, alpha=0.7)
    
    # Dibujar los vértices
    vx = [p.x for p in poligono]
    vy = [p.y for p in poligono]
    plt.scatter(vx, vy, color='red', zorder=5)

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.gca().set_aspect('equal')
    plt.show()
