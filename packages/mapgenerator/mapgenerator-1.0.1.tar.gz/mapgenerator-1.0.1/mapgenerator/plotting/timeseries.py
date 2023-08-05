import math
import os
import logging
import re

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.cbook as cbook

from mapgenerator.plotting.definitions import MapGenerator

logger = logging.getLogger(__name__)


class PlotSeries(MapGenerator):
    """ Main class for plotting time series """

    def __init__(self, loglevel='WARNING', **kwargs):
        """ Initialize class with attributes """
        super().__init__(loglevel=loglevel, kwargs=kwargs)
        self._current_fig = None
        self.scalex = kwargs.get('scalex', None)
        self.scaley = kwargs.get('scaley', None)
        self.suptitle_fontsize = kwargs.get('suptitle_fontsize', 24)
        self.title_fontsize = kwargs.get('title_fontsize', 16)
        self.axis_fontsize = kwargs.get('axis_fontsize', 12)
        self.plot_size = kwargs.get("plot_size", (8.0, 6.0))

    def _close(self):
        plt.close(self._current_fig)
        self._current_fig = None

    def plot_cube(self, cube, coord=None, **kwargs):
        if coord:
            coord = cube.coord(coord)
        if not coord and cube.dim_coords:
            coord = cube.dim_coords[0]
        if not coord and cube.dim_coords:
            coord = cube.aux_coords[0]

        points = coord.points
        if 'xlabel' not in kwargs:
            kwargs['xlabel'] = self._get_default_title(cube)
        self._current_fig = plt.figure(figsize=self.plot_size)
        self._plot_array(
            points,
            cube.data,
            title=self._get_default_title(cube),
            **kwargs,
        )
        self._set_time_axis(coord)
        self._current_fig.tight_layout()
        suptitle = kwargs.pop('suptitle', None)
        if suptitle:
            plt.suptitle(suptitle, y=1.08, fontsize=self.suptitle_fontsize)
        self._save_fig(self.img_template)
        self._close()

    def _plot_array(self, x, y, **kwargs):
        invertx = kwargs.pop('invertx', False)
        inverty = kwargs.pop('inverty', False)
        xlabel = kwargs.pop('xlabel', None)
        ylabel = kwargs.pop('ylabel', None)
        xlimits = kwargs.pop('xlimits', None)
        ylimits = kwargs.pop('ylimits', None)
        title = kwargs.pop('title', None)
        plt.plot(x, y)
        ax = plt.gca()
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=self.axis_fontsize)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=self.axis_fontsize)
        if title:
            ax.set_title(title, fontsize=self.title_fontsize, y=1.04)
        if invertx:
            logger.debug('Invert x axis')
            ax.invert_xaxis()
        if inverty:
            logger.debug('Invert y axis')
            ax.invert_yaxis()
        if self.scalex:
            ax.set_xscale(self.scalex)
        if self.scaley:
            ax.set_yscale(self.scaley)
        if xlimits:
            if xlimits == 'tight':
                ax.set_xlim(left=x.min(), right=x.max())
            elif xlimits == 'auto':
                ax.set_autoscalex_on(True)
            else:
                ax.set_xlim(left=xlimits[0], right=xlimits[1])
        if ylimits:
            if ylimits == 'tight':
                ax.set_ylim(left=y.min(), right=y.max())
            elif ylimits == 'auto':
                ax.set_autoscaley_on(True)
            else:
                ax.set_ylim(left=ylimits[0], right=ylimits[1])
        ax.grid(b=True, which='major', axis='both', alpha=0.6)
        ax.grid(b=True, which='minor', axis='both', alpha=0.3)
        ax.tick_params(
            axis='both', which='major', labelsize=self.axis_fontsize)

    def multiplot_cube(self, cube, coord, multi_coord, ncols=2, invert=False,
                       **kwargs):
        coord = cube.coord(coord)
        multi_coord = cube.coord(multi_coord)
        if multi_coord.shape[0] == 1:
            self.plot_cube(cube, coord, **kwargs)
            return
        sharex = kwargs.get('sharex', False)
        sharey = kwargs.get('sharey', False)

        self._current_fig = plt.figure(
            figsize=(
                ncols * self.plot_size[0],
                math.ceil(multi_coord.shape[0] / ncols) * self.plot_size[1])
        )
        suptitle = kwargs.pop('suptitle', '')
        if suptitle:
            suptitle = f"{suptitle}\n\n{self._get_default_title(cube)}"
        else:
            suptitle = self._get_default_title(cube)
        self._current_fig.suptitle(
            suptitle, y=1.0, fontsize=self.suptitle_fontsize
        )
        gs = GridSpec(math.ceil(multi_coord.shape[0] / ncols), ncols)
        for i, plot_cube in enumerate(cube.slices_over(multi_coord)):
            if i == 0 or not (sharex or sharey):
                self._current_fig.add_subplot(gs[i])
            elif sharex:
                if sharey:
                    self._current_fig.add_subplot(
                        gs[i], sharex=plt.gca(), sharey=plt.gca())
                    kwargs.pop('invertx', None)
                    kwargs.pop('inverty', None)
                else:
                    self._current_fig.add_subplot(gs[i], sharex=plt.gca())
                    kwargs.pop('invertx', None)
            elif sharey:
                self._current_fig.add_subplot(gs[i], sharey=plt.gca())
                kwargs.pop('inverty', None)
            title = plot_cube.coord(multi_coord).cell(0).point
            if isinstance(title, bytes):
                title = title.decode()
            plt.title(
                title,
                fontsize=self.title_fontsize
            )
            points = coord.points
            if invert:
                x = plot_cube.data
                y = points
                if 'ylabel' not in kwargs:
                    kwargs['ylabel'] = self._get_default_title(coord)
            else:
                x = points
                y = plot_cube.data
                if 'xlabel' not in kwargs:
                    kwargs['xlabel'] = self._get_default_title(coord)

            self._plot_array(
                x, y, **kwargs,
            )
            self._set_time_axis(coord)

        self._current_fig.tight_layout(pad=2.0)
        self._save_fig(self.img_template)
        self._close()

    def _save_fig(self, name):
        fullname = os.path.join(self.outdir, f"{name}.{self.filefmt}")
        self._current_fig.savefig(
            fullname, bbox_inches='tight', pad_inches=.2, dpi=self.dpi)

    @staticmethod
    def _set_time_axis(coord):
        if not coord.units.calendar:
            return
        axis = plt.gca().xaxis
        years = coord.cell(-1).point.year - coord.cell(0).point.year
        if years < 10:
            major_locator = 1
            minor_locator = None
        elif years < 50:
            major_locator = 5
            minor_locator = 1
        elif years < 100:
            major_locator = 10
            minor_locator = 2
        else:
            major_locator = 20
            minor_locator = 5
        axis.set_major_locator(YearLocator(coord.units, major_locator))
        if minor_locator:
            axis.set_minor_locator(YearLocator(coord.units, minor_locator))
        axis.set_major_formatter(DateFormatter('%Y', coord.units))
        axis.label._text = f"{coord.name()} (years)"


