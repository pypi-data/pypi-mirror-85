#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset as nc

from datetime import datetime, timedelta
import sys
import shutil


### GLOBAL VARIABLES
VARNAME = 'dust_conc'
MULTVAR = 1e9
BOUNDS = (10, 20, 40, 80, 160, 320, 640, 1280, 2650)
COLORS = ('#A1EDE3', '#5DE3BB', '#53BD9D', '#FCCA26', '#E5724C', '#944038', '#AB025C', '#7A54C2')
OVER = '#A9A9A9'
UNDER = '#ffffff'

# Temporal resolution of original data
FREQ = 3
# Timestep interval to plot
INT = 2
# Timesteps to plot (if < total timesteps of data)
TLIMIT = 24

# Lon/Lat line style
LSTYLE = '--'

LINEWIDTH = .3
FONTSIZE = 10

# LIMITS
LON0 = -25
LON1 = 60
LAT0 = 0
LAT1 = 60

LEV0_INDEX = 0
LEV1_INDEX = -1

# PATH OUT
POUT = './out/medi/'

# MISSINGVALUE
MVAL = -32767.

# FILLCOLOR
FILLCOLOR = 'white'

# YLIM
Y0LIM = 0
Y1LIM = 12

DTYPE = float32

DEBUG = True

def findCoordIndex(carray, cval):
    tmp0 = np.where(carray>cval)
    tmp1 = np.where(carray<=cval)
    #if DEBUG:
    #   print "***", tmp0[0], tmp1[0], cval, "***"
    cmax = cmin = 0
    if tmp0[0].any():
        cmax = tmp0[0][0]
    if tmp1[0].any():
        cmin = tmp1[0][-1]
    if abs(cval-carray[cmax]) >= abs(cval-carray[cmin]):
        return cmin
    return cmax

def createTicks(vec, off):
    noff = abs(vec[0])%off
    return np.arange(vec[0]+noff, vec[-1], off)

def createCLabel(coord, t='lon'):
    if type(coord) is np.ndarray:
        xts0 = [u"%d°" % int(abs(i)) for i in coord if int(i) == 0]
        if t == 'lon':
            xtsW = [u"%d°W" % int(abs(i)) for i in coord if int(i) < 0]
            xtsE = [u"%d°E" % int(abs(i)) for i in coord if int(i) > 0]
            return xtsW + xts0 + xtsE
        else:
            xtsS = [u"%d°S" % int(abs(i)) for i in coord if int(i) < 0]
            xtsN = [u"%d°N" % int(abs(i)) for i in coord if int(i) > 0]
            return xtsS + xts0 + xtsN
    else:
        if coord == 0: ncoord = u"0°"
        elif coord < 0:
            if t == 'lon': ncoord = u"%s°W" % abs(coord)
            else: ncoord = u"%s°S" % abs(coord)
        elif coord > 0:
            if t == 'lon': ncoord = u"%s°E" % abs(coord)
            else: ncoord = u"%s°N" % abs(coord)
        return ncoord


