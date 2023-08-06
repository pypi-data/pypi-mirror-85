"""Simple bokeh plotting API."""

import warnings

import bokeh.io as bkio
from bokeh.layouts import gridplot

__version__ = '0.2.2'

# we don't run a comprehensive test suite and mostly in notebooks,
# so show warnings all the time.
warnings.simplefilter('always', DeprecationWarning)


class Grid(list):
    """Create a list of lists of fixed length."""

    def __init__(self, width=4):
        """Initialize the Grid."""
        self.width = width
        self.append(list())

    def add(self, item):
        """Add an item to the grid.

        :param item: item to add

        """
        self[-1].append(item)
        if len(self[-1]) == self.width:
            self.append(list())

    def extend(self, items):
        """Add multiple items.

        :param items: items to add.

        """
        for item in items:
            self.add(item)


def show(plot):
    """Show a plot in a notebook."""
    bkio.output_notebook(hide_banner=True)
    bkio.show(plot)


def grid(plots, ncol=4, display=True, **kwargs):
    """Show a grid of plots in a notebook.

    :param plots: a list of bokeh plots.
    :param ncol: number of columns.
    :param kwargs: kwargs for bokeh `gridplot`.

    """
    warnings.warn(
        "Please use `bokeh.layout.gridplot` directly with an optional "
        "call to `.show()`", DeprecationWarning)

    grid = Grid(width=ncol)
    grid.extend(plots)
    plot = gridplot(grid, **kwargs)
    if display:
        show(plot)
    else:
        return plot


def InfoGraphItems():
    """Cumulatively create items for an infographic."""
    from aplanat import graphics
    warnings.warn(
        "This class has been moved to `aplanat.graphics.InfoGraphItems()`",
        DeprecationWarning)
    return graphics.InfoGraphItems()


def infographic(items, **kwargs):
    """Create an infographic 'plot'."""
    from aplanat import graphics
    warnings.warn(
        "This function has been moved to `aplanat.graphics.infographic()`",
        DeprecationWarning)
    return graphics.infographic(items, **kwargs)
