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
            global start_t, last_t
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
        ga.cmd("set lon %s %s" % (str(LON[0]), str(LON[1])))
        ga.cmd("set lat %s %s" % (str(LAT[0]), str(LAT[1])))
        ga.cmd("set t %s" % (nTime+1))

        dims = ga.query("dims", Quiet=True)

        print("nTime", nTime)
        if nTime == 0:
            global run_tmp
            global run
            run_tmp = dims.time[0] #12:30Z30NOV2010
            if run_tmp[:-10] == "01:30": run_tmp = run_tmp.replace("01:30", "00")
            if NORUNTIME:
                runt = "--"
            else:
                runt = run_tmp[:-10]
            run = "%sh %s %s %s" % (runt, run_tmp[-9:-7], run_tmp[-7:-4], run_tmp[-4:])
            print("run", run)

        valid_tmp = dims.time[1]
        valid = "%sh %s %s %s" % (valid_tmp[:-10], valid_tmp[-9:-7], valid_tmp[-7:-4], valid_tmp[-4:])

        nTime = nTime*FREQ
        sTime = "%02d" % nTime

        #ACMAD Section
        month = run_tmp[-7:-4]
        year = run_tmp[-4:]

        if ACMAD == '01':
            test_comp = "1-10 %s %s" % (month, year)
            #figName = "%s.%s.an%s.m%s.d01.10" % (varName.replace('_DUST','').lower(),modName,run_tmp[-4:],time.strftime('%m', time.strptime(run_tmp[-7:-4], '%b')))
            figName = "%s%s.d01.10-%s_%s" % (run_tmp[-4:],time.strftime('%m', time.strptime(run_tmp[-7:-4], '%b')), modName, varName.lower())
        elif ACMAD == '02':
            test_comp = "11-20 %s %s" % (month, year)
            #figName = "%s.%s.an%s.m%s.d11.20" % (varName.replace('_DUST','').lower(),modName,run_tmp[-4:],time.strftime('%m', time.strptime(run_tmp[-7:-4], '%b')))
            figName = "%s%s.d11.20-%s_%s" % (run_tmp[-4:],time.strftime('%m', time.strptime(run_tmp[-7:-4], '%b')), modName, varName.lower())
        elif ACMAD == '03':
            if month in ('NOV','APR','JUN','SEP'):
                days = '21-30'
            elif month == 'FEB':
                if int(year) % 4 != 0:
                    days = '21-28'
                else:
                    days = '21-29'
            else:
                days = '21-31'
            test_comp = "%s %s %s" % (days, month, year)
            #figName = "%s.%s.an%s.m%s.d21.30" % (varName.replace('_DUST','').lower(),modName,run_tmp[-4:],time.strftime('%m', time.strptime(run_tmp[-7:-4], '%b')))
            figName = "%s%s.d21.30-%s_%s" % (run_tmp[-4:],time.strftime('%m', time.strptime(run_tmp[-7:-4], '%b')), modName, varName.lower())
        elif ACMAD == '04':
            test_comp = "%s %s" % (month, year)
            figName = "%s%s-%s_%s" % (run_tmp[-4:],time.strftime('%m', time.strptime(run_tmp[-7:-4], '%b')), modName, varName.lower())
        elif ACMAD == '05':
            curm = datetime.strptime("%s %s" % (month, year), "%b %Y")
            newm = (curm - timedelta(days=60)).strftime("%b %Y").upper()
            test_comp = "%s - %s %s" % (newm, month, year)
            figName = "%s.%s.an%s.m%s" % (varName.replace('_DUST','').lower(),modName,run_tmp[-4:],time.strftime('%m', time.strptime(run_tmp[-7:-4], '%b')))
        elif ACMAD == '06':
            test_comp = "%s" % (year)
            figName = "%s.%s.an%s" % (varName.replace('_DUST','').lower(),modName,run_tmp[-4:])
        else:
            test_comp = (run, valid, 'H+'+sTime)
            #figName = "%s-%s-%s-%s" % (modName,varName,sTime,run_tmp)
            figName = "%s-%s-%s-%s" % (runDate, modName, varName, sTime)

        if os.path.exists(figName + ".gif") and not OVERWRITE:
            print(figName, " already exists.")
            clf()
            return figName

        if NODRAW and os.path.exists("%s-%s/%s.png" % (runDate, varName, figName)) and not OVERWRITE:
            print(figName, " already exists.")
            clf()
            return figName

        if NODRAW:
            axes(frameon=0)

        m = Basemap(
                projection='cyl', resolution=RESOLUTION, area_thresh=400.,
                llcrnrlon=LON[0], llcrnrlat=LAT[0], urcrnrlon=LON[1], urcrnrlat=LAT[1],
                )

        if TRANSF:
            ga.transf = TRANSF
        else:
            ga.transf = False

        var = ga.exp(varName+'*'+str(multiply))
        lons = ga.exp("lon")
        lats = ga.exp("lat")

        co = m.contourf(lons, lats, var,
            levels=self.bounds,
            cmap=self.cmap,
            norm=self.norm,
            extend=self.extend,
        )

