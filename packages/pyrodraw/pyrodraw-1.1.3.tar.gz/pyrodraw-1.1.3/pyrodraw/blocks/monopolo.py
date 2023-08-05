from pyrodraw.blocks import Esfera


"""
:class: 'Monopolo'. Clase que hereda de Esfera para armar el Monopolo en 'centro' y con 
color dependiendo de 'carga'. Además el radio distingue si se trata de un monopolo
simple o doble.
"""


class Monopolo(Esfera):

    # Inicializo
    def __init__(self, centro, carga):

        self.carga = carga

        # Spin Ice
        if self.carga == 0:
            super().__init__(centro, 0)
            self.color = "k"

        # Monopolo simple
        elif self.carga == +2:
            super().__init__(centro, 0.16)
            self.color = "#02590f"

        elif self.carga == -2:
            super().__init__(centro, 0.16)
            self.color = "#be0119"

        # Monopolo doble
        elif self.carga == +4:
            super().__init__(centro, 0.24)
            self.color = "#01ff07"

        elif self.carga == -4:
            super().__init__(centro, 0.24)
            self.color = "r"

        # Otro caso (con Spines que valen 0)
        else:
            super().__init__(centro, 0)
            self.color = "k"


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    import numpy as np

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    m = Monopolo([0, 0, 0], int(sum([1, 1, -1, 1])))

    x, y, z = zip(*m.coordenadas)
    ax.plot_surface(np.array(x), np.array(y), np.array(z), color=m.color)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1)

    # ax.set_aspect("equal")
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(20, -75)

    plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
    plt.show()
