#!/usr/bin/env python
# coding: utf-8


import matplotlib.pyplot as plt
plt.style.use('ggplot')
import pandas as pd
import numpy as np
from netCDF4 import Dataset as nc
from scipy.interpolate import RectBivariateSpline
from datetime import datetime, timedelta
from os.path import basename
from glob import glob
import os
import os.path
import logging
logging.basicConfig(level=logging.DEBUG)


class Evaluator(object):


    def __init__(self, str_date, end_date, obs_path, mod_path, obs_tmpl, mod_tmpl, dir_outp="./out/", rej_path=None, rej_tmpl=None, en_debug=False):
        """Initialize attributes"""

        self.str_date = str_date            # start date YYYYMMDD
        self.end_date = end_date            # end date YYYYMMDD
        self.obs_path = obs_path            # observation path
        self.mod_path = mod_path            # model path
        self.rej_path = rej_path            # observation path
        self.obs_tmpl = obs_tmpl            # observation template files
        self.mod_tmpl = mod_tmpl            # model template files
        self.rej_tmpl = rej_tmpl            # model path
        self.dir_outp = dir_outp            # output directory
        self.obs_list = []                  # observation files list
        self.mod_list = []                  # model files list
        self.lon_bnds = ()                  # lon bounds
        self.lat_bnds = ()                  # lat bounds
        self.obs_type = 'ASSIMILATION'      # obs type
        self.variable = 'OD550_DUST'        # variable name
        self.mod_vlon = 'lon'               # lon name
        self.mod_vlat = 'lat'               # lat name
        self.mod_name = 'AOD_MOD'           # model label
        self.obs_name = 'AOD_OBS'           # observation label
        self.plt_xlim = ()                  # plot x bounds
        self.plt_ylim = ()                  # plot y bounds
        self.plt_titl = ''                  # plot title
        self.plt_type = 'xy'                # types:
                                            # 'xy': model in x and observation in y
                                            # 'ts': time series with line
                                            # 'tss': time series with scatter
        self.tmp_tmpl = '/tmp/%s_obs_file.txt'
        self.plt_imag = "image.png"
        self.fil_stat = "stats.txt"
        self.date_fmt = "%Y%m%d"
        self.mylogger = en_debug and logging.getLogger(__name__)

        if not os.path.exists(dir_outp):
            os.makedirs(dir_outp)


    def getDateDict(self, dd):

        sdict = {
            'date' : dd.strftime(self.date_fmt),
            'year' : dd.strftime('%Y'),
            'month': dd.strftime('%m'),
            'day'  : dd.strftime('%d'),
        }

        return sdict


    def checkFileMatch(self, obs_tmp, mod_tmp):
        """Choose only observation files matching with model date-timestep"""

        # create dictionaries with date+timestep as keys
        otmp = {basename(i)[:10]: i for i in obs_tmp}
        mtmp = {basename(j)[:10]: j for j in mod_tmp}

        # intersection between observational files and model files
        intr = sorted(list(set(otmp.keys()) & set(mtmp.keys())))

        return [otmp[i] for i in intr], [mtmp[j] for j in intr]


    def readObsFile(self, obs_file):
        """Read observation file"""

        obs = pd.read_table(obs_file,
                            delimiter=' ',
                            skiprows=1,
                            #skipfooter=4,
                            usecols=(0,1,2,3),
                            names=('datetime', 'lon', 'lat', self.obs_name),
                            warn_bad_lines=False,
                            error_bad_lines=False,
                           )

        if self.mylogger: self.mylogger.debug("PARTIAL OBS:\n%s" % (obs.head()))

        # extract the date+tstep
        obs_date = basename(obs_file)[:10]

        # extract valid values
        obs = obs.loc[np.where(obs['datetime'].values == int(obs_date))]

        return obs, obs_date


    def cleanObs(self, obs, obs_date):
        """Compare observation file with rejected obs file, return the
        observation dataframe cleaned from rejected observations"""

        # obs rejected
        obs_rej_tmp = []

        # steps
        rstep = {
                 '06' : -3,
                 '12' : -2,
                 '18' : -1,
                 '00' :  0, # next day, so must go to previous
                }
        ostep = obs_date[-2:]
        cstep = rstep[ostep] # current step

        if cstep == 0:
            # previous day
            odate = datetime.strptime(obs_date[:-2], self.date_fmt)-timedelta(days=1)
        else:
            # current day
            odate = datetime.strptime(obs_date[:-2], self.date_fmt)

        sdict = self.getDateDict(odate)

        # get file(s)
        for rpath, rtmpl in zip(self.rej_path, self.rej_tmpl):
            rej_tmp = glob("%s%s" % (rpath, rtmpl % sdict))

            # read day file and extract only the 'ostep' timestep
            for rej in rej_tmp:
                if self.mylogger: self.mylogger.debug("REJ FILE: %s" % (rej))
                tmp = pd.read_table(
                                    rej,
                                    sep='\s*',
                                    engine='python',
                                    usecols=(0,1,2,3),
                                    names=('datetime', 'lon', 'lat', self.obs_name),
                        )

                if self.mylogger: self.mylogger.debug("CSTEP: %s REJ VALS: %s" % (type(cstep), tmp['datetime'].dtype))
                # extract valid values
                tmp = tmp[tmp['datetime']==cstep]
                obs_rej_tmp.append(tmp)

        obs_rej = pd.concat(obs_rej_tmp, names=('datetime', 'lon', 'lat', self.obs_name))
        if self.mylogger: self.mylogger.debug("SHAPE: %s\tOBS TO BE REJECTED 1:\n%s" % (obs_rej.shape, obs_rej))

        # convert reject observation to the same format
        obs_rej['datetime'] = obs_rej['datetime'].replace(cstep, obs_date)
        obs_rej['lon'] = ((360.0/(129-1)) * (obs_rej['lon']-1-4)).round(2)
        obs_rej['lon'][obs_rej['lon']>180.] = (obs_rej['lon'] - 360).round(2)
        obs_rej['lat'] = (((180.0/(91-1)) * (91+4-obs_rej['lat']))-90).round(2)
        obs_rej[self.obs_name] = obs_rej[self.obs_name].round(2)

        if self.mylogger: self.mylogger.debug("SHAPE: %s\tOBS TO BE REJECTED 2:\n%s" % (obs_rej.shape, obs_rej))
        if self.mylogger: self.mylogger.debug("OBS SHAPE BEFORE:\n%s" % (obs.shape,))
        # remove from obs value present in obs_rej, rounded at the 2nd decimal
        obs = obs[~obs.round({'lon': 2, 'lat': 2}).isin(obs_rej)].dropna()
        if self.mylogger: self.mylogger.debug("OBS SHAPE AFTER:\n%s" % (obs.shape,))

        return obs


    def mergeObs(self, obs_tmp):
        """Merge multiple observation sources"""

        # build the file list
        if self.rej_path:
            rej = True
            persistent = True
        else:
            rej = False
            persistent = False

        ret_list = []

        for obs_list in obs_tmp:
            for obs_file in obs_list:
                if self.mylogger: self.mylogger.debug("OBS FILE: %s" % (obs_file))

                # read obs file
                obs, obs_date = self.readObsFile(obs_file)

                # check if empty and jump to next
                if obs.empty:
                    continue

                if rej:
                    obs = self.cleanObs(obs, obs_date)

                    if persistent:
                        # write new cleaned files
                        new_file = obs_file.replace('.txt', '_cleaned.txt')
                        with open(new_file, 'w') as f:
                            f.write(obs.to_string(index=False, header=False))
                            f.write('\n')

                # append data to tmp file
                tmp_file = self.tmp_tmpl % (obs_date)
                with open(tmp_file, 'a') as f:
                    f.write(obs.to_string(index=False, header=False))
                    f.write('\n')

                # if the tmpfile is not in the list add it
                if not ret_list.count(tmp_file):
                    ret_list.append(tmp_file)

        return sorted(ret_list)


    def buildObsFileList(self, sdict):
        """Create the list of observation files available for the same timesteps"""

        if self.obs_type == 'ASSIMILATION':

            # we need a list of observation paths and templates
            if type(self.obs_path) == str:
                self.obs_path = (self.obs_path,)
            if type(self.obs_tmpl) == str:
                self.obs_tmpl = (self.obs_tmpl,)

            # create a list of filelists coupled with rejected
            obs_tmp = []
            for opath, otmpl in zip(self.obs_path, self.obs_tmpl):
                obs_tmp.append(glob("%s%s" % (opath, otmpl % sdict)))

            return self.mergeObs(obs_tmp)

        if self.obs_type == 'POLLEN':

            dateparse = lambda x: pd.datetime.strptime(x, "%d-%m-%y").strftime("%Y%m%d%H")

            if self.mylogger: self.mylogger.debug("OBS_FILE: %s" % (self.obs_path + self.obs_tmpl))

            obs = pd.read_csv(self.obs_path+self.obs_tmpl,
                              sep=';',
                              skiprows=3,
                              usecols=(0,4),
                              names=('datetime', self.obs_name),
                              parse_dates=['datetime'],
                              date_parser=dateparse,
                              decimal=',',
                              warn_bad_lines=False,
                              error_bad_lines=False,
                             )

            obs['lon'] = "2.1"
            obs['lat'] = "41.4"
            obs = obs[['datetime', 'lon', 'lat', self.obs_name]]

            day_obs = obs.loc[obs['datetime'].values == sdict['date']+'00']

