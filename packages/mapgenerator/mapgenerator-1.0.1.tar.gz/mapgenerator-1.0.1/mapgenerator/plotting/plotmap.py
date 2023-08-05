# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Barcelona Supercomputing Center
# @license: https://www.gnu.org/licenses/gpl-3.0.html
# @author: see AUTHORS file

import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from matplotlib.cbook import delete_masked_points
from matplotlib.path import Path
# from matplotlib.image import imread
import numpy as np
from datetime import datetime
import os.path
import subprocess
from collections import Iterable
from PIL import Image
from .definitions import MapData
from .definitions import MapCross
from .definitions import MapDrawOptions
from .definitions import MapDataHandler
from .definitions import DataFrameHandler
from .definitions import is_grid_regular
from .definitions import do_interpolation
from .definitions import parse_parameter
from .definitions import parse_parameters
from .definitions import parse_parameters_list
from .definitions import parse_path
from .tools import set_title
from .tools import set_resolution
from .tools import gen_kml
from .tools import gen_anim
# try:
#     from urllib2 import urlopen
# except ImportError:
#     from urllib.request import urlopen
import copy
from glob import glob
import logging

mpl.use('Agg')
LOG = logging.getLogger(__name__)


class PlotCross(object):
    """ Main class for plotting cross sections """

    def __init__(self, loglevel='WARNING', **kwargs):
        pass


class PlotMap(MapCross, MapDrawOptions):
    """ Main class for plotting maps """

    def __init__(self, loglevel='WARNING', **kwargs):
        """ Initialize class with attributes """
        MapCross.__init__(self, loglevel, **kwargs)
        MapDrawOptions.__init__(self, loglevel, **kwargs)
        self.nocontourf = False
        self.maxdata = False
        self.maxtitle = None
        self.nomap = False
        self.background = False
        self.extend = 'neither'
        self.kml = False
        self.kmz = False
        self.norm = None
        self.cmap = None
        self._orig_crs = ccrs.PlateCarree()
        self._crs = ccrs.PlateCarree()
        self.mgaxis = None
        self.mgplot = None
        self.stamen_terrain = None
        self.zoom_level = None
        # self.map = None   #Map
        self.first_image = False  # Is is the first image of the batch?
        self.map_name = None  # name of the figure to map animation colors
#        self.drawopts = {'coastlines':
#                            {'linewidth': 0.5, 'color': 'grey', },
#                         'countries':
#                            {'linewidth': 0.3, 'color': 'grey', },
#                        }

    def __setattr__(self, key, value):
        LOG.debug("SETATTR: %s - %s", key, value)
        super(PlotMap, self).__setattr__(key, parse_parameter(key, value))

    def _build_orig_projection(self):
        self._orig_crs = getattr(ccrs, self.orig_projection)(
            **self.orig_projection_kwargs)

    def _build_projection(self):
        if self.background:
            import cartopy.io.img_tiles as cimgt
            self.stamen_terrain = cimgt.Stamen('terrain-background')
            self._crs = self.stamen_terrain.crs
            self.projection = 'Stamen'
        else:
            self._crs = getattr(ccrs, self.projection)(
                **self.projection_kwargs)

    def set_color_map(self):
        """ Create color map """

        extend_opts = {
            'max': {
                'cmap_arg': lambda colors: colors[:-1],
                'cmap_ext': ('set_over'),
                'ext_arg': (lambda colors: colors[-1]),
                'norm_arg': (lambda bounds: bounds+[np.inf],
                             lambda cmap: cmap.N+1)
            },
            'min': {
                'cmap_arg': lambda colors: colors[1:],
                'cmap_ext': ('set_under'),
                'ext_arg': (lambda colors: colors[0]),
                'norm_arg': (lambda bounds: [-np.inf]+bounds,
                             lambda cmap: cmap.N+1)
            },
            'both': {
                'cmap_arg': self.colors[1:-1],
                'cmap_ext': ('set_over', 'set_under'),
                'ext_arg': (lambda colors: colors[-1],
                            lambda colors: colors[0]),
                'norm_arg': (lambda bounds: [-np.inf]+bounds+[np.inf],
                             lambda cmap: cmap.N + 2)

            }
        }

        if not isinstance(self.colors, str) and \
                isinstance(self.colors, Iterable):
            # adjust number of colors to number of bounds
            if self.bounds:
                if self.extend in ('min', 'max'):
                    if len(self.bounds) < len(self.colors):
                        self.colors = self.colors[:len(self.bounds)]
                elif self.extend == 'both':
                    if len(self.bounds)+1 < len(self.colors):
                        self.colors = self.colors[:len(self.bounds)+1]

            if self.extend in extend_opts:
                self.cmap = mpl.colors.ListedColormap(
                    extend_opts[self.extend]['cmap_arg'](self.colors))
                for ext, arg in zip(extend_opts[self.extend]['cmap_ext'],
                                    extend_opts[self.extend]['ext_arg']):
                    getattr(self.cmap, ext)(arg(self.colors))
            else:
                self.cmap = mpl.colors.ListedColormap(self.colors)
            custom_cmap = True
        else:
            try:
                if self.N:
                    self.cmap = mpl.cm.get_cmap(self.colors, self.N)
                else:
                    self.cmap = mpl.cm.get_cmap(self.colors)
            except ValueError:
                self.cmap = mpl.cm.get_cmap('jet')
            custom_cmap = False

        if self.bad:
            self.cmap.set_bad(self.bad)

        if self.background or self.kml or self.kmz:
            if self.extend in ('min', 'both'):
                self.cmap.set_under(color=(0, 0, 0, 0))
            else:
                self.cmap.colors = [(0, 0, 0, 0), ] + [c for c in
                                                       self.cmap.colors[1:]]

        # normalize colormap
        if self.bounds and self.smooth and not custom_cmap:
            if self.extend in ('min', 'max', 'both'):
                self.norm = mpl.colors.BoundaryNorm(
                    extend_opts[self.extend]['norm_arg'][0](self.bounds),
                    extend_opts[self.extend]['norm_arg'][1](self.cmap)
                )
            else:
                self.norm = mpl.colors.BoundaryNorm(self.bounds, self.cmap.N)
        elif self.bounds:
            self.norm = mpl.colors.BoundaryNorm(self.bounds, self.cmap.N)

    def set_color_bar(self, mco, location='right', drawedges=False, cax=None):
        """ Create color bar """
