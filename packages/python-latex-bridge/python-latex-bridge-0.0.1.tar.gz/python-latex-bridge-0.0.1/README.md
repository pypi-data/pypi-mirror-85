# python-latex-bridge
Python package to include python variables in a LaTeX document.

## Example
Some use cases given a file with
```python
from bridge import save
from uncertainties import ufloat
from pint import UnitRegistry
ureg = UnitRegistry()
Q = ureg.Quantity
```
- Any python value:
    ```python
    x = 1024
    save(x) # creates `variables/variable.dat` containing "1024"
    ```
- Uncertain value:
    ```python
    x = ufloat(3.1, 0.2)
    save(x, name='height') # creates `variables/height.dat` containing "3.10 \pm 0.20"
    ```
- Variable with unit
    ```python
    x = Q(42, 'mm')
    save(x, path='values') # creates `values/variable.dat` containing "42\,\si[]{\milli\meter}"
    ```
- Error and unit:
    ```python
    x = Q(ufloat(420, 7), 'ohm')
    save(x) # creates `variables/variable.dat` containing "(420 \pm 7)\,\si[]{\ohm}"
    ```
## Usage in LaTeX
To fetch the value in a LaTeX document, simply include the `.dat` file in math mode
```
$\include{variables/variable.dat}$
```
assuming the `.tex` file and the `variables/` folder share the same parent directory. 