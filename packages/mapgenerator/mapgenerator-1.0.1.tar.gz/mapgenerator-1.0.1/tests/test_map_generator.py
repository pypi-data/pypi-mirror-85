#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Francesco Benincasa <francesco.benincasa@bsc.es>

import subprocess
import time
from config import *
from pylab import *
from grads import *
import matplotlib as mpl
mpl.use('Agg')


VERSION = "0.1beta"

BOUNDS = []
BOUNDARIES = None


def setColorMap():
    """ create color map """
    cmap = mpl.colors.ListedColormap(COLORS)
    if OVER:
        cmap.set_over(OVER)
    if UNDER:
        cmap.set_under(UNDER)
    cmap.set_bad('red')

    return cmap


def setColorBar(drawedges=False, cax=None):
    """ create color bar """
    bounds = BOUNDS
    boundaries = BOUNDARIES
    # print bounds, boundaries
    extend = 'neither'
    if type(boundaries) is list:
        boundaries = [boundaries[0]] + bounds + [boundaries[1]]
        extend = 'both'
    else:
        if UNDER:
            boundaries = [boundaries] + bounds
            extend = 'min'
        if OVER:
            boundaries = bounds + [boundaries]
            extend = 'max'

    # print boundaries, extend
    norm = mpl.colors.BoundaryNorm(bounds, len(bounds)-1, clip=True)
    cb = mpl.colorbar.ColorbarBase(drawedges=drawedges,
                                   ax=cax,
                                   cmap=cmap,
                                   norm=norm,
                                   # to use 'extend', you must
                                   # specify two extra boundaries:
                                   boundaries=boundaries,
                                   extend=extend,
                                   ticks=bounds,  # optional
                                   spacing='uniform',
                                   orientation='vertical')

    return cb


def genImageMap(ga, modName, varName, multiply, nTime, imgTitle):
    """ generate image map """

    clf()
    ga.cmd("set lon %s %s" % (str(LON[0]), str(LON[1])))
    ga.cmd("set lat %s %s" % (str(LAT[0]), str(LAT[1])))
    ga.cmd("set t %s" % (nTime+1))

    dims = ga.query("dims", Quiet=True)

    print("nTime", nTime)
    if nTime == 0:
        global run_tmp
        global run
        run_tmp = dims.time[0]  # 12Z30NOV2010
        run = "%sh %s %s %s" % (
            run_tmp[:2], run_tmp[3:5], run_tmp[5:8], run_tmp[8:])
        print("run", run)

    valid_tmp = dims.time[1]
    valid = "%sh %s %s %s" % (
        valid_tmp[:2], valid_tmp[3:5], valid_tmp[5:8], valid_tmp[8:])

    ga.basemap(resolution='l')
    ga.transf = True
    ga.contourf(varName, mul=multiply, N=len(BOUNDS)-1, V=BOUNDS,
                cbar=setColorBar, clines=False, colors=COLORS)  # , cbar=None)

    # add states and parallels
    coord_int = 10
    # coords normalization
    lat_offset = abs(LAT[0]) % coord_int
    lon_offset = abs(LON[0]) % coord_int
    ga.map.drawcountries(linewidth=0.7)
    ga.map.drawparallels(arange(
        LAT[0]+lat_offset, LAT[1], coord_int), labels=[1, 0, 0, 0], linewidth=0.2)
    ga.map.drawmeridians(arange(
        LON[0]+lon_offset, LON[1], coord_int), labels=[0, 0, 0, 1], linewidth=0.2)

    nTime = nTime*FREQ

    if len(str(nTime)) < 2:
        sTime = '0' + str(nTime)
    else:
        sTime = str(nTime)

    month = run_tmp[-7:-4]
    year = run_tmp[-4:]

    if ACMAD == '01':
        test_comp = "1-10 %s %s" % (month, year)
        figName = "%s.%s.an%s.m%s.d01.10" % (varName.replace('_DUST', '').lower(
        ), modName, run_tmp[-4:], time.strftime('%m', time.strptime(run_tmp[-7:-4], '%b')))
    elif ACMAD == '02':
        test_comp = "11-20 %s %s" % (month, year)
        figName = "%s.%s.an%s.m%s.d11.20" % (varName.replace('_DUST', '').lower(
        ), modName, run_tmp[-4:], time.strftime('%m', time.strptime(run_tmp[-7:-4], '%b')))
    elif ACMAD == '03':
        if month in ('NOV', 'APR', 'JUN', 'SEP'):
            days = '21-30'
        elif month == 'FEB':
            if int(year) % 4 != 0:
                days = '21-28'
            else:
                days = '21-29'
        else:
            days = '21-31'
        test_comp = "%s %s %s" % (days, month, year)
        figName = "%s.%s.an%s.m%s.d21.30" % (varName.replace('_DUST', '').lower(
        ), modName, run_tmp[-4:], time.strftime('%m', time.strptime(run_tmp[-7:-4], '%b')))
    elif ACMAD == '04':
        test_comp = "%s %s" % (month, year)
        figName = "%s.%s.an%s.m%s" % (varName.replace('_DUST', '').lower(
        ), modName, run_tmp[-4:], time.strftime('%m', time.strptime(run_tmp[-7:-4], '%b')))
    else:
        test_comp = (run, valid, 'H+'+sTime)
        figName = "%s-%s-%s-%s" % (modName, varName, sTime, run_tmp)

    try:
        title(unicode(imgTitle.decode('utf-8')) % test_comp)
    except:
        title(imgTitle % test_comp)

    print("printing ", figName, " ...")
    savefig(figName + ".png")
    clf()

    if TOGIF:
        # convert from png to gif and delete png
        st, out = subprocess.getstatusoutput(
            "convert %s.png %s.gif && rm %s.png" % (figName, figName, figName))
        if st != 0:
            print("Error: %s" % str(out))
            sys.exit(1)

    return figName


