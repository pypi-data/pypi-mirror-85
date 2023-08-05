import numpy as np

from pyrodraw.blocks import Cilindro
from pyrodraw.blocks import Cono


"""
:class: 'Flecha'. Clase para calcular las coordenadas cartesianas de una Flecha, armada
con un Cilindro como vástago y un Cono como cabeza, a lo largo del eje 'eje' con centro
en 'pivot', de largo 'largo' y de radio 'radio' en su vástago, con una proporción entre
los radios del vástago y la cabeza dada por 'cono_cilindro_radio_ratio' y una relación
entre el largo del vástago y el largo total dada por 'cilindro_largo_ratio'.
"""


class Flecha:

    # Inicializo
    def __init__(
        self, pivot, eje, largo, cilindro_largo_ratio, radio, cono_cilindro_radio_ratio
    ):
        self.eje = np.array(eje) / np.linalg.norm(np.array(eje))
        self.pivot = np.array(pivot) - 0.5 * cilindro_largo_ratio * largo * self.eje

        self.largo = largo
        self.radio = radio

        self.cilindro = Cilindro(
            self.pivot, self.eje, self.radio, (1 - cilindro_largo_ratio) * self.largo
        )
        self.cono = Cono(
            self.cilindro.tapa,
            self.eje,
            cono_cilindro_radio_ratio * self.radio,
            cilindro_largo_ratio * self.largo,
        )

        self.calcula_coordenadas()

    # Método para el cálculo de las coordenadas cartesianas.
    def calcula_coordenadas(self):

        x_cilindro, y_cilindro, z_cilindro = zip(*self.cilindro.coordenadas)
        x_cono, y_cono, z_cono = zip(*self.cono.coordenadas)

        x = np.concatenate((np.array(x_cilindro), np.array(x_cono)))
        y = np.concatenate((np.array(y_cilindro), np.array(y_cono)))
        z = np.concatenate((np.array(z_cilindro), np.array(z_cono)))

        self.coordenadas = zip(x, y, z)


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    f = Flecha([1, 2, 3], [-1, -2, 1], 10, 0.5, 0.4, 1.5)

    x, y, z = zip(*f.coordenadas)
    ax.plot_surface(np.array(x), np.array(y), np.array(z), color="r")

    # ax.set_aspect("equal")
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(20, -75)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-10, 10)

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    plt.show()
