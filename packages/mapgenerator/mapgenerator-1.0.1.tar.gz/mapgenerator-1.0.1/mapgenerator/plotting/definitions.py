# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Barcelona Supercomputing Center
# @license: https://www.gnu.org/licenses/gpl-3.0.html
# @author: see AUTHORS file

from netCDF4 import Dataset as nc
# from netCDF4 import MFDataset as mnc
# from grads import GaLab
import pandas as pd
import numpy as np
import numpy.ma as ma
from scipy.interpolate import griddata
from datetime import datetime
from datetime import timedelta
import os
import os.path
import copy

import logging

# logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def is_grid_regular(lon, lat):
    """ Check spacing if uniform. Returns True if grid is regular """

    # print("Checking if lon is strictly_increasing ...")
    if not np.array([strictly_increasing(lon[x]) for x in
                     np.arange(lon.shape[0])]).all():
        return False

    # print("Checking if lat is strictly_increasing ...")
    if not np.array([strictly_increasing(lat[:, y]) for y in
                     np.arange(lat.shape[1])]).all():
        return False

    # print("Checking lon spacing ...")
    is_x_reg = np.array([(np.spacing(lon[x]) == np.spacing(lon[x+1])).all()
                         for x in np.arange(lon.shape[0]-1)]).all()

    LOG.debug(is_x_reg)
    if not is_x_reg:
        return is_x_reg

    # print("Checking lat spacing ...")
    return np.array([(np.spacing(lat[:, y]) == np.spacing(lat[:, y+1])).all()
                     for y in np.arange(lat.shape[1]-1)]).all()


def strictly_increasing(vector):
    """ Check if vector values are strictly increasing """
    return all(x < y for x, y in zip(vector, vector[1:]))


def do_interpolation(data, lon, lat):
    """ Takes a not regular grid (curvilinear, whatever kind) and interpolate
    to regular one derived from the first. Very demanding operation, try to
    avoid """
    # lon as second dimension
    # lat as first dimension
    LOG.info("Irregular grid, performing interpolation ...")
    lat_s = lat.shape[0]
    lon_s = lon.shape[1]
    reglon = np.linspace(lon.min(), lon.max(), lon_s)
    reglat = np.linspace(lat.min(), lat.max(), lat_s)
    LOG.info("LAT: %s, LON: %s, DATA: %s", reglon.shape, reglat.shape,
             data.shape)
    regx, regy = np.meshgrid(reglon, reglat)
    result = np.empty(data.shape)*np.nan
    if ma.is_masked(data):
        data = data.filled(np.nan)

    # assuming that lat and lon are the latest dimensions
    if len(data.shape) == 2:
        result = griddata((lon.ravel(), lat.ravel()), data.ravel(), (regx,
                                                                     regy))
    elif len(data.shape) == 3:
        for i in range(data.shape[0]):
            tmp = griddata((lon.ravel(), lat.ravel()), data[i].ravel(), (regx,
                                                                         regy))
            result[i] = tmp.reshape(result[i].shape)
    elif len(data.shape) == 4:
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                tmp = griddata((lon.ravel(), lat.ravel()), data[i, j].ravel(),
                               (regx, regy))
                result[i, j, :, :] = tmp.reshape(result[i, j, :, :].shape)
    # elif len(data.shape) == 5:
    return np.ma.masked_where(np.isnan(result), result), regx, regy


def extract_coords(self, var, coord='lons'):
    """ Given a variable and a coordinate name (lons, lats) extract values
    related to given coordinate interval """
    var = var[:].squeeze()
    LOG.info("VAR SHAPE %s" % str(var.shape))
    if not self.subsetting:
        LOG.info("Not subsetting")
        return var[:], None
    cur_coord = self.__getattribute__(coord)
    LOG.info("Coord: %s, cur_coord: %s" % (coord, str(cur_coord)))
    if cur_coord:  # and len(cur_coord) in (2,3):
        if len(var.shape) == 2:
            if coord == 'lons':
                var1 = var[0]
            else:
                var1 = var[:, 0]
        else:
            var1 = var
        if strictly_increasing(var1[:]):
            idxs = np.where((var1[:] >= cur_coord[0]) &
                            (var1[:] <= cur_coord[-1]))
            LOG.info("idxs %s %s %s %s", str(idxs), var1.shape, len(idxs),
                     idxs[0].shape)
            return var1[idxs], idxs[0]
    LOG.info("Not subsetting")
    return var[:], None


