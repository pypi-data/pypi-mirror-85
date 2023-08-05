#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Francesco Benincasa <francesco.benincasa@bsc.es>
# author: Luca Telloli <telloli.luca@bsc.es>

import matplotlib as mpl

from pylab import *
import os.path
import time
import commands
from mpl_toolkits.basemap import Basemap
from matplotlib.cbook import delete_masked_points
import matplotlib.pyplot as plt

from datetime import datetime

#from netCDF4 import *


class MapGenerator:
    """ """

    def __init__(self):
        """ Initialize class with attributes """
        self.extend = 'neither'
        self.norm = None
        self.cmap = None
        self.bounds = []
        self.formats = None
        self.boundaries = []
        self.map = None   #Map
        self.lat = None #Latitudes
        self.lon = None #Longitudes
        self.over = None
        self.under = None
        self.colors = []
        self.first_image = True # Is is the first image of the batch?
        self.mapName = None # name of the figure to map animation colors
        self.fontsize = 16 #rcParams['text.fontsize'] #12 #Title font size

    def setNorm(self):
        """ """
        #bounds = self.bounds
        #self.norm = mpl.colors.BoundaryNorm(bounds, len(bounds)-1, clip=True)
        self.norm = mpl.colors.BoundaryNorm(self.bounds, len(self.colors))

    def setExtend(self):
        """ """
        bounds = self.bounds
        boundaries = self.boundaries
        if type(boundaries) is list:
            boundaries = [boundaries[0]] + bounds + [boundaries[1]]
            self.extend = 'both'
        else:
            if self.under:
                boundaries = [boundaries] + bounds
                self.extend = 'min'
            if self.over:
                boundaries = bounds + [boundaries]
                self.extend = 'max'

    def setColorMap(self):
        """ create color map """
        self.cmap = mpl.colors.ListedColormap(self.colors)
        if self.over:
            print("Setting over to ", self.over)
            self.cmap.set_over(color=self.over)
        if self.under:
            print("Setting under to ", self.under)
            self.cmap.set_under(color=self.under)
        self.cmap.set_bad('red')

    def setColorBar(self, drawedges=False, cax=None):
        """ Create color bar """
        colorbar(drawedges=drawedges, cax=cax, ticks=self.bounds)

    def setTitle(self, title, sdate, cdate, step, stime):
        """ Set the title of the current image to the one provided, substituting the
            patterns """

        titleDic = {
            'syear': sdate.strftime("%Y"),
            'smonth': sdate.strftime("%m"),
            'sMONTH': sdate.strftime("%b"),
            'sday': sdate.strftime("%d"),
            'shour': sdate.strftime("%H"),
            'year': cdate.strftime("%Y"),
            'month': cdate.strftime("%m"),
            'MONTH': cdate.strftime("%b"),
            'day': cdate.strftime("%d"),
            'hour': cdate.strftime("%H"),
            'step': step,
            'simday': "%d" % (int(stime)/24),
            'simhh':  "%02d" % (int(stime)%24)
        }

        try:
            pTitle=unicode(title.decode('utf-8')) % titleDic #("%sh" % sTime, valid)
        except Exception as e:
            print(e)
            pTitle=title % titleDic #("%sh" % sTime, valid)

        return pTitle

    def printTime(self, msg=None):
        # initial time
        try:
            start_t
        except NameError:
            global start_t
            global last_t
            start_t = datetime.now()
            last_t = start_t

        now_t = datetime.now()
        diff_t = now_t - last_t
        if (msg != None):
            print('TIME:', msg, ' done in ', diff_t.seconds, ' s')
        last_t = now_t

    def runCommand(self, commStr, fatal=True):
        st, out = commands.getstatusoutput(commStr)
        if st != 0:
            print("Error: %s" % str(out))
            if (fatal == True):
                sys.exit(1)

    def genAnim(self, indir, inpattern, outdir, outfile):
        ''' Generate an animation starting from a set of
            images, specified by the inpattern parameter '''
        print("Animation: ", indir, inpattern, outdir, outfile)
        # Create animation
        #self.runCommand("convert -delay 75 -loop 0 -crop 800x600+0+0 -layers Optimize %s/%s %s/%s" % (indir, inpattern, outdir, outfile))
        self.runCommand("convert -delay 75 -loop 0 -layers Optimize %s/%s %s/%s" % (indir, inpattern, outdir, outfile))
        # Remove intermediate files
        #self.runCommand("rm %s/%s %s" % (indir, inpattern, self.mapName), False)

    def initMap(self, DRAW_OPTS, LAT, LON, BOUNDS, BOUNDARIES, COLORS, OVER, UNDER, **kwargs):
        """ Initialize a Basemap map.
            Initialization
            should be performed only once at the
            beginning of a serie of images """
        self.DRAW_OPTS = DRAW_OPTS
        self.lat = LAT
        self.lon = LON
        self.bounds = BOUNDS
        self.boundaries = BOUNDARIES
        self.colors = COLORS
        self.over = OVER
        self.under = UNDER
        self.printTime("Start: ")

        if not self.DRAW_OPTS.nomap:
            self.map = Basemap(projection='cyl', resolution=self.DRAW_OPTS.resolution,
                llcrnrlon=LON[0], llcrnrlat=LAT[0],
                urcrnrlon=LON[1], urcrnrlat=LAT[1],
                fix_aspect=self.DRAW_OPTS.keep_aspect,
                area_thresh=kwargs['area_thresh'] #self.DRAW_OPTS.area_threshold
            )

        self.printTime("Initialization of Basemap:")

        # Fix the printout of tick values to avoid .0 decimals in integers
        strs = []
        for b in self.bounds:
            if (b == int(b)):
                strs.append("%d" % b)
            else:
                strs.append(str(b))

        self.formats = matplotlib.ticker.FixedFormatter(strs)
        self.first_image = True


    def genKML(self, lon, lat, figNames, runDate, online=True):
        """ """
        from lxml import etree
        from pykml.parser import Schema
        from pykml.factory import KML_ElementMaker as KML
        from datetime import datetime, timedelta
        import zipfile

        if online is False:
            BASEPATH = ''
        else:
            BASEPATH = 'http://dust.aemet.es/archive/NMMB-BSC/'

        kmlName = '-'.join(figNames[0].split('-')[:-1])
        varName = figNames[0].split('-')[-2]
        dirName = BASEPATH + runDate + '-' + varName
        starth = int(runDate[-2:])
        interval = 3
        begindate = datetime.strptime("%s" % (runDate), "%Y%m%d%H")

        doc = KML.kml(
            KML.Folder(
                KML.name(kmlName),
                KML.LookAt(
                    KML.longitude((lon[1]+lon[0])/2),
                    KML.latitude((lat[1]+lat[0])/2),
                    KML.range(8500000.0),
                    KML.tilt(0),
                    KML.heading(0),
                ),
                KML.ScreenOverlay(
                    KML.name("Legend"),
                    KML.open(1),
                    KML.Icon(
                        KML.href("%s/%s-colorbar.png" % (dirName,runDate)),
                    ),
                    KML.overlayXY(x="0",y="1",xunits="fraction",yunits="fraction"),
                    KML.screenXY(x=".01",y="0.75",xunits="fraction",yunits="fraction"),
                    KML.rotationXY(x="0",y="0",xunits="fraction",yunits="fraction"),
                    KML.size(x="0",y="0.5",xunits="fraction",yunits="fraction"),
                    id="%s-ScreenOverlay" %(runDate),
                ),
            )
        )

        try:
            os.mkdir(dirName)
        except:
            pass

        if online is False:
            zf = zipfile.ZipFile("%s.kmz" % kmlName, 'w')

        for figName in figNames:
            figName = figName + ".png"
            figPath = "%s/%s" % (dirName,figName)
            begdate = datetime.strftime(begindate, "%Y-%m-%dT%H:00:00Z")
            enddate = datetime.strftime(begindate + timedelta(hours=interval), "%Y-%m-%dT%H:00:00Z")
            doc.Folder.append(KML.GroundOverlay(
                KML.name("%s:00:00Z" % starth),
                KML.TimeSpan(
                    KML.begin(begdate),
                    KML.end(enddate),
                ),
                KML.Icon(
                    KML.href(figPath),
                    KML.viewBoundScale(1.0),
                ),
                KML.altitude(0.0),
                KML.altitudeMode("relativeToGround"),
                KML.LatLonBox(
                    KML.south(lat[0]),
                    KML.north(lat[1]),
                    KML.west(lon[0]),
                    KML.east(lon[1]),
                    KML.rotation(0.0),
                ),
            ))
            starth += interval
            begindate = begindate + timedelta(hours=interval)

            if online is False and os.path.exists(figName):
                os.rename(figName, figPath)
                zf.write(figPath)

        outf = file("%s.kml" % kmlName, 'w')
        outf.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        outf.write(etree.tostring(doc, pretty_print=True))
        outf.close()

        if online is False:
            zf.write("%s.kml" % kmlName)
            zf.write("%s/%s-colorbar.png" % (dirName,runDate))
            zf.close()

