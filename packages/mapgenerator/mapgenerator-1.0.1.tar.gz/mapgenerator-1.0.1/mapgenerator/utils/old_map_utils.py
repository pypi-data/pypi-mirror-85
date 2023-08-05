#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Francesco Benincasa <francesco.benincasa@bsc.es>

import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.basemap import Basemap
from grads import *
from pylab import *
import Image

import time
import commands
import os.path
from config import *
from mpl_toolkits.basemap import Basemap
from matplotlib.cbook import delete_masked_points

from datetime import datetime

VERSION = "0.4beta"
MLEN = 0

mpl.rcParams.update({'font.size': 10})


class MapGenerator:
    """ """

    def __init__(self):
        """ Initialize class with attributes """
        self.extend = 'neither'
        self.norm = None
        self.cmap = None
        self.bounds = []
        self.boundaries = []
        self.logo = []
        self.rundate = None
        self.map = None   #Map
        self.lat = None #Latitudes
        self.lon = None #Longitudes
        self.res = None #Resolution


    def setNorm(self):
        """ Set normalization object """
        bounds = self.bounds
        self.norm = mpl.colors.BoundaryNorm(bounds, len(bounds)-1, clip=True)


    def setExtend(self):
        """ Set boundaries """
        bounds = self.bounds
        boundaries = self.boundaries
        if type(boundaries) is list:
            boundaries = [boundaries[0]] + bounds + [boundaries[1]]
            self.extend = 'both'
        else:
            if UNDER:
                boundaries = [boundaries] + bounds
                self.extend = 'min'
            if OVER:
                boundaries = bounds + [boundaries]
                self.extend = 'max'


    def setColorMap(self, colors, boundaries):
        """ Create color map """
        self.cmap = mpl.colors.ListedColormap(colors)
        if OVER:
            self.cmap.set_over(OVER)
        if UNDER:
            self.cmap.set_under(UNDER)
        self.cmap.set_bad('red')


    def setColorBar(self, drawedges=False, cax=None):
        """ Create color bar """
        colorbar(drawedges=drawedges, cax=cax, ticks=self.bounds)


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


    def setTitle(self, title):
        """ """
        pass

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

    def initMap(self, LAT, LON, RESOLUTION):
        """ initialize map """

        self.lat = LAT
        self.lon = LON
        self.res = RESOLUTION
        self.printTime("Start: ")
        self.map = Basemap(projection='cyl', resolution=RESOLUTION,
                #area_thresh=1,
                llcrnrlon=LON[0], llcrnrlat=LAT[0],
                urcrnrlon=LON[1], urcrnrlat=LAT[1]
                ,fix_aspect=False
                #,ax=ax1
        )
        self.printTime("Initialization of Basemap:")


    def genImageMap(self, ga, modName, varName, multiply, nTime, imgTitle, runDate):
        """ Generate image map """

        clf()
        params = {
             'font.size': 8,
             'text.fontsize': 13,
             'axes.titlesize': 11
             #,'savefig.dpi': 100
        }

        rcParams.update(params)


        g = DATA.grid
        x, y = self.map(*meshgrid(g.lon,g.lat))

        self.printTime("meshgrid")

        print("SHAPES: ", shape(DATA.grid.lon), shape(DATA.grid.lat), shape(x), shape(y))

        cm = mpl.colors.ListedColormap(COLORS)
        n = mpl.colors.BoundaryNorm(self.bounds, len(COLORS))
        cm.set_under(color=UNDER)
        cm.set_over(color=OVER)

        self.map.contourf(x, y, DATA, cmap=cm, norm=n, levels=self.bounds, extend='both')

        self.printTime("contourf")

        if kwargs.has_key('winds'):
            WINDS = kwargs['winds']
            print(WINDS)
            if (WINDS != None):
                X,Y,U,V = delete_masked_points(x.ravel(), y.ravel(), WINDS['u'].ravel(), WINDS['v'].ravel())
                Q = self.map.quiver(X, Y, U, V, units='width', headlength=2, width=0.0015, scale=400)
                # Draw the key
                quiverkey(Q, 0.8, -0.075, 20, label='20', coordinates='axes',
                    labelpos='S', labelsep=0.05)
                self.printTime("quivers")

        #add states and parallels
        coord_int = .1
        #coords normalization
        lat_offset = abs(self.lat[0]) % coord_int
        lon_offset = abs(self.lon[0]) % coord_int

        self.map.drawcountries(linewidth=0.7)
        self.printTime("countries")
        self.map.drawparallels(arange(self.lat[0], self.lat[1], self.lat[2]),labels=[1,0,0,0],linewidth=0.2)
        self.printTime("parallels")
        self.map.drawmeridians(arange(self.lon[0], self.lon[1], self.lon[2]),labels=[0,0,0,1],linewidth=0.2)
        self.printTime("meridians")

        self.map.drawcoastlines()
        self.printTime("coastlines")

        self.map.drawstates()
        self.printTime("states")
        #print "@@@@@ " , imgTitle, type(imgTitle)
        title(imgTitle)

       # Change axes for colorbar
        a = axes([.8, 0, .15, 1], frameon=False)
        axis('off')
        colorbar(ticks=self.bounds, pad=0, shrink=0.8, aspect=25, drawedges=True)
        self.printTime("colorbar")

        ## If required, draw arrow pointing to the specified limits
        if kwargs.has_key('limits'):
            # The following two values are absolute
            upper = 0.863
            lower = 0.137
            span  = upper - lower
            arrows = kwargs['limits']
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
                        arrow(0.83, pos + add, 0.15, 0, length_includes_head=True, head_length=0.15, head_width=0.025, fill=True, color='k')
            self.printTime("limits")

        print('FIGNAME: ', figName, ' ', type(figName))
        savefig(figName + ".png")
        self.printTime("saving")
        clf()

        #convert from png to gif and delete png
        print("printing ", figName, " ...")
        st, out = commands.getstatusoutput("convert %s.png %s.gif && rm %s.png" % (figName,figName,figName))
        if st != 0:
            print("Error: %s" % str(out))
            sys.exit(1)

        self.printTime("convert")
        return figName


    def twoMapsCompare(self, mapNames, app):
        """ Comparison between two maps """

        retNames = []
        items = items
        newMapNameTpl = ""

        for item0 in mapNames[0]:

            #print "loop 1:", item0
            idx0 = mapNames[0].index(item0)
            idx0 = "%02d" % idx0

            runDate0 = item0.split('-')[-1:][0][-9:]
            runHour0 = item0.split('-')[-1:][0][:-10]
            hOffset0 = item0.split('-')[-2:-1][0]
            var0 = item0.split('-')[-3:-2][0]
            mod0 = '-'.join(item0.split('-')[:-3])

            newDate0 = time.strftime('%Y%m%d', time.strptime(runDate0,"%d%b%Y"))

            for item1 in mapNames[1]:
                #print "loop 2:", item1
                idx1 = mapNames[1].index(item1)
                idx1 = "%02d" % idx1

                runDate1 = item1.split('-')[-1:][0][-9:]
                runHour1 = item1.split('-')[-1:][0][:-10]
                if runHour1 == "01:30": runHour1 = "00"
                hOffset1 = item1.split('-')[-2:-1][0]
                var1 = item1.split('-')[-3:-2][0]
                mod1 = '-'.join(item1.split('-')[:-3])

                newDate1 = time.strftime('%Y%m%d', time.strptime(runDate1,"%d%b%Y"))

                if (runDate0 != runDate1):
                    print("Error: different date, comparison impossible.")
                    print("MOD0", mod0, " - MOD1", mod1)
                    print("DAT0", runDate0, " - DAT1", runDate1)
                    continue

                if (var0 != var1):
                    print("Error: different variable, comparison impossible.")
                    print("MOD0", mod0, " - MOD1", mod1)
                    print("VAR0", var0, " - VAR1", var1)
                    continue

                #print "****", runHour0, hOffset0, "****", runHour1, hOffset1, "****"
                T = int(runHour0)+int(hOffset0)
                if T == (int(runHour1)+int(hOffset1)):
                    newMapName = "%s-%s-%s-%s-%sZ%s" % (mod0, mod1, var0, hOffset0, runHour0, runDate0)
                    newMapNameTpl = "%s-%s-%s-??-%sZ%s" % (mod0, mod1, var0, runHour0, runDate0)
                    st, out = commands.getstatusoutput("convert -background white %sappend %s.gif %s.gif %s.gif" %\
                      (app, item0, item1, newMapName))

                    if st != 0:
                        print("Error: %s" % str(out))
                    else:
                        #print "==>", newMapName, "<=="
                        retNames.append(newMapName)
                        break

        return items, retNames, newMapNameTpl


    def compareMaps(self, mapNames, freq, total):
        """ Generate maps comparison """

        if MLEN > 4:
            TILE = "3"
        else:
            TILE = "2"

        #print "MAPNAMES", mapNames
        #for mapName in mapNames:
        newMapNames = mapNames[0]
        items = {} #[i[0] for i in mapNames]
        for i in range(0, len(mapNames)-1):
            #print i, newMapNames, mapNames[i+1]
            app = '+'
            if i % 2: app = '-'
            items, newMapNames, newMapNameTpl = self.twoMapsCompare([newMapNames, mapNames[i+1]], app)

        ks = items.keys()
        ks.sort()
        #print ks, items
        #print newMapNames
        for item in ks:
            idx = ks.index(item)
            if idx >= len(newMapNames):
                continue
            imgs = ' '.join([i + '.gif' for i in items[item]])
            #print "xxxxx", idx, "xxxxx"
            comm = "montage %s -tile %sx -geometry 800x600+1+1 %s.gif" % (imgs, TILE, newMapNames[idx])
            #print "COMPARE COMMAND:", comm
            st, out = commands.getstatusoutput(comm)
            #print "***************", st
            #print "+++++++++++++++", out

        #montage <infiles> -tile 2x -geometry 800x600+1+1 <outfile>

        #rename from 00-06-... to 00-01 ...
        st, out = commands.getstatusoutput("ls %s*" % newMapNameTpl)
        if st != 0:
            print("Error: %s" % str(out))
        else:
            names = out.split('\n')
            #print names
            i = 0
            for num in range(0, len(names)):
                print(num, i)
                snum = "%02d" % i
                #print "mv %s %s.gif" % (names[num], newMapNameTpl.replace("??", snum))
                st2, out2 = commands.getstatusoutput("mv -f %s %s.gif" % (names[num], newMapNameTpl.replace("??", snum)))
                if i == total:
                    break
                i += int(freq)
                if st2 != 0:
                    print("Error: %s" % str(out2))
        newMapNameTpl2 = newMapNameTpl.replace("??", "loop")
        st, out = commands.getstatusoutput("convert -delay 75 -loop 0 %s.gif %s.gif" % \
          (newMapNameTpl, newMapNameTpl2))
        if st != 0:
            print("Error: %s" % str(out))