def parse_parameters_list(plist):
    """ Parser for list parameter to be able to enter intervals and number of
    steps (examples: 0,1,2 0-6,2 ..."""
    if isinstance(plist, list) or isinstance(plist, tuple) or \
            isinstance(plist, np.ndarray):
        if len(plist) == 1:
            plist = plist[0]
        else:
            return list(plist)
    if str(plist).find('-') > 0:
        tmp = plist.strip('[]')
        try:
            rng, steps = tmp.split(',')
        except:
            rng = tmp
            steps = None
        start, end = [float(i.replace('m', '-')) if i.find('.') >= 0 else
                      int(i.replace('m', '-')) for i in rng.split('-')]
        if not steps:
            steps = (end-start)/10
        else:
            steps = float(steps)
        return list(np.arange(start, end+int(steps), steps))
    else:
        res = eval(str(plist).replace('m', '-'))
        if isinstance(res, int) or isinstance(res, float):
            return [res]
        return list(res)


def parse_parameter(var, val):
    """ Parameter parser """
    # parse numeric list arguments
    if var in ('lon', 'lat', 'timesteps', 'bounds', 'ticks'):
        if var == 'timesteps' and val in ('all', ['all']):
            return 'all'
        if val is not None:
            return parse_parameters_list(val)

    # parse float arguments
    elif var in ('xsize', 'ysize', 'dpi', 'fontsize', 'alpha'):
        if val:
            return eval(str(val))

    # parse simple list arguments
    elif var in ('coordsopts', 'coastsopts', 'countropts'):
        if val and isinstance(val, str):
            LOG.debug("%s: %s :: %s", var, val, type(val))
            return val.split(',')

    return val


def parse_parameters(params):
    """ Parser for parameters """
    ret = copy.deepcopy(params)
    for var in params:
        LOG.debug("%s: %s", var, params[var])
        val = parse_parameter(var, params[var])
        ret[var] = val
        LOG.debug("%s: %s", var, val)
    return ret


def parse_path(directory, dfile):
    """ Path parser """
    # print "Opening data file", f
    if os.path.isabs(dfile):
        return dfile
    else:
        LOG.debug("Input: %s", dfile)
        return os.path.join(directory, dfile)


class MapData(object):
    """Wrapper class to handle all the data needed to draw a map"""

    def __init__(self, **kwargs):
        LOG.info("map_data initializer")
        self.reset()
        self.max_reset()
        # Process optional arguments
        for dtype in ('map_data', 'wind_data', 'contour_data', 'scatter_data'):
            if dtype in kwargs:
                setattr(self, dtype, kwargs[dtype])

    def reset(self):
        self.map_data = None
        self.wind_data = None
        self.contour_data = None
        self.scatter_data = None

    def max_reset(self):
        self.max_data = None

    def set_grid_data(self, data):
        self.grid_data = data

    def set_map_data(self, data):
        self.map_data = data

    def set_max_data(self, data):
        self.max_data = data

    def set_wind_data(self, data):
        self.wind_data = data

    def set_contour_data(self, data):
        self.contour_data = data

    def set_scatter_data(self, data):
        self.scatter_data = data

    def get_grid_data(self):
        return self.grid_data

    def get_map_data(self):
        return self.map_data

    def get_wind_data(self):
        return self.wind_data

    def get_contour_data(self):
        return self.contour_data

    def get_max_data(self):
        return self.max_data

    def get_scatter_data(self):
        return self.scatter_data

    def has_map_data(self):
        return (self.map_data is not None)

    def has_wind_data(self):
        return (self.wind_data is not None)

    def has_contour_data(self):
        return self.contour_data is not None

    def has_max_data(self):
        return (self.max_data is not None)

    def has_scatter_data(self):
        return (self.scatter_data is not None)


