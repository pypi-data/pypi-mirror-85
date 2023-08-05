import os
import numpy as np
import pandas as pd

from pyrodraw.blocks import Tetrahedro
from pyrodraw.blocks import Cubo

from pyrodraw.blocks import Spines
from pyrodraw.blocks import Monopolo


"""
:class: 'CeldaUnidad'. Clase para construir todos los elementos de una celda unidad a
partir de su posición particular 'ijk', las posiciones de los spines en 'posiciones' y
sus valores de spin en 'spin_values'. El parámetro 'N_cells', que da cuenta del número
total de celdas a dibujar, se pasa como argumento para la graduación del color de las 
caras de los tetrahedros.
"""


class CeldaUnidad:

    # Base de la red FCC
    base_fcc = 0.5 * np.array([[0, 0, 0], [1, 1, 0], [0, 1, 1], [1, 0, 1]])

    # Inicializo
    def __init__(self, ijk, posiciones, spin_values, N_cells):
        self.i = ijk[0]
        self.j = ijk[1]
        self.k = ijk[2]

        self.centros_up = (CeldaUnidad.base_fcc + ijk) / (np.sqrt(2) / 4)
        self.centros_down = self.centros_up + np.array([1, 1, 1]) / np.sqrt(2)

        _L = round((len(spin_values) / 16) ** (1 / 3))
        self.spin_inicial = (self.i + self.j * _L + self.k * _L * _L) * 16

        # Cubo
        self.cubo = Cubo(np.sqrt(8), np.array(ijk) * np.sqrt(8))

        # Tetrahedros
        self.tetrahedros = [
            Tetrahedro(centro, np.sqrt(0.5), N_cells) for centro in self.centros_up
        ]

        # Spines
        self.spines = [
            Spines(posiciones[i : i + 4], spin_values[i : i + 4])
            for i in range(self.spin_inicial, self.spin_inicial + 16, 4)
        ]

        # Monopolos
        ## Tetrahedros Up
        self.monopolos = [
            Monopolo(centro, -int(sum(spin_values[i : i + 4])))
            for centro, i in zip(
                self.centros_up, range(self.spin_inicial, self.spin_inicial + 16, 4)
            )
        ]

        ## Tetrahedros Down. Los vecinos para formar el tetrahedro down se pueden buscar
        ## con el método 'tetra_down'. Para acelerar la ejecución, en especial para
        ## tamaños grandes de sistema, se van guardando en archivos las tabla de vecinos
        ## para cada valor de L: si alguna vez ya se buscó los vecinos para ese spin,
        ## estará en la tabla y se extrae de allí, caso contrario, se busca con el
        ## método antes mencionado y se añade también al archivo.
        _data_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "down_neighbors",
            "L" + str(_L) + ".dat",
        )

        if os.path.isfile(_data_file):
            _down_neighbors = pd.read_csv(
                _data_file, sep=r"\s+", header=None, index_col=0, dtype=np.int
            )

        else:
            _folder = os.path.dirname(_data_file)
            if not os.path.exists(_folder):
                os.makedirs(_folder)

            _down_neighbors = pd.DataFrame()

        for centro, i in zip(
            self.centros_down, range(self.spin_inicial, self.spin_inicial + 16, 4)
        ):

            if i in _down_neighbors.index:
                _spines_down = np.insert(_down_neighbors.loc[i].values, 0, i)

            else:
                _spines_down = CeldaUnidad.tetra_down(i, posiciones, _L)

                with open(_data_file, "a") as fl:
                    np.savetxt(
                        fl, np.atleast_2d(_spines_down), fmt="%8d", delimiter=" "
                    )

            self.monopolos.append(Monopolo(centro, int(sum(spin_values[_spines_down]))))

    @staticmethod
    # Método para dado un spin apical de un Tetrahedro Up, determinar los vecinos con
    # los que conforma el Down.
    def tetra_down(i, posiciones, L):
        # Caja
        box = L * np.sqrt(8)

        # Calculo r_ij para todos los spines respescto del spin i considerando
        # condiciones de contorno periódicas.
        r_ij = []

        for pos in posiciones:
            aux = pos - posiciones[i]
            r_ij.append(aux - np.around(aux / box) * box)

        r_ij = np.array(r_ij)

        # Calculo las distancias entre el spin i y el resto.
        distancias = np.linalg.norm(r_ij, axis=1)

        # Determino quienes son los primeros vecinos del spin i ordenando las distancias
        # y quedándome con los seis siguientes.
        vecinos = np.argsort(distancias)[1:7]

        # Los vecinos con los que el spin i forma el Tetrahedro Down son los tres que
        # tienen todas las componentes de r_ij al menos más grande que -np.sqrt(2)/4:
        # dos vecinos, en posición fija, siempre tienen una de las tres componentes de
        # rij igual a 0 y las otras dos con módulo igual a raíz de dos sobre dos (lo
        # cual me asegura una distancia entre primeros vecinos igual a 1). Para ser
        # conservativo, ya que los spines se pueden mover de su posición de equilibrio,
        # pido que las componentes sean mayor a raíz de dos sobre cuatro en lugar de
        # pedir que sean mayor a cero (porque de hecho a veces, debido a las
        # distorsiones, no lo son).
        vecinos_down = vecinos[
            np.apply_along_axis(
                lambda x: np.all(x >= -np.sqrt(2) / 4), 1, r_ij[vecinos]
            )
        ]

        # Retorno el array ordenado de vecinos_down con el spin i insertado al principio.
        return np.insert(np.sort(vecinos_down), 0, i)