#            new_oname = "%s%s00_%s" % (self.obs_path, sdict['date'], self.obs_tmpl)
#            with open(new_oname, 'w') as f:
#                f.write(day_obs.to_string(index=False, header=False))
#                f.write('\n')

            # append data to tmp file
            tmp_file = self.tmp_tmpl % (sdict['date']+'00')
            with open(tmp_file, 'a') as f:
                f.write(day_obs.to_string(index=False, header=False))
                f.write('\n')

            return [tmp_file]


    def buildModFileList(self, sdict, obs_tmp):
        """Create the list of model files available for the same timesteps"""

        mod_tmp = glob("%s%s" % (self.mod_path, self.mod_tmpl % sdict))

        # call the checkFileMatch method
        if self.mylogger:
            self.mylogger.debug("BEFORE\n\tOBSTMP: %s\n\tMODTMP: %s" %\
                (obs_tmp, mod_tmp))
        obs_tmp, mod_tmp = self.checkFileMatch(obs_tmp, mod_tmp)
        if self.mylogger:
            self.mylogger.debug("AFTER\n\tOBSTMP: %s\n\tMODTMP: %s" %\
                (obs_tmp, mod_tmp))

        self.obs_list.extend(obs_tmp)
        self.mod_list.extend(mod_tmp)


    def createDateList(self):
        """Build the list of dates to search for"""

        str_date = datetime.strptime(self.str_date, self.date_fmt)
        end_date = datetime.strptime(self.end_date, self.date_fmt)

        return [d.to_datetime() for d in pd.date_range(str_date, end_date)]


    def selectRegion(self, lon, lat, mod):
        """Select a defined region"""

        if self.lon_bnds:
            lon_idx = np.where((lon >= self.lon_bnds[0]) & (lon <= self.lon_bnds[1]))
        else:
            lon_idx = (np.arange(lon.size),)

        if self.lat_bnds:
            lat_idx = np.where((lat >= self.lat_bnds[0]) & (lat <= self.lat_bnds[1]))
        else:
            lat_idx = (np.arange(lat.size),)

        if self.mylogger: self.mylogger.debug("LON_IDX: %s LAT_IDX: %s" % (lon_idx[0].size, lat_idx[0].size))

        # in case of observation lon and lat vector must have the same size
        if len(mod.shape) == 1:
            idx = np.intersect1d(lon_idx, lat_idx)
            return lon[idx], lat[idx], mod[idx]

        return lon[lon_idx], lat[lat_idx], mod.squeeze()[lat_idx[0],:][:,lon_idx[0]].T


    def genStats(self, data):
        """Generate statistics"""

        model = data[self.mod_name]
        obsrv = data[self.obs_name]

        bias = (model-obsrv).mean()
        rmse = np.sqrt(((model-obsrv)**2).mean())
        corr = model.corr(obsrv)
        frge = np.abs((model-obsrv)/(model+obsrv)).mean()*2
        snum = obsrv.size

        output_fmt = '{0:20}{1:12}{2:12}{3:12}{4:12}{5:12}'
        outputs = output_fmt.format('', 'BIAS', 'RMSE', 'CORR', 'FRGE', 'NSAMPLES') + '\n'
        outputs += output_fmt.format('# TOTAL', '%.5f' % bias, '%.5f' % rmse, '%.5f' % corr, '%.5f' % frge, '%.5f' % snum) + '\n'
        outfile = "%s/%s" % (self.dir_outp, self.fil_stat)
        with open(outfile, 'w') as f:
            f.write(outputs)


    def genPlots(self, data):
        """Generate plots"""

        model = data[self.mod_name]
        obsrv = data[self.obs_name]
        datet = data['datetime']

        outimag = "%s/%s" % (self.dir_outp, self.plt_imag)

        if self.plt_type == 'xy':
            plt.scatter(model, obsrv, edgecolor='none', s=50)
            plt.xlabel(self.mod_name)
            plt.ylabel(self.obs_name)
        elif self.plt_type in ('ts', 'tss'):
            fmt = '%Y%m%d%H'
            data['datetime'] = pd.to_datetime(datet, format=fmt)
            data = data.set_index(pd.DatetimeIndex(datet))
            #if self.mylogger: self.mylogger.debug("DATA:\n%s" % (data))
            if self.plt_type == 'tss':
                data.plot(style='.', ms=20)
            else:
                data.plot()

        if self.plt_xlim:
            plt.xlim(self.plt_xlim)
        if self.plt_ylim:
            plt.ylim(self.plt_ylim)

        plt.title(self.plt_titl)
        plt.savefig(outimag)
        plt.clf()


    def cleanTmp(self):
        """Clean temporary files"""

        for f in glob(self.tmp_tmpl % '*'):
            os.remove(f)


    def runEval(self):
        """Main method to run the evaluation"""

        # remove tmp filelist
        self.cleanTmp()

        # create the datelist and build filelists
        for dd in self.createDateList():
            sdict = self.getDateDict(dd)
            obs_tmp = self.buildObsFileList(sdict)
            self.buildModFileList(sdict, obs_tmp)

        if self.mylogger: self.mylogger.debug("OBS FILES: %s MOD FILES: %s" % (len(self.obs_list), len(self.mod_list)))

        # append data
        frame_list = []

        for obs_file, mod_file in zip(self.obs_list, self.mod_list):

            if self.mylogger: self.mylogger.debug("\n\tOBS FILE: %s\n\tMOD FILE: %s" % (obs_file, mod_file))

            # read observation file
            obs = pd.read_table(obs_file,
                                delimiter='\s*',
                                engine='python',
                                names=('datetime', 'lon', 'lat', self.obs_name))

            if self.mylogger: self.mylogger.debug("ORIG OBS SIZE: %s" % obs[self.obs_name].size)

            # read netcdf file
            f = nc(mod_file)

            flon = f.variables[self.mod_vlon][:]
            flat = f.variables[self.mod_vlat][:]
            # TODO: missing values handling
            fmod = f.variables[self.variable][:]

            # select region for model
            nlon, nlat, nmod = self.selectRegion(flon, flat, fmod)
            if self.mylogger: self.mylogger.debug("NLON: %s NLAT: %s NMOD: %s" % (nlon.shape, nlat.shape, nmod.shape))

            # select region for obs
            xobs, yobs, nobs = self.selectRegion(obs['lon'].values, obs['lat'].values, obs[self.obs_name].values)
            if self.mylogger: self.mylogger.debug("XOBS: %s YOBS: %s NOBS: %s" % (xobs.shape, yobs.shape, nobs.shape))

            # interpolate netcdf values to observation coords
            interp_func = RectBivariateSpline(nlon, nlat, nmod)
            interp_mod = interp_func(xobs, yobs, grid=False)
            if self.mylogger: self.mylogger.debug("INTERP_MOD: %s" % interp_mod.shape)

            f.close()

            # create dataframe with a column for observations and another one
            # with interpolated model values
            d = {
                    'datetime'    : pd.Series(obs['datetime']),
                    self.obs_name : pd.Series(nobs),
                    self.mod_name : pd.Series(interp_mod),
                }

            # append to the dataframe list
            frame_list.append(pd.DataFrame(d))

        if frame_list:
            if self.mylogger: self.mylogger.debug("FRAME LIST LEN: %s" % len(frame_list))
            # concatenate all dataframes into one
            data = pd.concat(frame_list)
            if self.mylogger: self.mylogger.debug("DATA:\n%s" % data)

            # generate statistics
            self.genStats(data) #model, obsrv)

            # generate plots
            self.genPlots(data) #model, obsrv)

        else:
            if self.mylogger: self.mylogger.debug("Empty file list. Exit.")

        # remove tmp filelist
        self.cleanTmp()