#        xs = self.xsize
#        nap = .8-((1-xs)*0.4)
#        a = plt.axes([nap, 0, .14, 1])#, frameon=False)
#        plt.axis('off')
        mpl.rcParams['axes.linewidth'] = 0.1
        mpl.rcParams['axes.formatter.useoffset'] = False
        if self.ticks:
            LOG.debug("ticks %s" % str(self.ticks))
            self.ticks = parse_parameters_list(self.ticks)
        elif self.bounds:
            self.ticks = self.bounds
        elif hasattr(mco, 'levels'):
            self.ticks = mco.levels

        LOG.debug("***** Formats: %s *****", self.formats)
        cax, kwargs = mpl.colorbar.make_axes(self.mgaxis, location=location,
                                             pad=0.02, shrink=0.8)
        cbar = self.mgplot.colorbar(mco, cax=cax, ax=self.mgaxis,
                                    ticks=self.ticks, format=self.formats,
                                    pad=.06, extend=self.extend,
                                    drawedges=drawedges, **kwargs)

        cbar.ax.tick_params(labelsize=float(self.coordsopts[1]))
        for lin in cbar.ax.yaxis.get_ticklines():
            lin.set_visible(False)

        # If required, draw arrow pointing to the specified limits
        if self.has_limits():
            # The following two values are absolute
            shrink = 0.75
            upper = 0.863 - 0.45 * (0.8 - shrink)  # formula seems to work ok
            lower = 0.137 + 0.45 * (0.8 - shrink)
            span = upper - lower
            arrows = self.limits

            if self.bounds:
                ticks = self.bounds
            else:
                ticks = mco.levels

            fac = span/float(len(ticks) - 1)
            for i in arrows:
                for j in range(0, len(ticks) - 1):
                    if i >= ticks[j] and i <= ticks[j+1]:
                        if i == ticks[j+1]:
                            idx = j+1
                            add = 0
                        else:
                            idx = j
                            add = (float(i - ticks[j])/float(ticks[j+1] -
                                                             ticks[j]))*fac
                        pos = fac*idx + lower
                        plt.arrow(0.88, pos + add, 0.10, 0,
                                  length_includes_head=True, head_length=0.10,
                                  head_width=0.025, fill=True, color='k')
        # plt.colorbar(drawedges=drawedges, cax=cax, ticks=self.bounds)

    def init_map(self, grid):
        """ Initialize a map. Initialization should be performed only once
        the beginning of a serie of images """
        glon, glat = grid
        # print("***",self.lon, self.lat,"***")
        if not self.lat:  # or len(self.lat) not in (2,3):
            self.lat = "%s-%s" % (str(round(glat.min(), 1)).replace('-', 'm'),
                                  str(round(glat.max(), 1)).replace('-', 'm'))

        if not self.lon:  # or len(self.lon) not in (2,3):
            self.lon = "%s-%s" % (str(round(glon.min(), 1)).replace('-', 'm'),
                                  str(round(glon.max(), 1)).replace('-', 'm'))

        self._build_orig_projection()
        self._build_projection()
        # print(self.lon, self.lat)
#        # Fix the printout of tick values to avoid .0 decimals in integers
#        strs = []
#        if self.bounds:
#            for b in self.bounds:
#                if (b == int(b)):
#                    strs.append("%d" % b)
#                else:
#                    strs.append(str(b))
#
        # Set the colormap
        self.set_color_map()
        if not self.resolution:
            self.resolution, self.zoom_level = \
                    set_resolution(self.lon, self.lat)
        else:
            _, self.zoom_level = set_resolution(self.lon, self.lat)

        self.first_image = True

    def gen_image_map(self, fig_name, grid, data, img_title,
                      cur_scatter_data=None, **kwargs):
        """ Generate image map """

        # overwrite option
        if os.path.exists(fig_name + ".png") and not self.overwrite:
            LOG.info(fig_name, " already exists.")
            if self.subplot is None:
                plt.clf()
            return fig_name

        map_data = data.map_data
        # FIXME
        scatter_data = data.scatter_data or cur_scatter_data
        # if self.subplot is None:
        #    self.mgplot.clear()