#            for img in os.listdir(dirName):
#                os.remove("%s/%s" % (dirName, img))
#            os.rmdir(dirName)
#            os.remove("%s.kml" % kmlName)


    def genImageMap(self, figName, subtitle, DATA,  imgTitle, **kwargs):
        """ Generate image map """
        mapData = DATA.getMapData()

        clf()
        params = {
             'font.size': 14,
             'text.fontsize': 28,
             'axes.titlesize': 11,
             'savefig.dpi': self.DRAW_OPTS.dpi
        }

        rcParams.update(params)

        g = mapData.grid
        if not self.DRAW_OPTS.nomap:
            x, y = self.map(*meshgrid(g.lon,g.lat))
        else:
            x, y = meshgrid(g.lon,g.lat)
        print("X", len(x))
        print("Y", len(y))
        print("mapData", mapData.shape)

        self.printTime("meshgrid")

        # Set the colormap
        self.setNorm()
        self.setColorMap()

        # overwrite option
        if os.path.exists(figName + ".png") and not OVERWRITE:
            print(figName, " already exists.")
            clf()
            return figName

        # nodraw option
        if self.DRAW_OPTS.nodraw and \
                os.path.exists("%s-%s/%s.png" % (runDate, varName, figName)) and \
                not self.DRAW_OPTS.overwrite:
            print(figName, " already exists.")
            clf()
            return figName

        if self.DRAW_OPTS.nodraw:
            axes(frameon=0)

        # Draw filled contour
        if not self.DRAW_OPTS.keep_aspect:
            print("Not keeping original aspect")
            ysize_norm = self.DRAW_OPTS.ysize*0.8
            xsize_norm = self.DRAW_OPTS.xsize*0.8

            rows = imgTitle.count("\n")
            blines = max(rows - 2, 0)
