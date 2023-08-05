import numpy as np
import sys

from pyrodraw import CeldaUnidad

from pyrodraw.blocks import Paralelepipedo
from pyrodraw.blocks import Flecha

"""
:class: 'Sistema'. Clase para construir y plotear todas las celdas que 
se desean del Sistema, con los valores de spin 'spin_values' y sus 
'posiciones' (si la lista está vacía se calculará), de tamaño Lx, Ly, Lz
en 'L', comenzando por la celda 'inicial'. Además es posible pasar un 
vector de campo en 'field', con el que se dibuja un flecha en esa 
dirección. Se inicializa también con 'flechas' y 'monopolos' que 
determinan qué clase de flechas y esferas se van a dibujar: True las 
lindas pero pesadas, False las feas pero livianas. El último argumento
de inicialización es 'numeros' que indica si escribir o no el número de
cada spin.
"""


class Sistema:

    # Inicializo
    def __init__(
        self,
        spin_values,
        posiciones=np.array([]),
        L=np.ones(3, np.int),
        inicial=np.zeros(3, np.int),
        field=np.zeros(3, np.int),
    ):
        self.N = len(spin_values)

        self.L = round(
            (self.N / 16) ** (1 / 3)
        )  # L del sistema completo. Se supone cúbico.

        if (
            np.all(inicial < self.L)
            and np.all(L > 0)
            and np.all(L <= self.L)
            and np.all(inicial + L <= self.L)
        ):
            self.ix = inicial[0]
            self.iy = inicial[1]
            self.iz = inicial[2]

            self.Lx = L[0]
            self.Ly = L[1]
            self.Lz = L[2]
            self.N_cells = np.prod(L)

        else:
            sys.exit(
                "\n***ERROR: Las celda/s requerida/s no se corresponde/n con la cantidad de datos ingresados***\n"
            )

        self.spin_values = np.array(spin_values)

        if posiciones.size == 0:
            self.posiciones = self.r0(self.N)
        else:
            self.posiciones = posiciones.values

        self.field = (
            field / np.linalg.norm(field) if np.linalg.norm(field) > 0 else field
        )

        # Genero la celdas y el paralelepipedo exterior para los bordes.
        self.celdas = [
            CeldaUnidad([i, j, k], self.posiciones, self.spin_values, self.N_cells)
            for j in range(self.iy, self.iy + self.Ly)
            for k in range(self.iz, self.iz + self.Lz)
            for i in range(self.ix, self.ix + self.Lx)
        ]

        self.paralelepipedo = Paralelepipedo(
            np.array([self.Lx, self.Ly, self.Lz]) * np.sqrt(8),
            np.array([self.ix, self.iy, self.iz]) * np.sqrt(8),
        )

    # Método para determinar posiciones de equilibrio (vértices de los tetrahedros).
    def r0(self, N):

        r0 = []

        for i in range(1, N, 16):
            Tetrahedron = []

            # Tetrahedros. Determino primero las posiciones de los centros de los cuatro tetrahedros up.
            Tetrahedron.append(
                np.array(
                    [
                        int(i / 16) % self.L,
                        int((i / 16) / self.L) % self.L,
                        int((i / 16) / (self.L * self.L)),
                    ]
                )
            )
            Tetrahedron.append(Tetrahedron[0] + [0.5, 0.5, 0.0])
            Tetrahedron.append(Tetrahedron[0] + [0.0, 0.5, 0.5])
            Tetrahedron.append(Tetrahedron[0] + [0.5, 0.0, 0.5])

            # Átomos. Posiciono los átomos en los vértices de cada tetrahedro.
            for j in range(4):
                r0.append(Tetrahedron[j] + [0.125, 0.125, 0.125])
                r0.append(Tetrahedron[j] + [0.125, -0.125, -0.125])
                r0.append(Tetrahedron[j] + [-0.125, -0.125, 0.125])
                r0.append(Tetrahedron[j] + [-0.125, 0.125, -0.125])

        r0 /= np.sqrt(2) / 4

        return r0

    # Método para plotear todos los componentes del sistema. Primero las celdas, después el borde del dibujo y, si corresponde, la flecha que indica la dirección del campo.
    def plotear(self, ax, plot_flechas=False, plot_monopolos=False, plot_numeros=False):

        # Celdas
        for celda in self.celdas:

            # Cubo
            ax.add_collection3d(celda.cubo.caras)

            # Tetrahedros
            for tetrahedro in celda.tetrahedros:

                for cara in tetrahedro.caras:
                    ax.add_collection3d(cara)

            # Spines
            for j, spines in enumerate(celda.spines):

                # Flechas
                if plot_flechas:

                    for flecha, color in zip(spines.flechas, spines.colores):
                        x, y, z = zip(*flecha.coordenadas)
                        ax.plot_surface(
                            np.array(x), np.array(y), np.array(z), color=color
                        )

                else:

                    spines.colores = np.concatenate(
                        (spines.colores, np.repeat(spines.colores, 2, axis=0))
                    )
                    ax.quiver(
                        *np.hsplit(spines.posiciones, 3),
                        *np.hsplit(spines.vectores, 3),
                        length=0.5,
                        arrow_length_ratio=0.5,
                        pivot="middle",
                        normalize=True,
                        capstyle="round",
                        colors=spines.colores,
                        lw=2 / np.cbrt(self.N_cells)
                    )

                # Puntos donde hay Spines que valen 0
                for i, spin in enumerate(spines.s1234):

                    if spin == 0:
                        ax.scatter(*np.hsplit(spines.posiciones[i], 3), s=50, c="C1")

                # Números
                if plot_numeros:

                    for i, pos in enumerate(spines.posiciones):
                        ax.text(
                            *pos + [0.05, 0, -0.2],
                            str(celda.spin_inicial + j * 4 + i + 1),
                            fontfamily="serif",
                            fontsize=12
                        )

            # Monopolos
            for monopolo in celda.monopolos:

                if plot_monopolos:

                    if monopolo.radio != 0:
                        x, y, z = zip(*monopolo.coordenadas)
                        ax.plot_surface(
                            np.array(x), np.array(y), np.array(z), color=monopolo.color
                        )

                else:

                    ax.scatter(
                        *monopolo.centro,
                        s=monopolo.radio * 2800 / max(self.Lx, self.Ly, self.Lz),
                        color=monopolo.color
                    )

        # Bordes
        ax.add_collection3d(self.paralelepipedo.caras)

        # Flecha de dirección del Campo
        if plot_flechas and not np.all(self.field == 0):

            field_direction = Flecha(
                [
                    (self.ix + self.Lx + 0.2) * np.sqrt(8),
                    (self.iy + 0.5 * self.Ly) * np.sqrt(8),
                    (self.iz + 0.5 * self.Lz) * np.sqrt(8),
                ],
                self.field,
                self.Lz * np.sqrt(8) / 2,
                0.3,
                0.06 * self.Lz,
                1.8,
            )

            x, y, z = zip(*field_direction.coordenadas)
            ax.plot_surface(np.array(x), np.array(y), np.array(z), color="navy")

        else:

            ax.quiver(
                (self.ix + self.Lx + 0.2) * np.sqrt(8),
                (self.iy + 0.5 * self.Ly) * np.sqrt(8),
                (self.iz + 0.5 * self.Lz) * np.sqrt(8),
                *self.field,
                length=self.Lz * np.sqrt(8) / 2,
                arrow_length_ratio=0.3,
                pivot="middle",
                capstyle="round",
                colors="navy",
                lw=3
            )

        # Limits and aspect
        ax.set_xlim(
            self.ix * np.sqrt(8),
            (self.ix + max(self.Lx, self.Ly, self.Lz)) * np.sqrt(8),
        )
        ax.set_ylim(
            self.iy * np.sqrt(8),
            (self.iy + max(self.Lx, self.Ly, self.Lz)) * np.sqrt(8),
        )
        ax.set_zlim(
            self.iz * np.sqrt(8),
            (self.iz + max(self.Lx, self.Ly, self.Lz)) * np.sqrt(8),
        )

        # ax.set_aspect("equal")
        ax.set_box_aspect((1, 1, 1))

        # Hide axis. No uso ax.axis('off') para que pueda poner nombre a los ejes cuando sólo dibujo la red.
        ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

        ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
        ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