def run():
    """ """

    import sys
    import string
    import os
    import os.path

    parser = parseOpts()

    (options, args) = parser.parse_args()

    print(options)
    print(args)

    if len(args) < 1:
        parser.error("wrong number of arguments")

    global run
    global run_tmp

    clf()

    run = ''
    run_tmp = ''
    mapNames = []

    cFile = options.configfile
    fNames = args

    curdir = os.getcwd()

    ga = GaLab(Bin='grads',Window=False,Echo=False)
    mg = MapGenerator()

    for fName in fNames:
        os.chdir(curdir)

        ga.cmd("reinit")
        print('@@@@@', fName, '; ', cFile)
        OPTS = readConf(fName, cFile)
        print(OPTS)

        if not OPTS:
            print("Section '", fName, "' doesn't exist.")
            continue

        INDIR = options.indir or OPTS['indir']
        OUTDIR = options.outdir or OPTS['outdir']
        SOURCES = options.srcfile or OPTS['srcfile']
        SRCVAR = options.var or OPTS['var']
        SRCGAP = options.gap or OPTS['gap']
        BOUNDS = options.bounds or OPTS['bounds']
        BOUNDARIES = options.boundaries or OPTS['boundaries']
        COLORS = options.colors or OPTS['colors']
        TOTAL = options.total or OPTS['total']
        INTERVAL = options.interval or OPTS['interval']
        FREQ = options.freq or OPTS['freq']
        TITLE = options.title or OPTS['title']
        LAT = options.lat or OPTS['lat']
        LON = options.lon or OPTS['lon']
        OVER = options.over or OPTS['over']
        UNDER = options.under or OPTS['under']
        LIMITS = options.limits or OPTS['limits']
        WIND = options.wind or OPTS['wind']
        WINDOPTS = options.windopts or OPTS['windopts']
        RESOLUTION = options.resolution or OPTS['resolution']
        MAX = options.max or OPTS['max']
        ANIM = options.anim or OPTS['anim']

        print("OPTIONS:", """
        INDIR = %s
        OUTDIR = %s
        SOURCES = %s
        SRCVAR = %s
        SRCGAP = %s
        BOUNDS = %s
        BOUNDARIES = %s
        COLORS = %s
        TOTAL = %s
        INTERVAL = %s
        FREQ = %s
        TITLE = %s
        LAT = %s
        LON = %s
        OVER = %s
        UNDER = %s
        LIMITS = %s
        WIND = %s
        WINDOPTS = %s
        RESOLUTION = %s
        MAX = %s
""" % (INDIR, OUTDIR, SOURCES, SRCVAR, SRCGAP, BOUNDS, BOUNDARIES, COLORS,
TOTAL, INTERVAL, FREQ, TITLE, LAT, LON, OVER, UNDER, LIMITS, WIND,
WINDOPTS, RESOLUTION, MAX))

        # Open SOURCES
        for f in SOURCES:
            ga.open(INDIR + '/' + f)

        # Open WINDS if specified
        if WIND:
            ga.open(INDIR + '/' + WIND)
        os.chdir(OUTDIR)

        mg.bounds = BOUNDS
        mg.boundaries = BOUNDARIES

        figNames = []

        dims = ga.query("dims", Quiet=True)
        mx = None
        run_tmp = dims.time[0] #12:30Z30NOV2010
        if run_tmp[:-10] == "01:30": run_tmp = run_tmp.replace("01:30", "00")
        run = "%sh %s %s %s" % (run_tmp[:-10], run_tmp[-9:-7], run_tmp[-7:-4], run_tmp[-4:])

        valid_tmp = dims.time[1]
        valid = "%sz %s %s %s" % (valid_tmp[:-10], valid_tmp[-9:-7], valid_tmp[-7:-4], valid_tmp[-4:])

        mg.initMap(LAT,LON,RESOLUTION)

        for nTime in range(0,TOTAL,INTERVAL):
            DATA = None
            #GET DATA from SOURCES
            print("SOURCES: ", SOURCES, type(SOURCES), len(SOURCES))
            for src_n in range(0, len(SOURCES)):
                print(">>>>> CURRENT SRC " , src_n, ':', SOURCES[src_n])
                ga.cmd("set dfile %d" % (src_n + 1))
                ga.cmd("set lon %s %s" % (str(LON[0]), str(LON[1])))
                ga.cmd("set lat %s %s" % (str(LAT[0]), str(LAT[1])))
                ga.cmd("set t %s" % (nTime + int(SRCGAP[src_n])))
                if DATA != None:
                    print("DATALON: ", shape(DATA.data), " SHAPE LON: ", shape(DATA.grid.lon), " SHAPE LAT: ", shape(DATA.grid.lat))
                    lons, lats = meshgrid(DATA.grid.lon, DATA.grid.lat)
                    print("SHAPE lats/lons:", shape(lats), shape(lons), "lenghts: ", len(DATA.grid.lat), len(DATA.grid.lon))
                    VVV, AAA = ga.interp(SRCVAR[src_n], lons, lats)
                    #print "SHAPE: ", shape(VVV), type(VVV), shape(DATA.data), type(DATA.data)
                    #print "DATA: ", VVV.data[0:10]
                    print(shape(VVV), shape(AAA), type(VVV))
                    DATA += VVV.reshape(shape(DATA))
                else:
                    #VVV = ga.exp(SRCVAR[src_n])
                    #print "SHAPE: ", shape(VVV), type(VVV), VVV.grid.lon[0:10]
                    #print "DATA: ", VVV.data[0:10]
                    DATA = ga.exp(SRCVAR[src_n])

                #print "DATA %d: " % (src_n), DATA.grid.lon[0:10], type(DATA), shape(DATA)
                print("DATA: ", type(DATA), shape(DATA))
                print("DATALON: ", shape(DATA.data), " SHAPE LON: ", shape(DATA.grid.lon), " SHAPE LAT: ", shape(DATA.grid.lat))


            #Get wind data
            WINDS=None
            if WIND:
                WINDS = {'u': None, 'v': None}
                ga.cmd("set dfile %d" % (len(SOURCES) + 1))
                ga.cmd("set lon %s %s" % (str(LON[0]), str(LON[1])))
                ga.cmd("set lat %s %s" % (str(LAT[0]), str(LAT[1])))
                ga.cmd("set t %s" % (nTime+1))
                WINDS['u'] = ga.exp("skip(%s,%s,%s)" % (WINDOPTS[0], WINDOPTS[2], WINDOPTS[2]))
                WINDS['v'] = ga.exp("%s" % WINDOPTS[1])

            pTime = nTime*FREQ
            sTime = "%02d" % pTime
            figName = "%s-%s-%s" % (fName, sTime, run_tmp)

            print('title: ' , TITLE, ' ', type(TITLE))
            try:
                pTitle=unicode(TITLE.decode('utf-8')) % (sTime, valid)
            except Exception as e:
                print(e)
                pTitle=TITLE % (sTime, valid)

            figNames.append(mg.genImageMap(ga, figName, valid, DATA, pTitle, COLORS,
                BOUNDARIES, OVER, UNDER, winds=WINDS, limits=LIMITS))
            ## Calculate matrix of maxs
            if mx != None:
                mx = maximum(DATA, mx)
                print("M [0, 0]: ", mx.data[0][0], DATA.data[0][0])
            else:
                mx = DATA
                print("E [0, 0]: ", mx.data[0][0])

            # Create Max at requires intervals
            if MAX and nTime in MAX:
                figName = "%s-%s" % (fName, 'max+d%d' % (nTime/24))
                try:
                    pTitle=unicode(TITLE.decode('utf-8')) % ('Max %d' % (nTime + 1), valid)
                except:
                    pTitle=TITLE % (valid, run)
                # Here we don't draw winds
                mg.genImageMap(ga, figName, valid,
                    mx, pTitle, COLORS, BOUNDARIES, OVER, UNDER, limits=LIMITS)

        #generate animation. TODO: use imagemagick libs
        if ANIM:
            st, out = commands.getstatusoutput("convert -delay 75 -loop 0 %s-%s-*-%s.gif %s-%s-%s-loop.gif" % (figName, varName, run_tmp, runDate, figName, varName))
            if st != 0:
                print("Error: %s" % str(out))
                sys.exit(1)

        mapNames.append(figNames)

    num = len(mapNames)
    if num > 1:
        mg.compareMaps(mapNames)


if __name__ == "__main__":
    run()