class YearLocator(mdates.DateLocator):
    """
    Make ticks on a given day of each year that is a multiple of base.

    Examples::

      # Tick every year on Jan 1st
      locator = YearLocator()

      # Tick every 5 years on July 4th
      locator = YearLocator(5, month=7, day=4)
    """
    def __init__(self, units, base=1, month=1, day=1, tz=None, ):
        """
        Mark years that are multiple of base on a given month and day
        (default jan 1).
        """
        mdates.DateLocator.__init__(self, tz)
        self.units = units
        self.base = ticker._Edge_integer(base, 0)
        self.replaced = {'month':  month,
                         'day':    day,
                         'hour':   0,
                         'minute': 0,
                         'second': 0,
                         }

    def __call__(self):
        # if no data have been set, this will tank with a ValueError
        try:
            dmin, dmax = self.viewlim_to_dt()
        except ValueError:
            return []

        return self.tick_values(dmin, dmax)

    def viewlim_to_dt(self):
        """
        Converts the view interval to datetime objects.
        """
        vmin, vmax = self.axis.get_view_interval()
        if vmin > vmax:
            vmin, vmax = vmax, vmin
        if vmin < 1:
            raise ValueError('view limit minimum {} is less than 1 and '
                             'is an invalid Matplotlib date value. This '
                             'often happens if you pass a non-datetime '
                             'value to an axis that has datetime units'
                             .format(vmin))
        return self.units.num2date(vmin), self.units.num2date(vmax)

    def tick_values(self, vmin, vmax):
        ymin = self.base.le(vmin.year) * self.base.step
        ymax = self.base.ge(vmax.year) * self.base.step

        vmin = vmin.replace(year=ymin, **self.replaced)

        ticks = [vmin]

        while True:
            dt = ticks[-1]
            if dt.year >= ymax:
                return self.units.date2num(ticks)
            year = dt.year + self.base.step
            dt = dt.replace(year=year, **self.replaced)
            ticks.append(dt)

    @cbook.deprecated("3.2")
    def autoscale(self):
        """
        Set the view limits to include the data range.
        """
        dmin, dmax = self.datalim_to_dt()

        ymin = self.base.le(dmin.year)
        ymax = self.base.ge(dmax.year)
        vmin = dmin.replace(year=ymin, **self.replaced)
        vmin = vmin.astimezone(self.tz)
        vmax = dmax.replace(year=ymax, **self.replaced)
        vmax = vmax.astimezone(self.tz)

        vmin = self.units.date2num(vmin)
        vmax = self.units.date2num(vmax)
        return self.nonsingular(vmin, vmax)


class DateFormatter(ticker.Formatter):
    """
    Format a tick (in days since the epoch) with a
    `~datetime.datetime.strftime` format string.
    """

    illegal_s = re.compile(r"((^|[^%])(%%)*%s)")

    def __init__(self, fmt, units):
        """
        Parameters
        ----------
        fmt : str
            `~datetime.datetime.strftime` format string
        tz : `tzinfo`, default: :rc:`timezone`
            Ticks timezone.
        """
        self.units = units
        self.fmt = fmt

    def __call__(self, x, pos=0):
        if x == 0:
            raise ValueError('DateFormatter found a value of x=0, which is '
                             'an illegal date; this usually occurs because '
                             'you have not informed the axis that it is '
                             'plotting dates, e.g., with ax.xaxis_date()')
        return self.units.num2date(x).strftime(self.fmt)
