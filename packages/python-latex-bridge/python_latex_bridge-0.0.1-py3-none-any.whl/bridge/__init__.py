"""
A package to include python variable values in a LaTeX document.

Example:

    from bridge import save
    from uncertainties import ufloat
    from pint import UnitRegistry

    ureg = UnitRegistry()
    Q = ureg.Quantity

    x = 1024
    save(x) # creates `variables/variable.dat` containing "1024"

    y = ufloat(3.1, 0.2)
    save(y, name='height') # creates `variables/height.dat` containing "3.1 \pm 0.2"

    z = Q(42, 'mm')
    save(z, path='length') # creates `length/variable.dat` containing "(42.0 \pm 3.0)\,\si[]{\milli\meter}"

"""
from .exporter import *

# Current version of the python-latex-bridge packages
__author__ = 'Tim Mutkala <contact@tim-media.com>'
__version_info__ = (0, 0, 1)
__version__ = '.'.join(map(str, __version_info__))