def testDA():
    #/scratch/Earth/editomas/observations/modis_nrl_oceanland_aquaterra_AE_AI_count_selected/200705/2007051106_oceanland_aquaterra_obsnew.txt
    #/scratch/Earth/editomas/observations/modis_nrl_oceanland_aquaterra_AE_AI_count_selected/200705/2007051112_oceanland_aquaterra_obsnew.txt
    #/scratch/Earth/editomas/observations/modis_nrl_oceanland_aquaterra_AE_AI_count_selected/200705/2007051118_oceanland_aquaterra_obsnew.txt
    #/scratch/Earth/editomas/observations/modis_nrl_oceanland_aquaterra_AE_AI_count_selected/200705/2007051200_oceanland_aquaterra_obsnew.txt
    #/scratch/Earth/editomas/observations/modis_DB_land_aqua_AE_AI_Count_selected/200705/2007051112_deepblue_aqua_obsnew.txt
    #/scratch/Earth/editomas/data/nmmb-bsc-ctm-v2.0_DA-2007-NRLDB-bincorr1-uss-1aer/ENS/departures/2007051106-2007051200/obs_dep_rejected.txt

    STR_DATE = "20070611"
    END_DATE = "20070612"

    NUM = "84"

    OBS_PATH = ("/scratch/Earth/editomas/observations/modis_nrl_oceanland_aquaterra_AE_AI_count_selected/",
                "/scratch/Earth/editomas/observations/modis_DB_land_aqua_AE_AI_Count_selected/",)
    OBS_TMPL = ("%(year)s%(month)s/%(date)s*_oceanland_aquaterra_obsnew.txt",
                "%(year)s%(month)s/%(date)s*_deepblue_aqua_obsnew.txt", )

    REJ_PATH = None #("/scratch/Earth/editomas/data/nmmb-bsc-ctm-v2.0_DA-2007-NRLDB-bincorr1-uss-1aer/ENS/departures/",)
    REJ_TMPL = None #("%(date)s*/obs_dep_rejected.txt",)

    #MOD_PATH = "/scratch/Earth/editomas/data/nmmb-bsc-ctm-v2.0_FC%s_CONTROL-2007-LR-5dd-IC-AN/ENS/nc_analysis_validation/" % NUM
    MOD_PATH = "/scratch/Earth/editomas/data/nmmb-bsc-ctm-v2.0_FG-2007-NRLDB-bincorr1-uss-1aer/ENS/nc_analysis_validation/"
    #FIX_TMPL = "_FC%(num)s_FC%(num)s_CONTROL-2007-LR-5dd-IC-AN.nc" % { 'num' : NUM }
    FIX_TMPL = "_FG-2007-NRLDB-bincorr1-uss-1aer.nc"
    MOD_TMPL = "%(date)s*" + FIX_TMPL

    DIR_OUTP = "./OUT/"

    DEBUG = True

    # create Class
    ev = Evaluator(STR_DATE, END_DATE, OBS_PATH, MOD_PATH, OBS_TMPL, MOD_TMPL, DIR_OUTP, REJ_PATH, REJ_TMPL, DEBUG)

    # setting attributes
    ev.plt_xlim = (0, 4)
    ev.plt_ylim = (0, 4)
    #ev.lon_bnds = (-25, 60)
    #ev.lat_bnds = (0, 65)
    #ev.mod_name = ""
    #ev.obs_name = ""
    ev.plt_titl = "Glob FG 2007 (REJ)" #% NUM
    ev.plt_imag = "glob_fg2007_image_rej.png" #% NUM
    ev.fil_stat = "glob_fg2007_stats_rej.txt" #% NUM

    # run
    ev.runEval()