#        params = {
#             'font.size': 14,
#             'text.fontsize': 28,
#             'axes.titlesize': 11,
#             'savefig.dpi': self.dpi
#        }
#
#        mpl.rcParams.update(params)

        # Draw filled contour
        self.mgaxis.set_aspect(self.xsize/self.ysize)

        if self.projection.lower().endswith('polarstereo'):
            self.mgaxis.set_extent([-180, 179.9999999999999,
                                    self.lat[0], self.lat[-1]],
                                   self._orig_crs)
            # Compute a circle in axes coordinates, which we can use as a
            # boundary for the map. We can pan/zoom as much as we like - the
            # boundary will be permanently circular.
            theta = np.linspace(0, 2*np.pi, 100)
            center, radius = [0.5, 0.5], 0.5
            verts = np.vstack([np.sin(theta), np.cos(theta)]).T
            circle = Path(verts * radius + center)
            self.mgaxis.set_boundary(circle, transform=self.mgaxis.transAxes)
        else:
            self.mgaxis.set_extent([self.lon[0], self.lon[-1],
                                    self.lat[0], self.lat[-1]],
                                   self._orig_crs)

#            if self.subplot:
#                self.map = Basemap(
#                    ax=self.mgaxis,
#                    projection=self.projection, resolution=self.resolution,
#                    llcrnrlon=self.lon[0], llcrnrlat=self.lat[0],
#                    urcrnrlon=self.lon[-1], urcrnrlat=self.lat[-1],
#                    lon_0=lon_0, lat_0=lat_0,
#                    fix_aspect=self.keep_aspect,
#                    area_thresh=self.area_thresh,
#                    boundinglat=self.boundinglat,
#                )
#            else:
#                self.map = Basemap(
#                    projection=self.projection, resolution=self.resolution,
#                    llcrnrlon=self.lon[0], llcrnrlat=self.lat[0],
#                    urcrnrlon=self.lon[-1], urcrnrlat=self.lat[-1],
#                    lon_0=lon_0, lat_0=lat_0,
#                    fix_aspect=self.keep_aspect,
#                    area_thresh=self.area_thresh,
#                    boundinglat=self.boundinglat,
#                )

        glon, glat = grid
        LOG.debug("0. GLON: %s, GLAT: %s", str(glon.shape), str(glat.shape))

        if len(glon.shape) == 1 and len(glat.shape) == 1:
            glon, glat = np.meshgrid(glon, glat)

        LOG.debug("1. GLON: %s, GLAT: %s", str(glon.shape), str(glat.shape))

        # if curvilinear grid do interpolation, return already gridded coords
        if not is_grid_regular(glon, glat):
            map_data[0], glon, glat = do_interpolation(map_data[0], glon, glat)

        LOG.info("2. GLON: %s, GLAT: %s", str(glon.shape), str(glat.shape))

#        if not self.nomap:
#            x, y = self.map(*(glon, glat))
#        else:
        xloc, yloc = glon, glat

        LOG.info("3. GLON: %s, GLAT: %s", str(xloc.shape), str(yloc.shape))
#        print "map_data", map_data[0].shape

        # self.print_time("meshgrid")
        # LOG.info("X: %s, Y: %s" % (str(x.shape), str(y.shape)))

#        # nomap option
#        if self.nomap and os.path.exists("%s-%s/%s.png" % (run_date, var_name,
#        fig_name)) and not self.overwrite:
#            print fig_name, " already exists."
#            plt.clf()
#            return fig_name

        if self.nomap:
            self.mgplot.frameon = False

#         if self.alpha is not None and self.bounds is not None:
#             if self.extend in ('min', 'both'):
#                 map_data[0] = np.ma.masked_where(map_data[0] <
#                 self.bounds[0], map_data[0])
#             else:
#                 map_data[0] = np.ma.masked_where((map_data[0] >=
#                                                   self.bounds[0]) &
#                                                  (map_data[0] <
#                                                   self.bounds[1]),
#                                                  map_data[0])

        mco = None

        LOG.info(type(map_data[0]))
        map_data[0] = np.ma.filled(map_data[0], np.nan)
        LOG.info(type(map_data[0]))

