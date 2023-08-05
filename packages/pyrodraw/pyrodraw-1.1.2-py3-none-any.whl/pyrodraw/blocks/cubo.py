from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from matplotlib import colors as mcolors

import numpy as np

from itertools import product, combinations


"""
:class: 'Cubo'. Clase para el dibujo de Cubos a partir de su lado 'L' y la posición 
'vert' de uno de sus vértices. Lo armo dibujando las seis caras, aunque también tiene la
posibilidad de dibujar sólo los bordes. Además se puede pasar como parámetro el valor de
alpha para las caras ('face_alpha'), el color de los bordes de las caras ('edge_color'), 
el tipo de línea ('line_style') y su grosor ('line_width').
"""


class Cubo:

    # Inicializo
    def __init__(
        self,
        L,
        vert=[0, 0, 0],
        face_alpha=0,
        edge_color="silver",
        line_style=":",
        line_width=0.2,
    ):
        self.L = L
        self.vert = vert

        self.calcula_vertices()
        self.calcula_bordes()
        self.calcula_caras()

        self.dibuja_caras(face_alpha, edge_color, line_style, line_width)

    # Método para el cálculo de los vértices. 
    # Se corresponde a trasladar el vértice en [0,0,0] en 'vert'.
    def calcula_vertices(self):
        self.vertices = self.vert + np.array(
            list(product([0, self.L], [0, self.L], [0, self.L]))
        )

    # Método para el cálculo de los bordes.
    def calcula_bordes(self):

        x, y, z = [], [], []

        for s, e in combinations(self.vertices, 2):
            if abs(np.sum(np.abs(s - e)) - self.L) < 0.0001:
                x.append([s[0], e[0]])
                y.append([s[1], e[1]])
                z.append([s[2], e[2]])

        self.bordes = zip(x, y, z)

    # Método para encontrar los vértices de cada cara del Cubo.
    def calcula_caras(self):

        self.vert_caras = []  # Vértices de las caras del Cubo.

        # Con este loop se consideran las seis maneras que corresponden de tomar de a
        # cuatos puntos entre los ocho vértices del Cubo.
        faces = [
            (2, 0, 1, 3),
            (0, 4, 5, 1),
            (0, 4, 6, 2),
            (1, 5, 7, 3),
            (6, 2, 3, 7),
            (4, 6, 7, 5),
        ]

        for cara in faces:
            vert_x = self.vertices[
                cara, 0
            ]  # Las cuatos posiciones x de cada vértice de la cara.
            vert_y = self.vertices[
                cara, 1
            ]  # Las cuatos posiciones y de cada vértice de la cara.
            vert_z = self.vertices[
                cara, 2
            ]  # Las cuatos posiciones z de cada vértice de la cara.

            self.vert_caras.append(
                [np.array(vert) for vert in zip(vert_x, vert_y, vert_z)]
            )

    # Método par dibujar las caras del Cubo a partir de los vértices de sus caras.
    def dibuja_caras(self, face_alpha, edge_color, line_style, line_width):

        self.caras = Poly3DCollection(
            self.vert_caras,
            facecolors=mcolors.to_rgba("gray", alpha=face_alpha),
            edgecolors=edge_color,
            linestyle=line_style,
            lw=line_width,
        )


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    c = Cubo(np.sqrt(2) * 2, [1, 1, 1], 0.2, "black", "-", 1)

    ax.add_collection3d(c.caras)

    for edge in c.bordes:
        ax.plot3D(*edge, color="red", lw=3)

    ax.scatter3D(*np.hsplit(c.vertices, 3), s=60)

    c = Cubo(1)

    ax.add_collection3d(c.caras)

    for edge in c.bordes:
        ax.plot3D(*edge, color="blue", lw=2)

    ax.scatter3D(*np.hsplit(c.vertices, 3), s=60)

    # ax.set_aspect("equal")
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(20, -75)

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    plt.show()
