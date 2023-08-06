# Color and Style Cycler

Colors and style cycler

Can cycle through combination of colors and line or marker styles. Colors will be computed from a color gradient,
depending on the number of lines to plot, which is given as an argument at object creation, and the number of
styles. By default, styles are supposed to be linestyles. This can be changed to marker with the 'style' argument.


## Installation

`pip install colorstylecycler`

## Usage

```python

    
# noinspection PyUnresolvedReferences
from matplotlib import pyplot as plt
from colorstylecycler import Cycler
number_of_curves = 15
cy = Cycler(ncurves=number_of_curves)
plt.rc('axes', prop_cycle=cy.cycler)
```