class MapDataHandler(object):

    def __init__(self, sources, srcvars, indir, srcgaps, windsource, windopts,
                 lats, lons, transf, subsetting, dimension, **kwargs):
        self.ncdf = [[], []]  # list of lists, srcfiles and windfiles
        self.srcs = sources
        self.srcvars = srcvars
        self.srcgaps = srcgaps
        self.indir = indir
        self.windsrc = windsource
        self.windopts = windopts
        self.lats = lats
        self.lons = lons
        self.maxdata = None
        self.last_tstep = None
        self.transf = transf
        self.data = MapData()
        self.do_winds = False
        self.do_contours = False
        self.varconds = None
        self.grid = None
        self.grid_idxs = None
        self.subsetting = subsetting
        self.dimension = dimension

        if ('winds' in kwargs) \
                and (kwargs['winds']['src']) \
                and (kwargs['winds']['opts']):
            LOG.info("Will do winds")
            self.do_winds = True
            self.windsrc = kwargs['winds']['src']
            self.windopts = kwargs['winds']['opts']

        if ('contours' in kwargs) \
                and (kwargs['contours']['var']):
            LOG.info("Will do contours")
            self.do_contours = True
            self.contoursrc = self.srcs[0]
            self.contourvar = kwargs['contours']['var']

        if ('varconds' in kwargs):
            vcond = kwargs['varconds']
            if vcond:
                self.varconds = eval(vcond)

        # Open sources
        for sfile in self.srcs:
            fpath = parse_path(self.indir, sfile)
            fin = nc(fpath)
            self.ncdf[0].append(fin)

        for vname in fin.variables:
            if vname in ('longitude', 'lon', 'nav_lon'):
                x, x_idxs = extract_coords(self, fin.variables[vname])
            elif vname in ('latitude', 'lat', 'nav_lat'):
                y, y_idxs = extract_coords(self, fin.variables[vname],
                                           coord='lats')

        self.grid = (x, y)
        if x_idxs is not None and y_idxs is not None:
            self.grid_idxs = (x_idxs, y_idxs)

        # Open wind source if available
        for w in self.windsrc:
            LOG.info("WINDS: %s", w)
            wpath = parse_path(self.indir, w)
            LOG.info("WPATH: %s", wpath)
            self.ncdf[1].append(nc(wpath))

#        if self.transf:
#            self.ncdf.transf = self.transf

    def ncdf_reset(self):
        """ Closes netcdfs """
        # close src files and winds
        for f in self.ncdf[0]:
            f.close()
        for w in self.ncdf[1]:
            w.close()

    def dim_operation(self, srcvar, srcfile):
        """ Operations over dimensions """
        dim, oper = self.dimension.split(',')
        LOG.info("Dimension %s, operation or index/value: %s" % (dim, oper))
        dimidx = srcvar.dimensions.index(dim)
        # string
        try:
            return getattr(np, oper)(srcvar, dimidx)
        except:
            oper = eval(oper)
            # dimension index
            # if is int do nothing, retrieve dimension index
            # if dimension value find dimension index from the
            # variable with the same name of dimension
            if isinstance(oper, float):
                dimvar = srcfile.variables[dim][:]
                oper = np.abs(dimvar-oper).argmin()
            return np.take(srcvar, oper, axis=dimidx)

    def get_data_for_tstep(self, step):
        """ Get data per timestep """
        self.data.reset()
        # print "Getting map data for step ", step
        self.data.set_map_data(self.get_map_data_for_tstep(step))

        if self.do_winds:
            LOG.info("Getting wind data for step '%s'" % step)
            self.data.set_wind_data(self.get_wind_data_for_tstep(step))

        if self.do_contours:
            LOG.info("Getting contour data for step '%s'" % step)
            self.data.set_contour_data(self.get_contour_data_for_tstep(step))

        # Calculate maximum over data
        # FIXME should this step be optional?