#        if not self.nocontourf and not self.nomap and self.smooth:
#            LOG.info("X: %s, Y: %s, DATA: %s" % (x.shape, y.shape,
#            map_data[0]))
#            mco = self.map.contourf(x, y,
#                                    map_data[0],
#                                    cmap=self.cmap,
#                                    norm=self.norm,
#                                    levels=self.bounds,
#                                    extend=self.extend,
#                                    horizontalalignment='center',
#                                    alpha=self.alpha,
#                                    antialiased=True)
#
#        elif not self.nocontourf and not self.nomap and not self.smooth:
#            LOG.info("X: %s, Y: %s, DATA: %s" % (x.shape, y.shape,
#            map_data[0]))
#            mco = self.map.pcolormesh(x, y,
#                                      map_data[0],
#                                      cmap=self.cmap,
#                                      norm=self.norm,
#                                      alpha=self.alpha,
#                                      antialiased=True)

        if not self.nocontourf and self.smooth:
            mco = self.mgaxis.contourf(xloc, yloc,
                                       map_data[0],
                                       cmap=self.cmap,
                                       norm=self.norm,
                                       levels=self.bounds,
                                       extend=self.extend,
                                       alpha=self.alpha,
                                       transform=self._orig_crs,
                                       antialiased=True)

        elif not self.nocontourf and not self.smooth:
            mco = self.mgaxis.pcolormesh(xloc, yloc,
                                         map_data[0],
                                         cmap=self.cmap,
                                         norm=self.norm,
                                         alpha=self.alpha,
                                         transform=self._orig_crs,
                                         antialiased=True)

        # Draw shape files
        if self.has_shape_files():
            line_w = float(self.countropts[0])
            for shapef in self.shapefiles:
                LOG.info("Processing shape file: %s with line width: %s",
                         shapef, line_w)
                adm1_shapes = list(shpreader.Reader(shapef).geometries())
                self.mgaxis.add_geometries(adm1_shapes, self._crs,
                                           linewidth=line_w,
                                           edgecolor=self.countropts[1])
                # self.map.readshapefile(shapef, "%s" %
                # os.path.basename(shapef), linewidth=line_w,
                # color=self.countropts[1])
                line_w = max(self.shapef_width_step, line_w -
                             self.shapef_width_step)

        # FIXME Modify to use scatter inside DATA
        # if DATA.hasScatterData()... etc...
        if scatter_data is not None:
            LOG.info("Plotting scatter data: %s of keys %s",
                     str(scatter_data), str(scatter_data.keys()))
            if mco and self.bounds:
                self.mgaxis.scatter(scatter_data['lon'].tolist(),
                                    scatter_data['lat'].tolist(),
                                    s=scatter_data['size'].tolist(),
                                    c=scatter_data['color'].tolist(),
                                    marker='o',
                                    linewidth=0.3,
                                    vmin=self.bounds[0],
                                    vmax=self.bounds[-1],
                                    cmap=self.cmap,
                                    norm=self.norm,
                                    transform=self._orig_crs,
                                    zorder=10)
            elif mco:
                self.mgaxis.scatter(scatter_data['lon'].tolist(),
                                    scatter_data['lat'].tolist(),
                                    s=scatter_data['size'].tolist(),
                                    c=scatter_data['color'].tolist(),
                                    marker='o',
                                    linewidth=0.3,
                                    cmap=self.cmap,
                                    norm=self.norm,
                                    transform=self._orig_crs,
                                    zorder=10)
            elif self.bounds:
                mco = self.mgaxis.scatter(scatter_data['lon'].tolist(),
                                          scatter_data['lat'].tolist(),
                                          s=scatter_data['size'].tolist(),
                                          c=scatter_data['color'].tolist(),
                                          marker='o',
                                          linewidth=0.3,
                                          vmin=self.bounds[0],
                                          vmax=self.bounds[-1],
                                          cmap=self.cmap,
                                          norm=self.norm,
                                          transform=self._orig_crs,
                                          zorder=10)
            else:
                mco = self.mgaxis.scatter(scatter_data['lon'].tolist(),
                                          scatter_data['lat'].tolist(),
                                          s=scatter_data['size'].tolist(),
                                          c=scatter_data['color'].tolist(),
                                          marker='o',
                                          linewidth=0.3,
                                          cmap=self.cmap,
                                          norm=self.norm,
                                          transform=self._orig_crs,
                                          zorder=10)

        if data.wind_data:
            winds = data.wind_data
            x_vec, y_vec, u_vec, v_vec = delete_masked_points(
                xloc.ravel(),
                yloc.ravel(),
                winds['u'].ravel(),
                winds['v'].ravel()
            )

            if 'barbs' in winds:
                self.mgaxis.barbs(x_vec, y_vec, u_vec, v_vec,
                                  units=self.wind_units,
                                  headlength=self.wind_head_length,
                                  headwidth=self.wind_head_width,
                                  width=self.wind_width,
                                  minshaft=self.wind_minshaft,
                                  scale=self.wind_scale,
                                  transform=self._orig_crs,
                                  color='k')
            else:
                quiv = self.mgaxis.quiver(x_vec, y_vec, u_vec, v_vec,
                                          units=self.wind_units,
                                          headlength=self.wind_head_length,
                                          headwidth=self.wind_head_width,
                                          width=self.wind_width,
                                          minshaft=self.wind_minshaft,
                                          scale=self.wind_scale,
                                          transform=self._orig_crs,
                                          color='gray')
                # Draw the key
                plt.quiverkey(quiv,
                              self.wind_label_xpos,
                              self.wind_label_ypos,
                              self.wind_label_scale,
                              label='%s m/s' % self.wind_label_scale,
                              coordinates='axes',
                              labelpos='S', labelsep=0.05)

        if data.contour_data:
            interval = self.contours_int
            exclude = self.contours_exclude_vals
            clow_bound = -99999
            cupp_bound = 99999
            cdata = data.contour_data
            try:
                # cmin = min(filter (lambda a: a > clow_bound, cdata.ravel()))
                cmin = cdata.where(cdata > clow_bound).min()
                adjcmin = int(cmin - (cmin % interval) - interval * 2)
            except ValueError:
                cmin = 0
            try:
                # cmax = max(filter (lambda a: a < cupp_bound, cdata.ravel()))
                cmax = cdata.where(cdata < cupp_bound).max()
                adjcmax = int(cmax - (cmax % interval) + interval * 2)
            except ValueError:
                cmax = 0
            lvls = np.arange(adjcmin, adjcmax, interval)
            for exc in exclude:
                lvls = [exc for exc in lvls if exc != 0]
            if (len(lvls) > 0) and map_data is not None:
                mco = plt.contourf(xloc, yloc,
                                   map_data[0],
                                   cmap=self.cmap,
                                   norm=self.norm,
                                   levels=self.bounds,
                                   extend=self.extend,
                                   horizontalalignment='center',
                                   alpha=self.alpha)

            if map_data is not None and (map_data[0] == cdata).all():
                LOG.debug(":::::::::::::::::::::: SAME !!! ::::::::::::::::")
                mcs = plt.contour(xloc, yloc,
                                  cdata,
                                  levels=self.bounds,
                                  colors=self.contours_color,
                                  linewidths=self.contours_linewidth,
                                  alpha=self.alpha)
            else:
                LOG.debug(":::::::::::::::::::: DIFFERENT !!! :::::::::::::")
                LOG.debug("MIN: %s - MAX: %s", cmin, cmax)
                mcs = plt.contour(xloc, yloc,
                                  cdata,
                                  levels=lvls,
                                  colors=self.contours_color,
                                  linewidths=self.contours_linewidth,
                                  alpha=self.alpha)

            if self.contours_label:
                self.mgplot.clabel(mcs,
                                   inline=1,
                                   fontsize=self.contours_label_fontsize,
                                   # backgroundcolor='r',
                                   fmt=self.contours_label_format)

        # coords normalization