if __name__ == "__main__":

    NCNAME = sys.argv[1]
    TXNAME = sys.argv[2]

    CLEVS = 25
    THLIM = 260
    IU = 2
    JU = 20
    NORM = mpl.colors.BoundaryNorm(BOUNDS, len(BOUNDS)-1, clip=True)
    mpl.rcParams.update({'font.size': FONTSIZE})

    title1 = u"""$http://www.bsc.es/projects/earthscience/NMMB-BSC-DUST/$
    NMMB/BSC-Dust Dust Concentration (µg/m³), Wind, Pot.Temp. LON = %s
    %sh forecast for %02dUTC %02d %s %s"""

    title2 = u"""NMMB/BSC-Dust Dust Concentration (µg/m³), Wind, Pot.Temp. LAT = %s
    %sh forecast for %02dUTC %02d %s %s"""

    #LON:2, LAT:3, STNAME:5
    if DEBUG:
        print("Loading stations ...")
    STLIST = np.loadtxt(TXNAME, delimiter=';', skiprows=1, dtype='str')

    if DEBUG:
        print("Loading NetCDF ...")
    f = nc(NCNAME, 'r')

    if DEBUG:
        print("Loading Coords ...")
    lons = f.variables['lon'][:].astype(DTYPE)
    lats = f.variables['lat'][:].astype(DTYPE)

    if DEBUG:
        print("FindCoordIndexes ...")
    LON0_INDEX = findCoordIndex(lons, LON0)
    LON1_INDEX = findCoordIndex(lons, LON1)
    LAT0_INDEX = findCoordIndex(lats, LAT0)
    LAT1_INDEX = findCoordIndex(lats, LAT1)

    lons = lons[LON0_INDEX:LON1_INDEX]
    lats = lats[LAT0_INDEX:LAT1_INDEX]
    #level = level[LEV0_INDEX:LEV1_INDEX]

    if DEBUG:
        print("Loading Main Var ...")
    main_var = f.variables[VARNAME][:,LEV0_INDEX:LEV1_INDEX,LAT0_INDEX:LAT1_INDEX,LON0_INDEX:LON1_INDEX].astype(DTYPE)
    main_var = (np.ma.masked_where(main_var == MVAL, main_var)*MULTVAR).astype(DTYPE)
    if DEBUG:
        print("Main Var Memory Usage:", main_var.nbytes)

    if DEBUG:
        print("Loading Z ...")
    z = f.variables['fis'][:,LAT0_INDEX:LAT1_INDEX,LON0_INDEX:LON1_INDEX].astype(DTYPE)
    z = (np.ma.masked_where(z == MVAL, z)/9800).astype(DTYPE)
    if DEBUG:
        print("Z Memory Usage:", z.nbytes)

    if DEBUG:
        print("Loading Time ...")
    v_time = f.variables['time']
    time = v_time[:]
    units = v_time.units

    if DEBUG:
        print("Loading HSL ...")
    hlevel = f.variables['hsl'][:,LEV0_INDEX:LEV1_INDEX,LAT0_INDEX:LAT1_INDEX,LON0_INDEX:LON1_INDEX].astype(DTYPE)
    hlevel = (np.ma.masked_where(hlevel == MVAL, hlevel)/1000).astype(DTYPE)
    if DEBUG:
        print("HSL Memory Usage:", hlevel.nbytes)

    if DEBUG:
        print("Loading TSL ...")
    tlevel = f.variables['tsl'][:,LEV0_INDEX:LEV1_INDEX,LAT0_INDEX:LAT1_INDEX,LON0_INDEX:LON1_INDEX].astype(DTYPE)
    tlevel = np.ma.masked_where(tlevel == MVAL, tlevel).astype(DTYPE)
    if DEBUG:
        print("TSL Memory Usage:", tlevel.nbytes)

    if DEBUG:
        print("Loading PRES ...")
    plevel = (f.variables['pres'][:]*100).astype(DTYPE)

    if DEBUG:
        print("Creating ones ...")
    level = (ones(hlevel.shape)*MVAL).astype(DTYPE)
    th = (ones(hlevel.shape)*MVAL).astype(DTYPE)

    if DEBUG:
        print("Populating tmplevel and tmpth ...")
    for tt in range(0,len(time)):
        for l in range(0,hlevel.shape[1]):
            level[tt,l,:,:] = hlevel[tt,l,:,:]
            th[tt,l,:,:] = tlevel[tt,l,:,:]*((100000/plevel[l])**0.286) #taking reference pressure at 1000kPa

    if DEBUG:
        print("Deleting tmp arrays ...")
    del plevel
    del hlevel
    del tlevel

    if DEBUG:
        print("Creating level and th ...")
    level = np.ma.masked_where(level == MVAL, level).astype(DTYPE)
    th = np.ma.masked_where(th == MVAL, th).astype(DTYPE)

    if DEBUG:
        print("++++++++++++++++++++++++++++++++++++++++++++++")
        print("LEVEL", level.shape)
        print("++++++++++++++++++++++++++++++++++++++++++++++")
        print("TH", th.shape)
        print("++++++++++++++++++++++++++++++++++++++++++++++")

    if DEBUG:
        print("Loading USL ...")
    udat = f.variables['usl_h'][:,LEV0_INDEX:LEV1_INDEX,LAT0_INDEX:LAT1_INDEX,LON0_INDEX:LON1_INDEX].astype(DTYPE)
    udat = (np.ma.masked_where(udat == MVAL, udat)*2).astype(DTYPE)
    if DEBUG:
        print("UDAT Memory Usage:", udat.nbytes)

    if DEBUG:
        print("Loading VSL ...")
    vdat = f.variables['vsl_h'][:,LEV0_INDEX:LEV1_INDEX,LAT0_INDEX:LAT1_INDEX,LON0_INDEX:LON1_INDEX].astype(DTYPE)
    vdat = (np.ma.masked_where(vdat == MVAL, vdat)*2).astype(DTYPE)
    if DEBUG:
        print("VDAT Memory Usage:", vdat.nbytes)

    cmap = mpl.colors.ListedColormap(COLORS)
    cmap.set_over(OVER)
    cmap.set_under(UNDER)

    TIME = datetime.strptime(units.replace('hours since ',''), "%Y-%m-%d %H:%M:%S")
    TIME_INIT = TIME

    TDGNUM = time.max() < 100 and "%02d" or "%03d"

    for line in STLIST:

        clf()
        LON = float(line[2])
        LAT = float(line[3])
        STNAME = line[5]
        TIME = TIME_INIT

        print("Station", STNAME, "LON", LON, "LAT", LAT)

        try:
            LON_INDEX = findCoordIndex(lons, LON)
            LAT_INDEX = findCoordIndex(lats, LAT)
        except:
            print("Coords not found. Continue")
            continue

        print("TIME", range(int(time[0]),int(time[-1])+INT*FREQ, INT*FREQ))

        for t in range(0,len(time),INT):
            plt.clf()
            step = TDGNUM % (t*FREQ)
            print("TIME", t, "STEP", step)

            MONTH = TIME.strftime("%b").upper()

            # data plot (t, var, idx, typ
            #dplot(t, lats, LON_INDEX, 'lat')
            #dplot(t, lons, LAT_INDEX, 'lon')

            # PLOT 1
            data1 = main_var[t,:,:,LON_INDEX]
            level1 = level[t,:,:,LON_INDEX]
            lats1 = lats.repeat(level1.shape[0]).reshape(lats.shape[0],level1.shape[0]).T
            z1 = z[t,:,LON_INDEX]
            thtemp = th[t,:,:,LON_INDEX]
            th1 = np.ma.masked_where(thtemp < THLIM, thtemp)
            udat1 = udat[t,:,:,LON_INDEX]
            for i in range(0, udat1.shape[0]):
                for j in range(0, udat1.shape[1]):
                    if i%IU == 0 and j%JU == 0:
                        continue
                    udat1[i,j] = np.ma.masked
            vdat1 = np.ma.masked_array(vdat[t,:,:,LON_INDEX])
            print("DATA", data1.shape, "LEV", level1.shape, "LATS", lats1.shape, "z1", z1.shape, "th1", th1.shape)

            xtmp = createTicks(lats, 10)
            xts = createCLabel(xtmp, 'lat')

            ax1 = plt.subplot(211)
            co = ax1.contourf(lats1, level1, data1, BOUNDS, cmap=cmap, norm=NORM, antialiased=True, extend='both')
            cs = ax1.contour(lats1, level1, th1, CLEVS, linewidths=LINEWIDTH, colors='red', antialiased=True)
            plt.clabel(cs, fontsize=8, fmt='%1d', inline=1)
            plt.colorbar(co, use_gridspec=True)
            ax1.barbs(lats1, level1, udat1, vdat1, length=6, barbcolor='k', linewidth=LINEWIDTH, sizes = {'emptybarb' : 0})
            ax1.plot([lats[LAT_INDEX],lats[LAT_INDEX]], [level1[0],level1[-1]], 'k'+LSTYLE, linewidth=.3)
            ax1.plot(lats1[0], z1, 'k-', linewidth=LINEWIDTH+2.0, zorder=5)
            ax1.fill_between(lats1[0], 0, z1, color=FILLCOLOR, zorder=4)
            ax1.set_xticks(xtmp)
            ax1.set_xticklabels(xts)
            ax1.set_ylabel('altitude (km)')
            ax1.set_xlim([lats[0],lats[-1]])
            ax1.set_ylim([Y0LIM,Y1LIM])
            plt.title(title1 % (createCLabel(LON), step, TIME.hour, TIME.day, MONTH, TIME.year), fontsize=FONTSIZE)
            plt.grid(True)

            # PLOT 2
            data2 = main_var[t,:,LAT_INDEX,:]
            level2 = level[t,:,LAT_INDEX,:]
            lons2 = lons.repeat(level2.shape[0]).reshape(lons.shape[0],level2.shape[0]).T
            z2 = z[t,LAT_INDEX,:]
            thtemp = th[t,:,LAT_INDEX,:]
            th2 = np.ma.masked_where(thtemp < THLIM, thtemp)
            udat2 = udat[t,:,LAT_INDEX,:]
            for i in range(0, udat2.shape[0]):
                for j in range(0, udat2.shape[1]):
                    if i%IU == 0 and j%JU == 0:
                        continue
                    udat2[i,j] = np.ma.masked
            vdat2 = vdat[t,:,LAT_INDEX,:]

            xtmp = createTicks(lons, 10)
            xts = createCLabel(xtmp, 'lon')

            ax2 = plt.subplot(212)
            co = ax2.contourf(lons2, level2, data2, BOUNDS, cmap=cmap, norm=NORM, antialiased=True, extend='both')
            cs = ax2.contour(lons2, level2, th2, CLEVS, linewidths=LINEWIDTH, colors='red', antialiased=True)
            plt.clabel(cs, fontsize=8, fmt='%1d', inline=1)
            plt.colorbar(co, use_gridspec=True)
            ax2.barbs(lons2, level2, udat2, vdat2, length=6, barbcolor='k', linewidth=LINEWIDTH, sizes = {'emptybarb' : 0})
            ax2.plot([lons[LON_INDEX],lons[LON_INDEX]], [level2[0],level2[-1]], 'k'+LSTYLE, linewidth=.3)
            ax2.plot(lons2[0], z2, 'k-', linewidth=LINEWIDTH+2.0, zorder=5)
            ax2.fill_between(lons2[0], 0, z2, color=FILLCOLOR, zorder=4)
            ax2.set_xticks(xtmp)
            ax2.set_xticklabels(xts)
            ax2.set_ylabel('altitude (km)')
            ax2.set_xlim([lons[0],lons[-1]])
            ax2.set_ylim([Y0LIM,Y1LIM])
            plt.title(title2 % (createCLabel(LAT, t='lat'), step, TIME.hour, TIME.day, MONTH, TIME.year), fontsize=FONTSIZE)
            plt.grid(True)

            plt.subplots_adjust(bottom=.05, hspace=.3, left=.1, right=1)

            print("Saving images", step, STNAME, "..." #date.crsc.station.XX.gif)
            #savefig(POUT + "%s%02d%02d12.crsc.%s.%s.png" % (TIME.year, TIME.month, TIME.day, STNAME, step))

            NFILE1 = "%scrsc.%s.%s.png" % POUT, STNAME, step
            NFILE2 = "%s%s%02d%02d12.crsc.%s.%s.png" % POUT, TIME_INIT.year, TIME_INIT.month, TIME_INIT.day, STNAME, step
            plt.savefig(NFILE2)
            shutil.copy(NFILE2, NFILE1)

            TIME = TIME + timedelta(hours=(INT*FREQ))

            if t > TLIMIT:
                continue