#        if (self.data.has_max_data()):
#            self.data.set_max_data(maximum(self.data.get_max_data(),
#            self.data.get_map_data()))
#        else:
#            self.data.set_max_data(self.data.get_map_data())
#        self.last_tstep = step
        return self.data

    def get_current_max_data(self):
        '''Get current max data.
           NOTE: A call to this method will
           reset current max data, so it can be called only once! '''
        LOG.info("""Retrieving max (last calculated tstep: %d); this will reset
                 current MAX data!!""", self.last_tstep)
        max_data = MapData(map_data=self.data.get_max_data())
        self.data.max_reset()
        return max_data

    def get_map_data_for_tstep(self, step):
        """ Get map data for tstep """
        map_data = []
        for src_n in range(len(self.srcs)):
            tstep = int(step + self.srcgaps[src_n])
            LOG.info("TSTEP: %s", tstep)
            srcfile = self.ncdf[0][src_n]
            # TODO zoom on lat lon according to the domain
            # FIXME variable operations
#            if self.varconds and len(self.varconds)>=src_n:
#                varcond = self.varconds[src_n]
#                cond = varcond[0]
#                term = varcond[1]
#                vres = varcond[2]
#                if cond == '=':
#                    if tstep == int(term):
#                        expvar = vres
#                elif cond == '<=':
#                    if tstep <= int(term):
#                        expvar = vres
#                elif cond == '<':
#                    if tstep < int(term):
#                        expvar = vres
#                elif cond == '>=':
#                    if tstep >= int(term):
#                        expvar = vres
#                elif cond == '>':
#                    if tstep > int(term):
#                        expvar = vres

            # variable with possible expression to calculate
            expvar = self.srcvars[src_n]
            if expvar in srcfile.variables:
                srcvar = srcfile.variables[expvar]
                if self.dimension:
                    srcvar = self.dim_operation(srcvar, srcfile)
                if self.grid_idxs:
                    # if no expression
                    # LOG.info("SRCVAR: %s - GRID_IDXS: %s" %
                    # (str(srcvar.shape), str(self.grid_idxs)))
                    values = srcvar[tstep, :, :][self.grid_idxs[1],
                                                 :][:, self.grid_idxs[0]]
                else:
                    values = srcvar[tstep, :, :]
                LOG.info("1. SRCVAR: %s - GRID_IDXS: %s", str(values.shape),
                         str(self.grid_idxs))
            else:
                # otherwise search for a variable of the dataset into the
                # expression given
                for vname in srcfile.variables:
                    if vname in expvar:
                        expvar = expvar.replace(vname, 'newvar')
                        LOG.info("EXPVAR: %s", expvar)
                        srcvar = srcfile.variables[vname]
                        LOG.info("SRCVAR: %s", srcvar)
                        if self.dimension:
                            srcvar = self.dim_operation(srcvar, srcfile)
                        if self.grid_idxs:
                            newvar = srcvar[tstep, :, :][
                                self.grid_idxs[1], :][:, self.grid_idxs[0]]
                        else:
                            newvar = srcvar[tstep, :, :]
                        values = eval(expvar)
                        break
                LOG.info("2. SRCVAR: %s - GRID_IDXS: %s", str(values.shape),
                         str(self.grid_idxs))
            if map_data:
                # exp_res = self.ncdf.exp(EXPVAR)
                map_data.append(values)
            else:
                map_data = [values]

        return map_data

    def get_wind_data_for_tstep(self, tstep):
        """ Get wind data for tstep """
        wind_data = {'u': None, 'v': None}
        LOG.info("WINDOPTS: %s" % str(self.windopts))
        srcfile = self.ncdf[1][0]
        srcvar_u = srcfile.variables[self.windopts[0]]
        srcvar_v = srcfile.variables[self.windopts[1]]
        if self.dimension:
            srcvar_u = self.dim_operation(srcvar_u, srcfile)
            srcvar_v = self.dim_operation(srcvar_v, srcfile)
        if self.grid_idxs:
            wind_data['u'] = srcvar_u[tstep, :, :][self.grid_idxs[1],
                                                   :][:, self.grid_idxs[0]]
            wind_data['v'] = srcvar_v[tstep, :, :][self.grid_idxs[1],
                                                   :][:, self.grid_idxs[0]]
        else:
            wind_data['u'] = srcvar_u[tstep, :, :]
            wind_data['v'] = srcvar_v[tstep, :, :]
        if len(self.windopts) == 4:
            wind_data['barbs'] = self.windopts[3]
        return wind_data

    def get_contour_data_for_tstep(self, tstep):
        """ Get contour data for tstep """
        cdata = None
        LOG.info("Contours variable: %s" % self.contourvar)
        srcfile = self.ncdf[0][0]
        srcvar = srcfile.variables[self.contourvar]
        if self.dimension:
            srcvar = self.dim_operation(srcvar, srcfile)
        if self.grid_idxs:
            cdata = srcvar[tstep, :, :][self.grid_idxs[1],
                                        :][:, self.grid_idxs[0]]
        else:
            cdata = srcvar[tstep, :, :]
        return cdata

    def get_scatter_data_for_tstep(self, tstep):
        """ """
        LOG.info("Scatter variable: %s" % self.scatter)
        srcfile = self.ncdf[0][0]
        srcvar = srcfile.variables[self.contourvar]
        if self.dimension:
            srcvar = self.dim_operation(srcvar, srcfile)
        if self.grid_idxs:
            cdata = srcvar[tstep, :, :][self.grid_idxs[1],
                                        :][:, self.grid_idxs[0]]
        else:
            cdata = srcvar[tstep, :, :]
        return cdata

    def get_dims(self):
        LOG.info("Getting dimensions from file '%s'" % self.srcs[0])
        # self.ncdf.cmd("set dfile 1")
        for vname in self.ncdf[0][0].variables:
            if vname in ('time', 'time_counter'):
                tvar = vname
        time = self.ncdf[0][0].variables[tvar]
        try:
            typ, _, dat, tim = time.units.split()[:4]
        except:
            typ, _, dat = time.units.split()[:3]
            tim = "00:00:00"
        tdata = time[:]
        tim = tim.split('.')[0]
        tfmt = '%HZ%d%b%Y'
        try:
            dtime = datetime.strptime("%s %s" % (dat, tim), '%Y-%m-%d %H:%M:%S')
        except:
            dtime = datetime.strptime("%s %s" % (dat, tim), '%Y-%m-%d %H:%M')
        if typ == 'minutes':
            cdate = {(np.where(tdata == i)[0][0], (dtime +
                                                   timedelta(minutes=int(i))).strftime(tfmt))
                     for i in tdata}
        elif typ == 'seconds':
            cdate = {(np.where(tdata == i)[0][0], (dtime +
                                                   timedelta(seconds=int(i))).strftime(tfmt))
                     for i in tdata}
        else:  # typ == 'hours':
            cdate = {(np.where(tdata == i)[0][0], (dtime +
                                                   timedelta(hours=int(i))).strftime(tfmt))
                     for i in tdata}
        return dict(cdate)