#        lat_offset = abs(self.lat[0]) % self.lat[2]
#        lon_offset = abs(self.lon[0]) % self.lon[2]

        if not self.nomap and not self.kml and not self.kmz:

            if self.continents:
                self.mgaxis.add_feature(cfeature.LAND, color=self.continents,
                                        zorder=10)

            self.mgaxis.coastlines(resolution=self.resolution,
                                   linewidth=float(self.coastsopts[0]),
                                   color=str(self.coastsopts[1]),
                                   zorder=15)

            self.mgaxis.add_feature(cfeature.BORDERS
                                    .with_scale(self.resolution),
                                    linewidth=float(self.countropts[0]),
                                    edgecolor=str(self.countropts[1]),
                                    zorder=15)

            draw_labels = bool(self.projection == 'PlateCarree')

            grl = self.mgaxis.gridlines(xlocs=self.lon, ylocs=self.lat,
                                        crs=self._crs,
                                        draw_labels=draw_labels,
                                        linestyle='--',
                                        linewidth=float(self.coordsopts[0]),
                                        color=str(self.coordsopts[2]),
                                        zorder=20)

            if draw_labels:
                grl.xlabels_top = False
                grl.ylabels_right = False
                grl.xlabel_style = {'size': float(self.coordsopts[1])}
                grl.ylabel_style = grl.xlabel_style

        # Change axes for colorbar
        if self.colorbar and not self.kml and not self.kmz and \
           (not self.nocontourf or scatter_data is not None):
            self.set_color_bar(mco)

        if self.background:
            self.mgaxis.add_image(self.stamen_terrain, self.zoom_level)
#        if self.background == 'shadedrelief':
#        #m.bluemarble()
#        if self.background == 'shadedrelief':
#            self.map.shadedrelief()
#        if self.background == 'bluemarble':
#            self.map.bluemarble()
#        if self.background == 'etopo':
#            self.map.etopo()
#        if self.background == 'GIS':
#            h0 = float(self.lat[-1] - self.lat[0])
#            w0 = float(self.lon[-1] - self.lon[0])
#            ff = h0/w0      # form factor
#            height = 1024*ff       # height
#            size = "%d,%d" % (1024, height)
#            basemap_url =
#            "http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?\
# bbox=%s,%s,%s,%s&\
# bboxSR=4326&\
# imageSR=4326&\
# size=%s&\
# dpi=%d&\
# format=png24&\
# f=image" % (self.lon[0], self.lat[0], self.lon[-1], self.lat[-1], size,
# self.dpi) self.map.imshow(imread(urlopen(basemap_url)), origin='upper')

        # logo
        if self.logo:
            img = Image.open(self.logo[0])
#            height = im.size[1]
#            width  = im.size[0]

            # We need a float array between 0-1, rather than
            # a uint8 array between 0-255
            nim = np.array(img).astype(np.float) / 255

            # With newer (1.0) versions of matplotlib, you can
            # use the "zorder" kwarg to make the image overlay
            # the plot, rather than hide behind it... (e.g. zorder=10)
            self.mgplot.figimage(nim, self.logo[1], self.logo[2], zorder=10)

        # SAVEFIG
        fullname = "{}.{}".format(fig_name, self.filefmt)
        LOG.info("printing %s", fullname)
        if self.kml or self.kmz:
            # self.mgplot.axes(frameon=0)
            if self.save:
                self.mgplot.savefig(fullname, bbox_inches='tight',
                                    frameon=0, pad_inches=0, dpi=self.dpi,
                                    transparent=True)
        else:
            self.mgaxis.set_title(img_title, fontsize=self.fontsize, zorder=0)

            if self.save:
                self.mgplot.savefig(fullname, bbox_inches='tight',
                                    pad_inches=.2, dpi=self.dpi)

        return fig_name

    def compare_maps(self, map_names, outdir, date, steps, tpl=''):
        """ Generate maps comparison """

        os.chdir(outdir)

        # print "MAPNAMES", map_names
        # for map_name in map_names:
#        newMapNames = map_names[0]
#        items = {} #[i[0] for i in map_names]
#        for i in range(0, len(map_names)-1):
#            items, newMapNames, newMapNameTpl =
#            self.twoMapsCompare([newMapNames, map_names[i+1]], items)

        mnames = np.array(map_names)
        k_s = mnames.T

        idx = 0
        for item in k_s:
            # if idx >= len(newMapNames):
            #  continue
            imgs = ' '.join([str(i) + '.gif' for i in item])
            if tpl:
                newimg = tpl % {'date': date, 'step': steps[idx]}
            else:
                newimg = steps[idx]
            comm = "montage %s -tile 2x -geometry +1+1 %s.gif" % (imgs, newimg)
            _, _ = subprocess.getstatusoutput(comm)
            idx += 1

        # montage <infiles> -tile 2x -geometry 800x600+1+1 <outfile>

        # rename from 00-06-... to 00-01 ...
#        st, out = commands.getstatusoutput("ls %s*" % newMapNameTpl)
#        if st != 0:
#            print "Error: %s" % str(out)
#        else:
#            names = out.split('\n')
#            #print names
#            for num in range(0, len(names)):
#                snum = "%02d" % num
#                #print "mv %s %s.gif" % (names[num],
#                newMapNameTpl.replace("??", snum)) st2, out2 =
#                commands.getstatusoutput("mv -f %s %s.gif" % (names[num],
#                newMapNameTpl.replace("??", snum)))
#                if st2 != 0:
#                    print "Error: %s" % str(out2)

#        newMapNameTpl2 = newMapNameTpl.replace("??", "loop")
        nimg0 = "??"
        nimg1 = "loop"
        if tpl:
            nimg0 = tpl % {'date': date, 'step': nimg0}
            nimg1 = tpl % {'date': date, 'step': nimg1}
        status, out = subprocess.getstatusoutput(
            "convert -delay 75 -loop 0 %s.gif %s.gif" % (nimg0, nimg1))
        if status != 0:
            LOG.error("Error: %s", str(out))

    def init_environ(self, **kwargs):
        """ initialize environment with all arguments """

        # update from config file
        if ('config' in kwargs) and ('section' in kwargs):
            self.load_conf(kwargs['section'], kwargs['config'])

        # update from command line
        vars(self).update(parse_parameters(kwargs))
        # arguments are only local

        LOG.setLevel(self.loglevel)

        # parse wind arguments
        if self.windopts and (len(self.windopts) == 4):
            self.wind_scale = int(self.windopts[3])
        LOG.info("SHP %s", str(self.shapefiles))
        if self.shapefiles:
            self.shapefiles = [f.replace(".shp", "") for f in
                               glob(self.shapefiles)]
        LOG.info("SHP %s", str(self.shapefiles))

    def aplot(self, xloc, yloc, map_data=None, wind_data=None,
              contour_data=None, scatter_data=None, **kwargs):
        """ Plot one or more maps directly from numerical arrays """

        # store options to be restored at the end
        localvars = copy.deepcopy(vars(self))

        self.init_environ(**kwargs)

        if scatter_data is not None:
            if isinstance(scatter_data, str):
                scatter_data = DataFrameHandler(
                    parse_path(self.indir, scatter_data)).filter()
            else:
                scatter_data = DataFrameHandler(scatter_data).filter()
        else:
            scatter_data = None
        LOG.info("scatter data: %s", str(scatter_data))

        data = MapData(
            map_data=[map_data],  # temporarily
            wind_data=wind_data,
            contour_data=contour_data,
            scatter_data=scatter_data
        )
        grid = (xloc, yloc)
        self.init_map(grid)

        if self.img_template:
            f_name = self.img_template
        else:
            f_name = 'mg_aplot'
        fig_name = "%s/%s" % (self.outdir, f_name)
        if self.subplot is None:
            plt.clf()
            self.mgaxis = plt.axes(projection=self._crs)
            self.mgplot = plt.gcf()
        else:
            self.mgaxis = plt.subplot(self.subplot[0],
                                      self.subplot[1],
                                      self.subplot[2],
                                      projection=self._crs)
            self.mgplot = plt.gcf()

        self.gen_image_map(
            fig_name,
            grid,
            data,
            self.title,
            # scatter_data=scatter_data
        )

