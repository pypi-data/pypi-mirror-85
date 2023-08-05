import numpy as np


"""
:class: 'Esfera'. Clase para calcular las coordenadas cartesianas de una Esfera centrada
en 'centro' y de radio 'radio'.
"""


class Esfera:

    # Inicializo
    def __init__(self, centro, radio):
        self.centro = centro
        self.radio = radio

        self.calcula_coordenadas()

    # Método para el cálculo de las coordenadas cartesianas.
    def calcula_coordenadas(self):
        _theta = np.linspace(0, np.pi, 100)
        _phi = np.linspace(0, 2 * np.pi, 100)

        _theta, _phi = np.meshgrid(_theta, _phi)

        x = self.centro[0] + self.radio * np.sin(_theta) * np.cos(_phi)
        y = self.centro[1] + self.radio * np.sin(_theta) * np.sin(_phi)
        z = self.centro[2] + self.radio * np.cos(_theta)

        self.coordenadas = zip(x, y, z)


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(8, 10))
    ax = fig.add_subplot(111, projection="3d")

    e = Esfera([1, 1, 1], 2)

    x, y, z = zip(*e.coordenadas)
    ax.plot_surface(np.array(x), np.array(y), np.array(z), color="r")

    # ax.set_aspect("equal")
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(20, -75)

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    plt.show()
