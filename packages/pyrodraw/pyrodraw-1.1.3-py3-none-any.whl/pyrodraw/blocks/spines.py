import numpy as np

from pyrodraw.blocks import Flecha


"""
:class: 'Spines'. Clase para el cálculo de los vectores correspondientes a los spines
dede un Tetrahedro Up y sus colores, dependiendo de la configuración pasada a través
de 's1234'.
"""


class Spines:

    # Base de los Spines de un Tetrahedro Up.
    base_spin = np.array([[1, 1, 1], [1, -1, -1], [-1, -1, 1], [-1, 1, -1]]) / np.sqrt(
        3
    )

    # Inicializo
    def __init__(self, posiciones, s1234):
        self.posiciones = posiciones
        self.s1234 = s1234

        self.calcula_vectores()
        self.calcula_colores()

        self.flechas = [
            Flecha(pivot, eje, 0.6, 0.4, 0.036, 1.8)
            for pivot, eje in zip(self.posiciones, self.vectores)
        ]

    # Método para calcular los vectores de cada spin de acuerdo a su valor.
    def calcula_vectores(self):
        self.vectores = np.matmul(np.diag(self.s1234), Spines.base_spin)
        self.vectores[
            self.vectores == 0
        ] = 1  # Esto lo hago para funcionen bien aunque algún Spin valga 0.

    # Método para calcular los colores de cada spin de acuerdo a su valor. 
    # Si es cero, dibuja una flecha transparente.
    def calcula_colores(self):
        self.colores = []

        for spin in self.s1234:
            if int(spin) == 1:
                self.colores.append([0, 0, 1, 1])
            elif int(spin) == -1:
                self.colores.append([0, 0, 0, 1])
            elif int(spin) == 0:
                self.colores.append([1, 1, 1, 0])


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    posiciones = np.array(
        [
            [0.125, 0.125, 0.125],
            [0.125, -0.125, -0.125],
            [-0.125, -0.125, 0.125],
            [-0.125, 0.125, -0.125],
        ]
    ) / (np.sqrt(2) / 4)

    s = Spines(posiciones, [1, -1, 1, 0])

    # Flechas
    ## Lindas
    for flecha, color in zip(s.flechas, s.colores):
        x, y, z = zip(*flecha.coordenadas)
        ax.plot_surface(np.array(x), np.array(y), np.array(z), color=color)

    ## Feas
    # s.colores = np.concatenate((s.colores, np.repeat(s.colores,2,axis=0)))
    # ax.quiver(*np.hsplit(s.posiciones,3), *np.hsplit(s.vectores,3),
    #           length=0.5, arrow_length_ratio=0.5, pivot='middle', normalize=True,
    #           capstyle='round', colors=s.colores, lw=2)

    # Puntos donde hay Spines que valen 0
    for i, spin in enumerate(s.s1234):

        if spin == 0:
            ax.scatter(*np.hsplit(s.posiciones[i], 3), s=50, c="C1")

    ax.set_xlim(0, np.sqrt(8))
    ax.set_ylim(0, np.sqrt(8))
    ax.set_zlim(0, np.sqrt(8))

    # ax.set_aspect("equal")
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(20, -75)

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    plt.show()