class DataFrameHandler(object):
    """ Clase to handle dataframes """

    def __init__(self, dframe, separator=',', ):
        if isinstance(dframe, str):
            LOG.debug("opening '%s'" % dframe)
            self.reader = pd.read_csv(dframe, sep=separator, parse_dates=True)
        else:
            self.reader = dframe

    def filter(self, **kwargs):
        """ Filtering dataframes """

        latcol = 'latcol' in kwargs and kwargs['latcol'] or 'lat'
        loncol = 'loncol' in kwargs and kwargs['loncol'] or 'lon'
        colcol = 'colcol' in kwargs and kwargs['colcol'] or 'color'
        datecol = 'datecol' in kwargs and kwargs['datecol'] or 'date'
        sizecol = 'sizecol' in kwargs and kwargs['sizecol'] or 'size'

        ret = {}

        if isinstance(self.reader, dict):
            self.reader = pd.DataFrame(self.reader)

        self.reader = self.reader.dropna()

        if datecol not in self.reader.columns:
            return dict(self.reader)

        gdf = self.reader.groupby(datecol)
        for gname in gdf.groups:
            group = gdf.get_group(gname)
            if isinstance(gname, str):
                dtime = datetime.strptime(gname, "%Y-%m-%d %H:%M:00")
            else:
                dtime = gname.to_pydatetime()
            ret[dtime] = group[[loncol, latcol, colcol, sizecol]]
        # LOG.info('filtering on date: %s and hour %s', date, hour)
        return ret