def compareMaps(mapNames):
    """ generate Maps Comparison """

    for item0 in mapNames[0]:
        # print "loop 1"
        idx0 = str(mapNames[0].index(item0))
        if len(idx0) == 1:
            idx0 = '0' + idx0
        runDate0 = item0.split('-')[-1:][0][-9:]
        runHour0 = item0.split('-')[-1:][0][:2]
        hOffset0 = item0.split('-')[-2:-1][0]
        var0 = item0.split('-')[-3:-2][0]
        mod0 = '-'.join(item0.split('-')[:-3])

        newDate0 = time.strftime('%Y%m%d', time.strptime(runDate0, "%d%b%Y"))

        for item1 in mapNames[1]:
            # print "loop 2"
            idx1 = str(mapNames[1].index(item1))
            if len(idx1) == 1:
                idx1 = '0' + idx1
            runDate1 = item1.split('-')[-1:][0][-9:]
            runHour1 = item1.split('-')[-1:][0][:2]
            hOffset1 = item1.split('-')[-2:-1][0]
            var1 = item1.split('-')[-3:-2][0]
            mod1 = '-'.join(item1.split('-')[:-3])

            newDate1 = time.strftime(
                '%Y%m%d', time.strptime(runDate1, "%d%b%Y"))

            if (runDate0 != runDate1):
                print("Error: different date, comparison impossible.")
                continue

            if (var0 != var1):
                print("Error: different variable, comparison impossible.")
                continue

            if (int(runHour0)+int(hOffset0)) == (int(runHour1)+int(hOffset1)):
                st, out = subprocess.getstatusoutput("convert +append %s.gif %s.gif %s-%s-%s-compared-map-%s-%s.gif" %
                                                   (item0, item1, newDate0, mod0, mod1, var0, idx0))

                if st != 0:
                    print("Error: %s" % str(out))
                else:
                    break

    st, out = subprocess.getstatusoutput("convert -delay 75 -loop 0 %s-%s-%s-compared-map-%s-??.gif %s-%s-%s-compared-map-%s-loop.gif" %
                                       (newDate0, mod0, mod1, var0, newDate0, mod0, mod1, var0,))
    if st != 0:
        print("Error: %s" % str(out))


if __name__ == "__main__":
    import os
    import sys
    import string

    error_msg = """\
    Usage: %s <file> <varname>""" % sys.argv[0]

    if len(sys.argv) not in (3, 4):
        print(error_msg)
        sys.exit(1)

    global cmap
    global run
    global run_tmp
    global ACMAD

    clf()

    run = ''
    run_tmp = ''
    mapNames = []
    cmap = setColorMap()

    fNames = sys.argv[1].split(',')
    varName = sys.argv[2]

    if len(sys.argv) == 4:
        ACMAD = sys.argv[3]

    curdir = os.getcwd()

    ga = GaLab(Bin='grads', Window=False, Echo=False)

    for fName in fNames:
        os.chdir(curdir)
        ga.cmd("reinit")
        ga.open(INDIR + '/' + fName)
        os.chdir(OUTDIR)

        modName = '_'.join(fName.split('_')[1:]).replace('.nc', '')
        runDate = fName.split('_')[0]

        for sec in OPTS.keys():
            data = sec.split('-')
            # unify all elements without the last one
            secMod = '-'.join(data[:-1])
            secVar = data[-1:][0]  # I suppose the last element is the variable
            if secMod == modName and secVar == varName:
                imgTitle = OPTS[sec]['title']
                multiply = OPTS[sec]['mul']
                BOUNDS = OPTS[sec]['bounds']
                BOUNDARIES = OPTS[sec]['boundaries']
                anim = OPTS[sec]['anim']
                INTERVAL = OPTS[sec]['interval']
                FREQ = OPTS[sec]['freq']
                TOTAL = OPTS[sec]['total']
                TOGIF = OPTS[sec]['togif']
                break

        figNames = []
        for nTime in range(0, TOTAL, INTERVAL):
            figNames.append(genImageMap(
                ga, modName, varName, multiply, nTime, imgTitle))

        # generate animation. TODO: use imagemagick libs
        if anim:
            st, out = subprocess.getstatusoutput("convert -delay 75 -loop 0 %s-%s-*-%s.gif %s-%s-%s-loop.gif" % (
                modName, varName, run_tmp, runDate, modName, varName))
            if st != 0:
                print("Error: %s" % str(out))
                sys.exit(1)

        mapNames.append(figNames)

    # comparing different (2) models
    # MODNAME-VAR-ISTANT-HHZDATE
    # 3H_MACC-ECMWF-SCONC_DUST-12-00Z18JAN2011.gif

    num = len(mapNames)
    if num > 2:
        print("Error: comparison only between 2 files.")
        sys.exit(1)
    if num > 1:
        compareMaps(mapNames)
