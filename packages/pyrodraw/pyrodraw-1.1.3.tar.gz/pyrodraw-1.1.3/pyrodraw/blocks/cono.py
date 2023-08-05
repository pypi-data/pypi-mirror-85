import numpy as np


"""
:class: 'Cono'. Clase para calcular las coordenadas cartesianas de un Cono a lo largo
del eje 'eje' con centro de la base en 'base', de radio máximo 'radio_max' y largo 
'largo'.
"""


class Cono:

    # Inicializo
    def __init__(self, base, eje, radio_max, largo):
        self.base = np.array(base)
        self.eje = np.array(eje) / np.linalg.norm(eje)  # Vector unitario
        self.radio_max = radio_max
        self.largo = largo

        self.punta = self.base + self.eje * self.largo  # Posición de la punta del cono

        self.calcula_coordenadas()

    # Método para el cálculo de las coordenadas cartesianas.
    def calcula_coordenadas(self):

        # Armo dos vectores unitarios perpendiculares entre sí y al eje del cono, para
        # que hagan las veces de ejes 'x' e 'y' sobre el que construir el cono. Primero
        # busco un vector en una dirección distinta al eje. Luego, con éste y el eje,
        # armo un vector unitario n1 perpendicular al eje. Finalmente, con eje y n1 armo
        # un vector unitario n2 perpendicular a ambos.
        not_eje = np.array([1, 0, 0])
        if (self.eje == not_eje).all():
            not_eje = np.array([0, 1, 0])

        _n1 = np.cross(self.eje, not_eje)
        _n1 = _n1 / np.linalg.norm(_n1)

        _n2 = np.cross(self.eje, _n1)

        # Variables paramétricas y grid.
        _theta = np.linspace(0, 2 * np.pi, 100)
        _t = np.linspace(0, -1, 100)

        _theta, _t = np.meshgrid(_theta, _t)

        x, y, z = [
            self.punta[i]
            + _t * self.largo * self.eje[i]
            + _t * self.radio_max * np.sin(_theta) * _n1[i]
            + _t * self.radio_max * np.cos(_theta) * _n2[i]
            for i in [0, 1, 2]
        ]

        self.coordenadas = zip(x, y, z)


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    c = Cono([1, 3, 1], [4, 2, 1], 2, 8)

    x, y, z = zip(*c.coordenadas)
    ax.plot_surface(np.array(x), np.array(y), np.array(z), color="r")

    # ax.set_aspect("equal")
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(20, -75)

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    plt.show()