class DataTransform(object):
    """ Data transform"""
    @staticmethod
    def set_color_from_buckets(colors, bounds, values):
        '''Returns a vector of the same size as values,
        containing a value picked from colors when the
        current value falls in a bucket as specified in
        bounds.

        Colors and bounds must have the same size'''

        LOG.info('bounds: %s' % bounds)
        LOG.info('colors: %s' % colors)
        LOG.info('values: %s' % values)

        if len(colors) != len(bounds) + 1:
            raise Exception("Wrong size for colors/bounds")

        out = []

        for idx in range(0, len(values)):
            LOG.info("processing %s" % str(values[idx]))
            if values[idx] < bounds[0]:
                out.append(colors[0])
            elif values[idx] >= bounds[len(bounds) - 1]:
                out.append(colors[len(colors) - 1])
            else:
                for bidx in range(0, len(bounds) - 1):
                    if values[idx] >= bounds[bidx] and \
                            values[idx] < bounds[bidx + 1]:
                        out.append(colors[bidx + 1])

        LOG.info("data transform output: %s" % str(out))
        return out


class MapDrawOptions(object):
    """ Map draw options """

    def __init__(self, loglevel='INFO', **kwargs):
        LOG.setLevel(loglevel)
        ## General Options
        self.area_thresh = None      # Default area threshold for maps
        self.resolution = None       # Default resolution is intermediate
        self.xsize = '1.'              # (when keep_aspect = False) Default horizontal size [value between 0 and 1]
        self.ysize = '1.'              # (when keep_aspect = False) Default vertical size [value between 0 and 1]              # Default DPI
        self.coordsopts = ".3,8,grey"
        self.coastsopts = ".5,grey"
        self.countropts = ".3,grey"

        self.save = True
        self.subplot = None

        self.boundinglat = None

        ## FILLED COUNTOUR OPTIONS

        ## AIR QUALITY OPTIONS
        self.limits = []         # Default is no limits arrows

        ## WINDS OPTIONS
        self.wind_units = 'inches'    # Wind arrow default unit
        self.wind_scale = 40          # Wind arrow scale default
        self.wind_head_length = 10    # Wind arrowhead length default
        self.wind_head_width = 8     # Wind arrowhead width default
        self.wind_width = 0.008       # Wind arrow width default
        self.wind_minshaft = 0.25     # Wind arrow minimum shaft default
        self.wind_label_xpos = 0.8     # Wind label x position (relative to quiver plot)
        self.wind_label_ypos = -0.075  # Wind label y position (relative to quiver plot)
        self.wind_label_scale = 20     # Size of the label (represents m/s)

        # CONTOUR OPTIONS
        self.contours_int = 1      # Default contour interval
        self.contours_color = 'k'  # Default contour color
        self.contours_linewidth = 0.8   # Default line width for contours
        self.contours_label = False  # if True labels of contours are showed
        self.contours_label_fontsize = 13   # Default font size for contour label
        self.contours_label_format = '%d'   # Default format for contour label
        self.contours_exclude_vals = [0]    # Default list of values to exclude from drawing

#        self.nocontourf = False # if True contourf is hidden
#        self.nomap = False # if True map is hidden
#        self.nointerp = False # if False use contourf, else pcolor

        # SHAPEFILES
        self.shapefiles = []            # Default shapefiles list is empty
        self.shapef_width_init = 0.75   # Initial line width for shapefiles
        self.shapef_width_step = 0.25   # Line width difference between two consecutive shapefiles

        LOG.setLevel(loglevel)

    def has_shape_files(self):
        return (len(self.shapefiles) > 0)

    def has_limits(self):
        return (len(self.limits) > 0)


