# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrodraw', 'pyrodraw.blocks']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3,<4.0', 'numpy>=1,<2', 'pandas>=1,<2']

setup_kwargs = {
    'name': 'pyrodraw',
    'version': '1.1.2',
    'description': 'Library to draw the pyrochlore lattice and configurations of the Spin Ice model',
    'long_description': "# Overview\n\nLibrary based on `matplotlib` (`>=3.3`) to draw the pyrochlore lattice (corner-sharing tetrahedra) and configurations of the Spin Ice model.\n\n![Example](https://raw.githubusercontent.com/Raudcu/pyrodraw/master/example.png)\n\n\n# Installation\n\n`$ pip install pyrodraw`\n\n# Basic usage\n\nIt can, and probably should, be executed as a script:\n\n`python -m pyrodraw [<parameters>...]`\n\nand follow the instructions which appear on the screen.\n\nDepending on the parameters supplied:\n* No arguments: draws only the pyrochlore lattices and adds details such as names to the axes.\n* '+ z': draws the spin ice +z configuration.\n* 'ms': draws the saturation configuration with the field at [111], with positives simple monopoles in all Up Tetrahedra.\n* 'md': draws the configuration with positive double monopoles in all Up Tetrahedra.\n* Name of a file along with a column number: the data is obtained from it to draw the configuration.\n\nIt's also possible to import it and use it to draw more specific configurations.\n\n# Possible general improvements\nThe following are things I didn't know how to do it properly by the time I built the library, and for the purpose of the project it didn't worth changing them when I published it.\n* The documentation is not properly done (doesn't follow a docstring convention), and it's in spanish.\n* It probably should use `argparse` for managing the arguments.\n\n# ToDo\n* Add a circle path as a bottom lid for the arrows.\n* Be possible to annotate the field direction when using the field arrow.\n",
    'author': 'Lucas Pili',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Raudcu/pyrodraw',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
