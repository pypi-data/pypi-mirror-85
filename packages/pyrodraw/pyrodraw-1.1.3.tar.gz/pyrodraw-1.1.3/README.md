# Overview

Library based on `matplotlib` (`>=3.3`) to draw the pyrochlore lattice (corner-sharing tetrahedra) and configurations of the Spin Ice model.

![Example](https://raw.githubusercontent.com/Raudcu/pyrodraw/master/example.png)


# Installation

`$ pip install pyrodraw`

# Basic usage

It can, and probably should, be executed as a script:

`python -m pyrodraw [<parameters>...]`

and follow the instructions which appear on the screen.

Depending on the parameters supplied:
* No arguments: draws only the pyrochlore lattices and adds details such as names to the axes.
* '+ z': draws the spin ice +z configuration.
* 'ms': draws the saturation configuration with the field at [111], with positives simple monopoles in all Up Tetrahedra.
* 'md': draws the configuration with positive double monopoles in all Up Tetrahedra.
* Name of a file along with a column number: the data is obtained from it to draw the configuration.

It's also possible to import it and use it to draw more specific configurations.

# Possible general improvements
The following are things I didn't know how to do it properly by the time I built the library, and for the purpose of the project it didn't worth changing them when I published it.
* The documentation is not properly done (doesn't follow a docstring convention), and it's in spanish.
* It probably should use `argparse` for managing the arguments.

# ToDo
* Add a circle path as a bottom lid for the arrows.
* Be possible to annotate the field direction when using the field arrow.