#        # Create Max at required intervals
#        if self.maxdata and n_time in self.maxdata:
#            if (self.maxtitle != None):
#                fig_name = "%s_%s" % (f_name, 'MAXD%d' % (n_time/24))
#                p_title = self.set_title(self.maxtitle, s_date, curr_date,
#                s_time)
#                self.gen_image_map(
#                                fig_name,
#                                grid,
#                                nc_handler.get_current_max_data(),
#                                p_title
#                                )
#            else:
#                print "Missing MAXTITLE, thus not generating MAX images!"

        # restore options without local function parameters
        vars(self).update(localvars)

    def plot_cube(self, cube, **kwargs):
        """ Plot cube """

        if 'title' not in kwargs:
            kwargs['title'] = self._get_default_title(cube)

        self.aplot(
            cube.coord('longitude').points,
            cube.coord('latitude').points,
            map_data=cube.data,
            **kwargs
        )

    def plot(self, **kwargs):
        """ Plot one or more maps from netCDF file(s) """

        # store options to be restored at the end
        localvars = copy.deepcopy(vars(self))

        self.init_environ(**kwargs)

        if isinstance(self.srcvars, str):
            self.srcvars = [self.srcvars]
        elif not isinstance(self.srcvars, list):
            LOG.error('Error')

        if isinstance(self.srcfiles, str):
            self.srcfiles = [self.srcfiles]
        elif not isinstance(self.srcfiles, list):
            LOG.error('Error')

        if self.scatter is not None:
            if isinstance(self.scatter, str):
                scatter_data = DataFrameHandler(
                    parse_path(self.indir, self.scatter)).filter()
            else:
                scatter_data = DataFrameHandler(self.scatter).filter()
        else:
            scatter_data = None
        LOG.info("scatter data: %s", str(scatter_data))

        # run = ''
        run_tmp = ''
        map_names = []

        nc_handler = MapDataHandler(
            self.srcfiles,
            self.srcvars,
            self.indir,
            self.srcgaps,
            self.wind,
            self.windopts,
            self.lat,
            self.lon,
            self.transf,
            self.subsetting,
            self.dimension,
            winds={'src': self.wind,
                   'opts': self.windopts},
            contours={'var': self.contours},
            varconds=self.varconds,
        )

        fig_names = []
        plt_names = []

        dims = nc_handler.get_dims()

        if self.timesteps == 'all':
            self.timesteps = list(sorted(dims.keys()))

        run_tmp = dims[0]  # 12:30Z30NOV2010
        if run_tmp[:-10] == "01:30":
            run_tmp = run_tmp.replace("01:30", "00")
        # run = "%sh %s %s %s" % (run_tmp[:-10], run_tmp[-9:-7],
        # run_tmp[-7:-4], run_tmp[-4:])

        # return grid
        grid = nc_handler.grid

        # if not NOMAP:
        self.init_map(grid)

        s_date = datetime.strptime("%s %s %s %s" % (run_tmp[-4:],
                                                    run_tmp[-7:-4],
                                                    run_tmp[-9:-7],
                                                    run_tmp[0:2]),
                                   "%Y %b %d %H")

        ss_date = s_date.strftime("%Y%m%d")
        steps = []

        start = self.timesteps[0]

        # LOG.info("Start @ %s - s_date: %s - run_tmp: %s" % (START, s_date,
        # run_tmp))

        if start is None:
            start = 0

        for n_time in self.timesteps:  # range(START,int(TOTAL),INTERVAL):
            if self.subplot is None:
                plt.clf()
                self.mgaxis = plt.axes(projection=self._crs)
                self.mgplot = plt.gcf()
            else:
                self.mgaxis = plt.subplot(self.subplot[0],
                                          self.subplot[1],
                                          self.subplot[3],
                                          projection=self._crs)
                self.mgplot = plt.gcf()

            valid_tmp = dims[n_time]
            curr_date = datetime.strptime("%s %s %s %s" % (valid_tmp[-4:],
                                                           valid_tmp[-7:-4],
                                                           valid_tmp[-9:-7],
                                                           valid_tmp[0:2]),
                                          "%Y %b %d %H")

            s_time = "%02d" % n_time
            steps.append(s_time)

            p_time = (curr_date - s_date).total_seconds()/3600
            # s_time24 = "%02d" % (p_time%24)
            # s_time3d = "%03d" % p_time # Currently unused, only for
            # Valentina who has more than 99 img in a set

            if self.img_template:
                f_name = self.img_template % {'date': ss_date, 'step': s_time}
                fig_name = "%s/%s" % (self.outdir, f_name)
                loop_name = self.img_template % {'date': ss_date,
                                                 'step': 'loop'}
            else:
                f_name = '.'.join(os.path.basename(self.srcfiles[0])
                                  .split('.')[:-1])
                fig_name = "%s/%s_%s" % (self.outdir, f_name, s_time)
                loop_name = "%s_loop" % (f_name)

            # valid = "%02dUTC %s" % (p_time % 24, curr_date.strftime("%d %b
            # %Y"))

            # stime = "%02d" % (int(run_tmp.split('Z')[0])+p_time)
            stime = "%02d" % (p_time)
            p_title = set_title(self.title, s_date, curr_date, s_time, stime)
            cur_scatter_data = None
            if scatter_data is not None and (curr_date in scatter_data):
                cur_scatter_data = scatter_data[curr_date]

            fname = self.gen_image_map(
                fig_name,
                grid,
                nc_handler.get_data_for_tstep(n_time),
                p_title,
                cur_scatter_data=cur_scatter_data
            )

            fig_names.append(fname)
            plt_names.append((self.mgplot, self.mgaxis))

            # Create Max at required intervals
            if self.maxdata and n_time in self.maxdata:
                if self.maxtitle is not None:
                    fig_name = "%s_%s" % (f_name, 'MAXD%d' % (n_time/24))
                    p_title = set_title(self.maxtitle, s_date, curr_date,
                                        s_time, stime)
                    self.gen_image_map(
                        fig_name,
                        grid,
                        nc_handler.get_current_max_data(),
                        p_title
                    )
                else:
                    LOG.info("Missing MAXTITLE, not generating MAX images!")

        if self.kml or self.kmz:
            plt.clf()

            run_date = s_date.strftime("%Y%m%d%H")
            # separate colorbar
            mpl.rcParams['axes.linewidth'] = 0.1
            fig = plt.figure(figsize=(.1, 12))
            cax = fig.add_axes([0.05, 0.80, 0.9, 0.15])
            # , axisbg=(1, 1, 1, 0))
            print("...", self.bounds, "...")
            cbar = mpl.colorbar.ColorbarBase(
                cax,  # =self.mgaxis,
                cmap=self.cmap,
                norm=self.norm,
                values=self.bounds,
                ticks=self.bounds,
                extend=self.extend,
                drawedges=False)
            if self.bounds:
                cbar.set_ticklabels(self.bounds)