#            print "++++++++++++++++++++++++++"
#            print "rows", rows
#            print "++++++++++++++++++++++++++"
            param = float(self.fontsize)/400
            ystart_base_norm = 0.1 - param*(blines)#imgTitle
            xstart_base_norm = 0.1
            ystart_norm = (0.8 - ysize_norm) / 2 + ystart_base_norm
            xstart_norm = (0.8 - xsize_norm) / 2 + xstart_base_norm
            ax_map = axes([xstart_norm, ystart_norm, xsize_norm, ysize_norm])
            print("Switching AXES for MAP:", ax_map)

        print("******** INTERPOLATION **********:", self.DRAW_OPTS.nointerp)
        if not self.DRAW_OPTS.nocontourf and not self.DRAW_OPTS.nomap and not self.DRAW_OPTS.nointerp:
            mco = self.map.contourf(x, y, mapData, cmap=self.cmap, norm=self.norm,
                levels=self.bounds, extend='both', horizontalalignment='center')
        elif not self.DRAW_OPTS.nocontourf and not self.DRAW_OPTS.nomap and self.DRAW_OPTS.nointerp:
            mco = self.map.pcolor(x, y, mapData, cmap=self.cmap, norm=self.norm)
        elif not self.DRAW_OPTS.nocontourf and self.DRAW_OPTS.nomap:
            mco = contourf(x, y, mapData, cmap=self.cmap, norm=self.norm,
                levels=self.bounds, extend='both', horizontalalignment='center')

        # Draw shape files
        if self.DRAW_OPTS.hasShapeFiles():
            line_w = self.DRAW_OPTS.shapef_width_init
            for shapef in self.DRAW_OPTS.shapefiles:
                print("Processing shape file:", shapef, " with line width:", line_w)
                self.map.readshapefile(shapef, "%s" % os.path.basename(shapef), linewidth=line_w)
                line_w = max(self.DRAW_OPTS.shapef_width_step, line_w - self.DRAW_OPTS.shapef_width_step)
        self.printTime("contourf")

        ## FIXME Modify to use scatter inside DATA
        ## if DATA.hasScatterData()... etc...
        if kwargs.has_key('scatter'):
            SCATTERD = kwargs['scatter']
            if (SCATTERD != None):
                print("Plotting scatter data", SCATTERD[0], SCATTERD[1])
                self.map.scatter(SCATTERD[0], SCATTERD[1], s=SCATTERD[2], c=SCATTERD[3],
                    marker='o', linewidth=0.5)

        if DATA.hasWindData():
            WINDS = DATA.getWindData()
            X,Y,U,V = delete_masked_points(x.ravel(), y.ravel(), WINDS['u'].ravel(), WINDS['v'].ravel())
            print("Wind scale is", self.DRAW_OPTS.wind_units, self.DRAW_OPTS.wind_scale)
            if WINDS.has_key('barbs'):
                B = self.map.barbs(X, Y, U, V, #units=self.DRAW_OPTS.wind_units,
                    #headlength=self.DRAW_OPTS.wind_head_length,
                    #headwidth=self.DRAW_OPTS.wind_head_width,
                    #width=self.DRAW_OPTS.wind_width,
                    #minshaft=self.DRAW_OPTS.wind_minshaft,
                    #scale=self.DRAW_OPTS.wind_scale,
                    color='k')
                self.printTime("barbs")
            else:
                Q = self.map.quiver(X, Y, U, V, units=self.DRAW_OPTS.wind_units,
                        headlength=self.DRAW_OPTS.wind_head_length,
                        headwidth=self.DRAW_OPTS.wind_head_width,
                        width=self.DRAW_OPTS.wind_width,
                        minshaft=self.DRAW_OPTS.wind_minshaft,
                        scale=self.DRAW_OPTS.wind_scale,
                        color='gray')
                # Draw the key
                quiverkey(Q,
                    self.DRAW_OPTS.wind_label_xpos,
                    self.DRAW_OPTS.wind_label_ypos,
                    self.DRAW_OPTS.wind_label_scale,
                    label='%s m/s' % self.DRAW_OPTS.wind_label_scale,
                    coordinates='axes',
                    labelpos='S', labelsep=0.05)
                self.printTime("quivers")

        if DATA.hasContourData():
            interval = self.DRAW_OPTS.contours_interval
            exclude = self.DRAW_OPTS.contours_exclude_vals
            cLowBound = -99999
            cUppBound = 99999
            CDATA = DATA.getContourData()
            try:
                cMin = min(filter (lambda a: a > cLowBound, ravel(CDATA.data)) )
                adjcMin = int(cMin - (cMin % interval) - interval * 2)
            except ValueError:
                cMin =0
            try:
                cMax = max(filter (lambda a: a < cUppBound, ravel(CDATA.data)) )
                adjcMax = int(cMax - (cMax % interval) + interval * 2)
            except ValueError:
                cMax = 0
            lvls = arange(adjcMin, adjcMax, interval)
            for ex in exclude:
                lvls = filter (lambda ex: ex != 0, lvls)
            if(len(lvls) > 0):
                mco = self.map.contourf(x, y, mapData, cmap=self.cmap, norm=self.norm, levels=self.bounds, extend='both', horizontalalignment='center')

            print("-----------------", mapData, CDATA, "--------------------")
            if (mapData == CDATA).all():
                print(":::::::::::::::::::::::: SAME !!! :::::::::::::::::::")
                CS = contour(x, y, CDATA, levels=self.bounds,
                        colors=self.DRAW_OPTS.contours_color,
                        linewidths=self.DRAW_OPTS.contours_linewidth)
            else:
                print(":::::::::::::::::::::::: DIFFERENT !!! :::::::::::::::::::")
                print("MIN:", cMin, "MAX:", cMax)
                CS = contour(x, y, CDATA, levels=lvls,
                        colors=self.DRAW_OPTS.contours_color,
                        linewidths=self.DRAW_OPTS.contours_linewidth)

            if self.DRAW_OPTS.contours_label:
                plt.clabel(CS, inline=1,
                        fontsize=self.DRAW_OPTS.contours_lbl_fontsize,
                        #backgroundcolor='r',
                        fmt=self.DRAW_OPTS.contours_lbl_format)