#        Z1 = dot(ga.exp(varName), multiply)
#        g = Z1.grid
#        x, y = ga.map(*meshgrid(g.lon,g.lat))
#
#        ## Calculate matrix of maxs
#        if max != None:
#            max = maximum(Z1, max)
#            print "[0, 0]: ", max.data[0][0], Z1.data[0][0]
#        else:
#            max = Z1
#            print "E [0, 0]: ", max.data[0][0]
#
#        ga.contourf(Z1, N=len(self.bounds) - 1 , V=self.bounds,
#            clines=False, cbar=self.setColorBar, cmap=self.cmap, norm=self.norm, extend=self.extend)

#        m.contour(lons, lats, var,
#            levels=self.bounds,
#            norm=self.norm,
#            linewidths=.2,
#            colors=('grey'))

        if not NODRAW:

            m.drawcountries(linewidth=.3)
            m.drawmapboundary(fill_color='grey')
            m.drawcoastlines(linewidth=.4)

            cb = m.colorbar(co, size='3%', extend=self.extend)
            cb.set_ticklabels(self.bounds)

            #add states and parallels
            coord_int = int(COORDINT)
            #coords normalization
            lat_offset = abs(LAT[0]) % coord_int
            lon_offset = abs(LON[0]) % coord_int
            m.drawparallels(arange(LAT[0]+lat_offset, LAT[1], coord_int),labels=[1,0,0,0],linewidth=0.2)
            m.drawmeridians(arange(LON[0]+lon_offset, LON[1], coord_int),labels=[0,0,0,1],linewidth=0.2)

            #hide lakes
#            for j,cp in enumerate(m.coastpolygons):
#                if m.coastpolygontypes[j]<2:
#                    m.plot(cp[0],cp[1],'k-', linewidth=.4)

        if ACMAD in ('04','05','06') and modName == 'MODIS':
            ga.map.plot([-25,-18,-18,-25,-25,-25], [30,30,15,15,30,15], linewidth=2, color='red')

        if STATIONS:
            stlist = loadtxt(STATIONS, skiprows=1, dtype=str)
            stnam  = stlist.T[0]
            stlon  = stlist.T[1]
            stlat  = stlist.T[2]
            m.scatter(stlon, stlat, c='r', s=10, alpha=.5)

            for name,xpt,ypt in zip(stnam,stlon,stlat):
                if name == "OUAGADOUGOU_AERO":
                    text(float(xpt)-0.5, float(ypt)-0.2, name, color='k', fontsize=8)
                elif name in ("BOUTILIMIT", "BARKEOL", "KAEDI(IRAT)", "SELIBABY"):
                    text(float(xpt)-0.9, float(ypt)-0.3, name, color='k', fontsize=8)
                else:
                    text(float(xpt)+0.1, ypt, name, color='k', fontsize=8)

        #m.bluemarble()
        if BACKGROUND:
            m.shadedrelief()

        #logo
        if self.logo:
            im = Image.open(self.logo[0])
            height = im.size[1]
            width  = im.size[0]

            # We need a float array between 0-1, rather than
            # a uint8 array between 0-255
            nim = np.array(im).astype(np.float) / 255

            # With newer (1.0) versions of matplotlib, you can
            # use the "zorder" kwarg to make the image overlay
            # the plot, rather than hide behind it... (e.g. zorder=10)
            figimage(nim, self.logo[1], self.logo[2], zorder=10)

        print("printing ", figName, " ...")
        if NODRAW:
            savefig(figName + ".png", bbox_inches='tight', pad_inches=0, dpi=DPI, transparent=True)
        else:
            try:
                title(unicode(imgTitle.decode('utf-8')) % test_comp)
            except:
                title(imgTitle % test_comp)

            savefig(figName + ".png", bbox_inches='tight', pad_inches=.2, dpi=DPI)


        if not ACMAD:
            #convert from png to gif and delete png
            #st, out = commands.getstatusoutput("convert %s.png %s.gif" % (figName,figName)) #,figName))
            st, out = commands.getstatusoutput("convert %s.png %s.gif && rm %s.png" % (figName,figName,figName))
            st, out = commands.getstatusoutput("convert %s.png %s.gif && rm %s.png" % (figName2,figName2,figName2))
            if st != 0:
                print("Error: %s" % str(out))
                sys.exit(1)

        clf()

        self.printTime("convert")
        return figName


    def twoMapsCompare(self, mapNames, items):
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
                    retNames.append(newMapName)
                    try:
                        items[T].append(item1)
                    except:
                        items[T] = [item0, item1]
                    break