#            else:
#                try:
#                    cbar.set_ticklabels(mco.levels)
#                except:
#                    pass
            cbar.ax.tick_params(labelsize=6)
            plt.setp(plt.getp(cax, 'yticklabels'), color='w')
            plt.setp(plt.getp(cax, 'yticklabels'), fontsize=6)
            for lin in cbar.ax.yaxis.get_ticklines():
                lin.set_visible(False)

            tit = str(p_title)
            idx1 = tit.find('(')
            idx2 = tit.find(')')
            var_unit = tit[idx1:idx2+1]
            if var_unit.find("%s") >= 0:
                var_unit = ''
            plt.xlabel(
                p_title,
                # "%s\n%s" % (self.srcvars[0], var_unit),
                horizontalalignment='left',
                color='w',
                fontsize=6,
            )
            cax.xaxis.set_label_coords(-0.025, -0.025)

            os.makedirs("%s-%s" % (run_date, self.srcvars[0]))

            if self.save:
                fig.savefig(
                    "%s/%s-%s/%s-colorbar.png" % (self.outdir, run_date,
                                                  self.srcvars[0], run_date),
                    bbox_inches='tight',
                    pad_inches=0, dpi=self.dpi,
                    transparent=True
                )

            # generate KMZ/KML - Offline/Online - online priority
            if self.kmz or self.kml:
                online = self.kml
                LOG.info("Generating KMZ ...")
                gen_kml(fig_names, self.srcvars[0], self.lon, self.lat, dims,
                        self.outdir, online=online)

        # generate animation.
        if self.anim:
            gen_anim(
                "%s.%s" % (loop_name.replace('loop', '*'), self.filefmt),
                "%s.gif" % loop_name,
                self.outdir,
                self.anim_delay
            )
#            fulloutdir = os.path.join(self.outdir,
#            os.path.dirname(self.img_template))
#            loop_name = os.path.basename(loop_name)
#            self.gen_anim(
#                         fulloutdir,
#                         "%s.%s" % (loop_name.replace('loop','*'),
#                         self.filefmt),
#                         fulloutdir,
#                         "%s.gif" % loop_name
#                        )

        map_names.append(fig_names)

        # restore options without local function parameters
        vars(self).update(localvars)

        # print "Returning ", plt_names
        # return plt_names

#    num = len(map_names)
#    if num > 1:
#        mg.compare_maps(map_names, OUTDIR, ss_date, steps, JOINT_TEMPLATE )

    def reset_conf(self):
        """ Back to the initial conditions. """

        self.__init__()

    def load_conf(self, section=None, fpath=None, reset=False):
        """ Load existing configurations from file. """

        from .config import read_conf

        if fpath is None:
            fpath = parse_path(self.config_dir, self.config_file)
        else:
            fpath = parse_path(self.indir, fpath)

        if not os.path.isfile(fpath):
            LOG.error("Error %s", fpath)
            return

        opts = read_conf(section, fpath)
        if section is None:
            return opts

        if reset:
            self.reset_conf()
        vars(self).update(parse_parameters(opts))

    def write_conf(self, section, fpath=None):
        """ Write configurations on file. """

        from .config import write_conf

        if fpath is None:
            fpath = parse_path(self.config_dir, self.config_file)
        else:
            fpath = parse_path(self.indir, fpath)

        # create new dir if doesn't exist
        dirname = os.path.dirname(fpath)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # save current conf
        curropts = copy.deepcopy(vars(self))
        # load defaults
        self.reset_conf()
        defaults = copy.deepcopy(vars(self))
        # calculate diff
        diff = {k: curropts[k] for k in curropts if curropts[k] !=
                defaults[k]}
        # reload diff
        vars(self).update(diff)
        # save diff
        write_conf(section, fpath, diff)
