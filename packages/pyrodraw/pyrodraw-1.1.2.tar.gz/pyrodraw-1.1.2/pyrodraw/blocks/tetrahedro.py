from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from matplotlib import colors as mcolors

import numpy as np


"""
:class: 'Tetrahedro'. Clase para el dibujo de Tetrahedros de a pares (uno 'Up' y uno
'Down') en la dirección [111], a partir del centro del 'Up' y el lado 'L' del cubo en el
que se inscribe. Lo armo dibujando las cuatro caras triangulares de cada Tetrahedro. 
También se puede pasar como argumento 'N', que es un número relacionado a la intensidad
del sombreado en las caras (cuánto mayor es N, más transparentes serán las caras).
"""


class Tetrahedro:

    # Inicializo
    def __init__(self, centro, L, N=1):
        self.centro = centro
        self.L = L

        self.calcula_vertices()
        self.calcula_caras()
        self.dibuja_caras(N)

    # Método para el cálulo de los vértices. Se corresponde a sumarle a 'centro' las
    # posiciones de los vértices del Tetrahedro 'Up' respecto a su centro.
    def calcula_vertices(self):
        self.vertices = self.centro + self.L / 2 * np.array(
            [[1, 1, 1], [1, -1, -1], [-1, -1, 1], [-1, 1, -1]]
        )

    # Método para encontrar los vértices de cada cara triangular del Tetrahedro.
    def calcula_caras(self):

        self.vert_up = []  # Vértices de las caras del Tetrahedro Up.
        self.vert_down = []  # Vértices de las caras del Tetrahedro Down.

        # Con este loop se consideran todas las maneras de tomar de a tres puntos entre
        # los cuatro vértices del Tetrahedro, o sea, los vértices de cada cara triangular.
        for cara in [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]:
            # Las tres posiciones x de cada vértice de la cara triangular.
            vert_x = self.vertices[cara, 0]
            # Las tres posiciones y de cada vértice de la cara triangular.
            vert_y = self.vertices[cara, 1]
            # Las tres posiciones z de cada vértice de la cara triangular.
            vert_z = self.vertices[cara, 2]

            self.vert_up.append(
                [[np.array(vert) for vert in zip(vert_x, vert_y, vert_z)]]
            )

            # Las caras del Tetrahedro down se arman invirtiendo los valores de los
            # vértices y trasladándolos.
            self.vert_down.append(
                [
                    [
                        np.array(vert)
                        for vert in zip(
                            -np.array(vert_x) + 2 * self.vertices[0, 0],
                            -np.array(vert_y) + 2 * self.vertices[0, 1],
                            -np.array(vert_z) + 2 * self.vertices[0, 2],
                        )
                    ]
                ]
            )

    # Método par dibujar las caras de ambos Tetrahedros a partir de los vértices
    # de sus caras.
    def dibuja_caras(self, N):

        self.caras = []

        for i, (cara_up, cara_down) in enumerate(zip(self.vert_up, self.vert_down)):
            self.caras.append(
                Poly3DCollection(
                    cara_up,
                    facecolors=mcolors.to_rgba(
                        "mediumpurple", alpha=(0.1 + i * 0.1) / np.cbrt(N)
                    ),
                    edgecolors=mcolors.to_rgba("gray", alpha=0.1 / np.cbrt(N)),
                )
            )

            self.caras.append(
                Poly3DCollection(
                    cara_down,
                    facecolors=mcolors.to_rgba(
                        "lightskyblue", alpha=(0.1 + i * 0.1) / np.cbrt(N)
                    ),
                    edgecolors=mcolors.to_rgba("gray", alpha=0.1 / np.cbrt(N)),
                )
            )


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    t = Tetrahedro([0, 0, 0], 0.5)

    for cara in t.caras:
        ax.add_collection3d(cara)

    ax.scatter(*np.hsplit(t.vertices, 3), s=0)

    # ax.set_aspect("equal")
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(20, -75)

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    plt.show()