class MapGenerator(object):
    """ Root class for plotting"""

    def __init__(self, **kwargs):
        """ Initialize MapGenerator with attributes common to all the plotting
        services """
        self.mgplot         = kwargs.get('mgplot', None)
        self.mgaxis         = kwargs.get('mgaxis', None)
        self.indir          = kwargs.get('indir', '.')
        self.outdir         = kwargs.get('outdir', '.')
        self.srcgaps        = kwargs.get('srcgaps', [0])
        self.title          = kwargs.get('title', '')
        self.fontsize       = kwargs.get('fontsize', 10)
        self.loglevel       = kwargs.get('loglevel', 'WARNING')
        self.orig_projection = kwargs.get('orig_projection', 'PlateCarree')
        self.orig_projection_kwargs = kwargs.get('orig_projection_kwargs', dict())
        self.projection     = kwargs.get('projection', 'PlateCarree')
        self.projection_kwargs = kwargs.get('projection_kwargs', dict())
        self.subsetting     = kwargs.get('subsetting', True)
        self.dimension      = kwargs.get('dimension', None)
        self.continents     = kwargs.get('continents', None)
        self.transf         = kwargs.get('transf', False)
        self.scatter        = kwargs.get('scatter', None)
        self.logo           = kwargs.get('logo', None)
        self.overwrite      = kwargs.get('overwrite', True)
        self.anim           = kwargs.get('anim', False)
        self.anim_delay     = kwargs.get('anim_delay', 25)
        self.img_template   = kwargs.get('img_template', '')
        self.joint_template = kwargs.get('joint_template', '')
        self.varconds       = kwargs.get('varconds', None)
        self.filefmt        = kwargs.get('filefmt', 'png')
        self.config_dir     = kwargs.get('config_dir', \
                                os.path.join(os.environ['HOME'], '.mapgenerator'))
        self.config_file    = kwargs.get('config_file', 'config.cfg')
        self.alpha          = kwargs.get('alpha', None)
        self.shapefiles     = kwargs.get('shapefiles', None)
        self.dpi = kwargs.get('dpi', 200)

    @staticmethod
    def _get_default_title(cube):
        if cube.attributes.get('plot_name', None):
            show_name = cube.attributes['plot_name']
        elif cube.long_name and len(cube.long_name) < 45:
            show_name = cube.long_name
        elif cube.standard_name and len(cube.standard_name) < 45:
            show_name = cube.standard_name
        else:
            show_name = cube.var_name
        return f"{show_name} ({cube.units})"


class MapCross(MapGenerator):
    """ Define common attributes to maps and cross sections """

    def __init__(self, loglevel='INFO', **kwargs):
        """ Initialize class with MapGenerator attributes plus some others """
        LOG.setLevel(loglevel)
        MapGenerator.__init__(self, **kwargs)
        self.bounds         = kwargs.get('bounds', None)
        self.ticks          = kwargs.get('ticks', None)
        self.colors         = kwargs.get('colors', 'jet')
        self.bad            = kwargs.get('bad', None)
        self.N              = kwargs.get('N', None)
        self.lat            = kwargs.get('lat', [])
        self.lon            = kwargs.get('lon', [])
        self.wind           = kwargs.get('wind', [])
        self.windopts       = kwargs.get('windopts', [])
        self.contours       = kwargs.get('contours', None)
        self.contours_color = kwargs.get('contours_color', None)
        self.contours_label = kwargs.get('contours_label', None)
        self.contours_int   = kwargs.get('contours_int', 1)
        self.smooth         = kwargs.get('smooth', False)
        self.colorbar       = kwargs.get('colorbar', True)
        self.formats        = kwargs.get('formats', None)
        self.noruntime      = kwargs.get('noruntime', False)
        self.timesteps      = kwargs.get('timesteps', '0')
        self.limits         = kwargs.get('limits', None)