#            else:
#                print "Not drawing contours since levels has ", len(lvls), " elements"

        #coords normalization
        lat_offset = abs(self.lat[0]) % self.lat[2]
        lon_offset = abs(self.lon[0]) % self.lon[2]

        if not self.DRAW_OPTS.nomap:
            self.map.drawparallels(arange(self.lat[0]+lat_offset, self.lat[1], self.lat[2]),labels=[1,0,0,0],linewidth=0.2, fontsize=12)
            self.map.drawmeridians(arange(self.lon[0]+lon_offset, self.lon[1], self.lon[2]),labels=[0,0,0,1],linewidth=0.2, fontsize=12)
            self.printTime("meridians")

            if kwargs.has_key('drawopts'):
                # Drawing countries
                if 'countries' in kwargs['drawopts']:
                    self.map.drawcountries(linewidth=0.7)
                    self.printTime("countries")
                # Drawing coastlines (land/sea, lakes, etc...)
                if 'coastlines' in kwargs['drawopts']:
                    self.map.drawcoastlines()
                    self.printTime("coastlines")
                # Drawing states (FIXME does it work outside the U.S.?)
                if 'states' in kwargs['drawopts']:
                    self.map.drawstates()
                    self.printTime("states")

        a = axes([0.0, 0.0, 1.0, 1.0])
        axis('off')
        text(
            0.5,
            0.97,
            imgTitle,
            horizontalalignment='center',
            verticalalignment='top',
            fontsize=self.fontsize
            )

       # Change axes for colorbar
        if self.DRAW_OPTS.draw_colorbar: # or not self.DRAW_OPTS.nocontourf:
            xs = self.DRAW_OPTS.xsize
            nap = .78-((1-xs)*0.4)
            a = axes([nap, 0, .15, .9], frameon=False)
            axis('off')
            shrink=0.75
            colorbar(mco, ticks=self.bounds, format=self.formats, pad=0, shrink=shrink, aspect=20, drawedges=True)
            self.printTime("colorbar")

            ## If required, draw arrow pointing to the specified limits
            if self.DRAW_OPTS.hasLimits():
                # The following two values are absolute
                upper = 0.863 - 0.45 * (0.8 - shrink) # formula seems to work ok
                lower = 0.137 + 0.45 * (0.8 - shrink)
                span  = upper - lower
                arrows = self.DRAW_OPTS.aq_limits
                f = span/float(len(self.bounds) - 1)
                for i in arrows:
                    for j in range(0, len(self.bounds) - 1):
                        if (i >= self.bounds[j] and i <= self.bounds[j+1]):
                            if (i == self.bounds[j+1]):
                                p = j+1
                                add = 0
                            else:
                                p = j
                                add = (float(i - self.bounds[j])/float(self.bounds[j+1] - self.bounds[j]))*f
                            pos = f*p + lower
                            arrow(0.88, pos + add, 0.10, 0, length_includes_head=True,
                                head_length=0.10, head_width=0.025, fill=True, color='k')

        savefig(figName + ".png") #, bbox_inches='tight', pad_inches=-0.3)
        self.printTime("saving")

        if(self.first_image):
