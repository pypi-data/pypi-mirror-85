from cycler import cycler
import math
import re
from colour import Color
from typing import Union, List
from string import Template


class Cycler(object):
    """ Colors and line cycler

    Can cycle through combination of colors and line or marker styles. Colors will be computed from a color gradient,
    depending on the number of lines to plot, which is given as an argument at object creation, and the number of
    styles. By default, styles are supposed to be linestyles. This can be changed to marker with the 'style' argument.

    can be used in matplotlib like this :.

    >>> # noinspection PyUnresolvedReferences
    >>> from matplotlib import pyplot as plt  # doctest: +SKIP
    >>> number_of_curves = 15  # doctest: +SKIP
    >>> cy = Cycler(ncurves=number_of_curves)  # doctest: +SKIP
    >>> plt.rc('axes', prop_cycle=cy.cycler)  # doctest: +SKIP
    """

    cstart: Color
    cend: Color

    def __init__(
        self,
        color_start: Union[str, Color] = "darkblue",
        color_end: Union[str, Color] = "darkred",
        linestyles: List[str] = None,
        markerstyles: List[str] = None,
        styles: List[str] = None,
        style: str = "line",
        ncurves: int = 10,
        ncolors: int = 5,
    ):
        """
        Parameters
        ----------
        color_start: Union[str, Color]
            start color
        color_end: Union[str, Color]
            end color
        linestyles: List[str]
            lines styles
        markerstyles: List[str]
            makers styles
        styles: List[str]
            mixed lines and makers styles
        style: str
            line or marker
        ncurves: int
            number of curves
        ncolors: int
            number of colors
        """
        self.cstart = color_start if isinstance(color_start, Color) else Color(color_start)
        self.cend = color_end if isinstance(color_end, Color) else Color(color_end)
        self.linestyles = linestyles if linestyles else ["-", "--", ":", "-."]
        self.markerstyles = markerstyles if markerstyles else [".", "x", "v", "^", "s", "+"]
        self.styles = styles if styles else []
        self.style = end_replace("s", "", style.lower())
        self.ncurves = ncurves
        self.ncolors = ncolors

        if self.style not in ["line", "marker"]:
            raise ValueError(f"Unkown style {self.style}")

        if self.ncurves > 5:
            if len(self.styles) * 5 <= self.ncurves:
                self.nstyles = math.ceil(self.ncurves / 5)
                self.styles = self.styles[: self.nstyles]
            else:
                self.ncolors = math.ceil(self.ncurves / len(self.styles))
        else:
            self.styles = []

        if len(self.styles) == 0:
            self.styles = getattr(self, f"{self.style}styles")

    @property
    def colors(self):
        return map(to_rgb, self.cstart.range_to(self.cend, self.ncolors))

    @property
    def cycler(self):
        if self.styles is not None:
            if self.style == "line":
                return self.linestyle_cycler * self.color_cycler
            elif self.style == "marker":
                return self.marker_cycler * self.color_cycler
        else:
            return self.color_cycler

    @property
    def color_cycler(self):
        return cycler(color=self.colors)

    @property
    def linestyle_cycler(self):
        return cycler(linestyle=self.linestyles)

    @property
    def marker_cycler(self):
        return cycler(marker=self.markerstyles)

    def __str__(self):
        return f"Cycler of {self.ncurves} curves"

    def __repr__(self):
        return Template(
            'Cycler(color_start="$color_start", color_end="$color_end", linestyles=$linestyles, '
            'markerstyles=$markerstyles, styles=$styles, style="$style", ncurves=$ncurves, '
            "ncolors=$ncolors)"
        ).safe_substitute(
            {
                "color_start": self.cstart,
                "color_end": self.cend,
                "linestyles": self.linestyles,
                "markerstyles": self.markerstyles,
                "styles": self.styles,
                "style": self.style,
                "ncurves": self.ncurves,
                "ncolors": self.ncolors,
            }
        )


def to_rgb(col: Color):
    return col.rgb


def end_replace(pattern: str, sub: str, string: str) -> str:
    """Replace pattern with sub at the end of string.

    Replaces 'pattern' in 'string' with 'sub' if 'pattern' ends 'string'.

    Parameters
    ----------
    pattern : str
        regex patern
    sub : str
        substitute string
    string : str
        main string

    Returns
    -------
    str
        remplaced string
        identical if identical
    """
    return re.sub(f"{pattern}$", sub, string)
