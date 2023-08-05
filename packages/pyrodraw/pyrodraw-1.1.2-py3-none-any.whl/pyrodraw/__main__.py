#!/usr/bin/env python3

"""
Script para plotear configuraciones de red Pirocloro.

Dependiendo de los parámetros ingresados:
* '': dibuja solamente la red pirocloro y agrega detalles como el nombres a los ejes.
* '+z': dibuja la configuración spin ice +z.
* 'ms': dibuja la configuración de saturación con el campo en [111], con monopolos 
simples positivos en todos los Tetrahedros Up.
* 'md': dibuja la configuración con monopolos dobles positivos en todos los Tetrahedros Up.
* Si se pasa el nombre de un archivo, se obtienen de él los datos para dibujar la 
configuración. Si no se pasa más que el nombre, se supone que es un output de uno de 
mis programas y se obtienen del mismo, además de los valores de spin, sus posiciones. Si
se pasa 'ch' como segundo argumento, significa que es un archivo de Chufo: se extraen de
él los valores de spin y se los ubica en los vértices de los tetrahedros. Si en cambio 
se pasa un valor de columna como segundo argumento, significa entonces que se trata de
un archivo de otra persona (que no debe tener header): se toman de esa columna los 
valores de spin y se los ubica en los vértices de los tetrahedros.
"""

# General setup
import sys
import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pyrodraw import Sistema


# Figure and axes
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")


# System construction
if len(sys.argv) > 3:
    sys.exit("\n***ERROR: Too many arguments***\n")


elif len(sys.argv) == 1:
    spin_values = np.array([0, 0, 0, 0] * 256)

    # Labels
    ax.set_xlabel("x", fontfamily="serif", fontsize=20)
    ax.set_ylabel("y", fontfamily="serif", fontsize=20)
    ax.set_zlabel("z", fontfamily="serif", fontsize=20)

    ax.xaxis.labelpad = -10
    ax.yaxis.labelpad = -10
    ax.zaxis.labelpad = -10

    # Ingreso de parámetros
    L = input("\n*Size 'LxLyLz' to draw [default: 111]: ")
    L = np.array([int(i) for i in L]) if L else np.ones(3, np.int)

    numeros = input("\n*¿Enumerate sites? (y/n) [default: no]: ")
    plot_numeros = True if numeros == "y" else False

    # Construyo y ploteo el sistema.
    print("\n\n***Wait while the plot is built***\n")
    s = Sistema(spin_values, L=L)
    s.plotear(ax, plot_numeros=plot_numeros)


else:
    posiciones = np.array([])

    filename = sys.argv[1]

    if filename == "+z":
        spin_values = np.array([1, -1, 1, -1] * 256)

    elif filename == "ms":
        spin_values = np.array([1, -1, -1, -1] * 256)

    elif filename == "md":
        spin_values = np.array([-1, -1, -1, -1] * 256)

    else:
        if not os.path.isfile(filename):
            sys.exit("\n***ERROR: Not valid option or file not found***\n")

        if len(sys.argv) == 2:  # Archivos míos
            df = pd.read_csv(
                filename, sep=r"\s+", header=None, skiprows=1, float_precision="high"
            )

            spin_values = df.iloc[:, 4]

            pos = input("\n*¿Positions from file? (y/n) [default: no]: ")
            if pos == "y":
                posiciones = df.iloc[:, 1:4]

        elif len(sys.argv) == 3:

            if sys.argv[2] == "ch":  # Archivos de Chufo

                with open(filename, "rt") as f:
                    # Auxiliary list
                    spin_values = []

                    # Skip header
                    for _ in range(5):
                        next(f)

                    # Extract spin values
                    for line in f:
                        row = line.split()
                        spin_values.extend([int(s) for s in row[4:8]])

                spin_values = np.array(spin_values)

            else:  # Archivos de otros
                df = pd.read_csv(
                    filename, sep=r"\s+", header=None, float_precision="high"
                )

                spin_values = df.iloc[:, int(sys.argv[2]) - 1]

    # Ingreso de parámetros y opciones.
    L = input("\n*Size 'LxLyLz' to draw [default: 111]: ")
    L = np.array([int(i) for i in L]) if L else np.ones(3, np.int)

    inicial = input("\n*Position 'xyz' of the init cell [default: 000]: ")
    inicial = np.array([int(i) for i in inicial]) if inicial else np.zeros(3, np.int)

    field = input("\n*Field direction 'BxByBz' [default: no arrow]: ")
    field = np.array([int(i) for i in field]) if field else np.zeros(3, np.int)

    nice = input('\n*Nice spins and monopoles? (y/n) [default: no]: ')
    plot_flechas, plot_monopolos = (True, True) if nice == "y" else (False, False)

    # Construyo y ploteo el sistema.
    print("\n\n***Wait while the plot is built***\n")
    s = Sistema(spin_values, posiciones, L, inicial, field)
    s.plotear(ax, plot_flechas, plot_monopolos)


# Show
ax.view_init(20, -75)
# ax.view_init(0,270)
# ax.view_init(0,45)

# plt.savefig(filename[:-4]+'.pdf', transparent=True, bbox_inches='tight')
# plt.savefig(filename[:-4]+'.png', transparent=True, bbox_inches='tight', dpi=500)

plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
plt.show()