#                    if st != 0:
#                        print "Error: %s" % str(out)
#                    else:
#                        #print "==>", newMapName, "<=="
#                        retNames.append(newMapName)
#                        break

#            comm = "montage %s.gif -tile 2x -geometry 800x600+1+1 %s.gif" %\
#             (items, newMapName)
#            print "COMPARE COMMAND:", comm
#            st, out = commands.getstatusoutput(comm)

#        print "RETNAMES", retNames
#        print "********************* ITEMS ********************"
#        print items
#        print "************************************************"

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

    error_msg = """\
    Usage: %s <file> <varname>""" % sys.argv[0]

    if len(sys.argv) not in (3,4):
        print(error_msg)
        sys.exit(1)

    global run
    global run_tmp
    global ACMAD

    clf()

    run = ''
    run_tmp = ''
    mapNames = []

    fNames = sys.argv[1].split(',')
    varName = sys.argv[2]

    if len(sys.argv) == 4:
        ACMAD = sys.argv[3]
    else: ACMAD = ''

    curdir = os.getcwd()

    os.chdir(INDIR)
    ga = GaLab(Bin='grads',Window=False,Echo=False)
    mg = MapGenerator()

    MLEN = len(fNames)

    for fName in fNames:
        #os.chdir(curdir)

        if not os.path.exists(INDIR + '/' + fName):
            print("File '", fName, "' doesn't exist.")
            continue

        ga.cmd("reinit")
        ga.open(fName)

        ext = fName.split('.')[-1:][0]
        modName = '_'.join(fName.split('_')[1:]).replace('.' + ext,'')
        runDate = fName.split('_')[0]
        mg.rundate = runDate

        for sec in OPTS.keys():
            data = sec.split('-')
            secMod = '-'.join(data[:-1]) #unify all elements without the last one
            secVar = data[-1:][0] #I suppose the last element is the variable
            if secMod == modName and secVar == varName:
                imgTitle = OPTS[sec]['title']
                multiply = OPTS[sec]['mul']
                BOUNDS = OPTS[sec]['bounds']
                BOUNDARIES = OPTS[sec]['boundaries']
                anim = OPTS[sec]['anim']
                if OPTS[sec].has_key('colors'):
                    COLORS = OPTS[sec]['colors']
                if OPTS[sec].has_key('indir'):
                    INDIR = OPTS[sec]['indir']
                if OPTS[sec].has_key('outdir'):
                    OUTDIR = OPTS[sec]['outdir']
                if OPTS[sec].has_key('resolution'):
                    RESOLUTION = OPTS[sec]['resolution']
                if OPTS[sec].has_key('coordint'):
                    COORDINT = OPTS[sec]['coordint']
                if OPTS[sec].has_key('longitude'):
                    LON = OPTS[sec]['longitude']
                if OPTS[sec].has_key('latitude'):
                    LAT = OPTS[sec]['latitude']
                if OPTS[sec].has_key('under'):
                    UNDER = OPTS[sec]['under']
                if OPTS[sec].has_key('over'):
                    OVER = OPTS[sec]['over']
                if OPTS[sec].has_key('interval'):
                    INTERVAL = OPTS[sec]['interval']
                if OPTS[sec].has_key('freq'):
                    FREQ = OPTS[sec]['freq']
                if OPTS[sec].has_key('total'):
                    TOTAL = OPTS[sec]['total']
                if OPTS[sec].has_key('togif'):
                    TOGIF = OPTS[sec]['togif']
                if OPTS[sec].has_key('overwrite'):
                    OVERWRITE = OPTS[sec]['overwrite']
                if OPTS[sec].has_key('logo'):
                    LOGO = OPTS[sec]['logo']
                if OPTS[sec].has_key('stations'):
                    STATIONS = OPTS[sec]['stations']
                else:
                    STATIONS = None
                if OPTS[sec].has_key('noruntime'):
                    NORUNTIME = OPTS[sec]['noruntime']
                else:
                    NORUNTIME = None
                if OPTS[sec].has_key('background'):
                    BACKGROUND = OPTS[sec]['background']
                else:
                    BACKGROUND = None
                if OPTS[sec].has_key('dpi'):
                    DPI = OPTS[sec]['dpi']
                else:
                    DPI = None
                if OPTS[sec].has_key('transf'):
                    TRANSF = OPTS[sec]['transf']
                else:
                    TRANSF = False
                if OPTS[sec].has_key('nodraw'):
                    NODRAW = OPTS[sec]['nodraw']
                else:
                    NODRAW = False
                break

        os.chdir(OUTDIR)

        mg.bounds = BOUNDS
        mg.boundaries = BOUNDARIES
        mg.logo = LOGO
        mg.setNorm()
        mg.setExtend()
        mg.setColorMap()

        figNames = []
        for nTime in range(0,TOTAL,INTERVAL):
            figNames.append(mg.genImageMap(ga, modName, varName, multiply, nTime, imgTitle, runDate))

        if NODRAW:
            clf()

            #separate colorbar
            mpl.rcParams['axes.linewidth'] = 0.1
            fig = figure(figsize=(.1,12))
            ax = fig.add_axes([0.05, 0.80, 0.9, 0.15], axisbg=(1,1,1,0))
            cb = mpl.colorbar.ColorbarBase(ax, cmap=mg.cmap, norm=mg.norm, ticks=mg.bounds, extend=mg.extend, drawedges=False)
            setp(getp(ax, 'yticklabels'), color='w')
            setp(getp(ax, 'yticklabels'), fontsize=6)
            for lin in cb.ax.yaxis.get_ticklines():
                lin.set_visible(False)

            tit = unicode(imgTitle.decode('utf-8'))
            idx1 = tit.find('(')
            idx2 = tit.find(')')
            varUnit = tit[idx1:idx2+1]
            if varUnit.find("%s") >= 0:
                varUnit = ''
            xlabel(
                "%s\n%s" % (varName, varUnit),
                horizontalalignment='left',
                color='w',
                fontsize=6,
            )
            ax.xaxis.set_label_coords(-0.025,-0.025)

            try:
                os.mkdir("%s-%s" % (runDate, varName))
            except:
                pass

            fig.savefig("%s-%s/%s-colorbar.png" % (runDate, varName, runDate), bbox_inches='tight', pad_inches=0, dpi=DPI, transparent=True)

            #generate KMZ - Offline
            print("Generating KMZ ...")
            mg.genKML(LON, LAT, figNames, runDate, online=False)

            #generate KML - Online
            print("Generating KML ...")
            mg.genKML(LON, LAT, figNames, runDate)

        #generate animation. TODO: use imagemagick libs
        if anim:
            st, out = commands.getstatusoutput("convert -delay 75 -loop 0 %s-%s-*-%s.gif %s-%s-%s-loop.gif" % (modName, varName, run_tmp, runDate, modName, varName))
            st, out = commands.getstatusoutput("convert -delay 75 -loop 0 %s-%s-%s-??.gif %s-%s-%s--loop-.gif" % (runDate, modName, varName, runDate, modName, varName))
            if st != 0:
                print("Error: %s" % str(out))
                sys.exit(1)

        mapNames.append(figNames)

    num = len(mapNames)
    if num > 1:
        mg.compareMaps(mapNames, FREQ*INTERVAL, TOTAL)