def testPollen():

    STR_DATE = "20130328"
    END_DATE = "20130331"

    OBS_PATH = "/home/Earth/fbeninca/Programs/ACtools/evaluation/tests/polen/"
    OBS_TMPL = "Pollen_barcelona_2013-14_Pinus_Platanus_massa.csv"

    MOD_PATH = "/home/Earth/fbeninca/Programs/ACtools/evaluation/tests/polen/"
    MOD_TMPL = "%(date)s00/%(date)s00_NMMB-BSC-CTM_regular.nc"

    DIR_OUTP = "./OUT/"

    DEBUG = True

    # create Class
    ev = Evaluator(STR_DATE, END_DATE, OBS_PATH, MOD_PATH, OBS_TMPL, MOD_TMPL, DIR_OUTP, en_debug=DEBUG)

    # setting attributes
    ev.obs_type = 'POLLEN'
    ev.variable = 'bc_platanus'     # variable name
    ev.mod_name = 'Model'           # model label
    ev.obs_name = 'Observation'     # observation label
    ev.plt_type = 'xy'
    ev.lon_bnds = (1, 3)
    ev.lat_bnds = (40, 42)
    ev.plt_xlim = (-0.0000005, 0.000003)
    ev.plt_ylim = (0, 0.000009)
    ev.plt_titl = u"Pollen March 2013 (g/m$^3$)" #% NUM
    ev.plt_imag = "pollen_201303_scatter.png" #% NUM
    ev.fil_stat = "pollen_201303.txt" #% NUM

    # run
    ev.runEval()


if __name__ == "__main__":
    # TODO: parameters handling
    import sys

    nargs = len(sys.argv)
    if nargs != 2:
        print("Error: maximum of 2 args")
        sys.exit(1)

    def exec_all():
        #print "EXEC_ALL"
        try:
            testDA()
        except Exception as e:
            print("Error (DA):", e)
        try:
            testPollen()
        except Exception as e:
            print("Error (Pollen):", e)

    if nargs == 1:
        exec_all()
    else:
        attr = sys.argv[1]
        print("ATTR:", attr)
        current_module = sys.modules[__name__]
#        print attr, current_module.__name__
#        for i in dir(current_module):
#            print i
        hasattr(current_module, attr) and getattr(current_module, attr)() #or exec_all()