#            #if first image of the batch, produce a image "color map"
#            print "First image of the batch: creating image color map"
#            self.mapName = "%s.map.png" % figName
#            # Get the colorbar to generate the image color map
#            self.runCommand("convert -crop 70x600+730+0 -colors 160 %s.png %s" % (figName, self.mapName))
            self.first_image = False

        #convert from png to gif
        print("printing ", figName)
#        self.runCommand("convert -quality 80 +dither -remap %s %s.png %s.anim.png" % (self.mapName, figName, figName))
        self.runCommand("convert +dither %s.png %s.gif" % (figName, figName))
        self.runCommand("rm %s.png" % figName)

        clf()
        self.printTime("convert")
        return figName


    def compareMaps(self, mapNames, outdir, date, steps, tpl=''):
        """ Generate maps comparison """

        os.chdir(outdir)

        #print "MAPNAMES", mapNames
        #for mapName in mapNames:
#        newMapNames = mapNames[0]
#        items = {} #[i[0] for i in mapNames]
#        for i in range(0, len(mapNames)-1):
#            items, newMapNames, newMapNameTpl = self.twoMapsCompare([newMapNames, mapNames[i+1]], items)

        mn = array(mapNames)
        ks = mn.T

        idx = 0
        for item in ks:
#            if idx >= len(newMapNames):
#                continue
            imgs = ' '.join([str(i) + '.gif' for i in item])
            if tpl:
                newimg = tpl % {'date':date, 'step':steps[idx]}
            else:
                newimg = steps[idx]
            #comm = "montage %s -tile 2x -geometry 800x600+1+1 %s.gif" % (imgs, newMapNames[idx])
            comm = "montage %s -tile 2x -geometry +1+1 %s.gif" % (imgs, newimg)
            #print "COMPARE COMMAND:", comm
            st, out = commands.getstatusoutput(comm)
            idx += 1

        #montage <infiles> -tile 2x -geometry 800x600+1+1 <outfile>

        #rename from 00-06-... to 00-01 ...
#        st, out = commands.getstatusoutput("ls %s*" % newMapNameTpl)
#        if st != 0:
#            print "Error: %s" % str(out)
#        else:
#            names = out.split('\n')
#            #print names
#            for num in range(0, len(names)):
#                snum = "%02d" % num
#                #print "mv %s %s.gif" % (names[num], newMapNameTpl.replace("??", snum))
#                st2, out2 = commands.getstatusoutput("mv -f %s %s.gif" % (names[num], newMapNameTpl.replace("??", snum)))
#                if st2 != 0:
#                    print "Error: %s" % str(out2)

#        newMapNameTpl2 = newMapNameTpl.replace("??", "loop")
        nimg0 = "??"
        nimg1 = "loop"
        if tpl:
            nimg0 = tpl % {'date':date, 'step':nimg0}
            nimg1 = tpl % {'date':date, 'step':nimg1}
        st, out = commands.getstatusoutput("convert -delay 75 -loop 0 %s.gif %s.gif" % (nimg0, nimg1))
        if st != 0:
            print("Error: %s" % str(out))
