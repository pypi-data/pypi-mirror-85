##!/usr/bin/env python
## -*- coding: utf-8 -*-
##
## author: Francesco Benincasa <francesco.benincasa@bsc.es>
#
#
# import matplotlib
# matplotlib.use('Agg')
#
# import matplotlib.pyplot as plt
# from pylab import plot
# from pylab import show
# import numpy as np
# from xml.dom.minidom import parseString
# from datetime import datetime
# from datetime import date
# from datetime import timedelta
# from calendar import monthrange
# import os.path
#
# from random import randrange
#
# global FIGURE
#
# def do_avg(l, k):
#    #print "LIST", l
#    #print "K", k
#
#    #search prev
#    prev = 0
#    for i in range(k-1,-1,-1):
#        if l.has_key(i):
#            #print "IP", i, "L[i]", l[i]
#            if l[i] > 0:
#                prev = float(l[i])
#                break
#
#    #search next
#    next = 0
#    for i in range(k+1, k+3):
#        if l.has_key(i):
#            if l[i] > 0:
#                #print "NEXT", l[i]
#                next = float(l[i])
#                break
#
#    #do avg
#    avg = (prev + next)/2
#
#    #do avg prev
#    avg_p = (avg + prev)/2
#
#    #do avg next
#    avg_n = (avg + next)/2
#
#    #print "PREV", avg_p
#    #print "NEXT", avg_n
#
#    if avg_p == 0: avg_p = NULLVAL
#    if avg_n == 0: avg_p = NULLVAL
#
#    return avg_p, avg_n
#
#
# class DataXMLParser:
#    """ """

#    def __init__(self):
#        """ """
#        pass

#    def getCountryCode(self, dom):
#        """ """
#        xmlTags = dom.getElementsByTagName('country_isocode')
#        elem = xmlTags[0]
#        return elem.firstChild.data

#    def getStation(self, dom, code):
#        """ """
#        station_name = ''
#        xmlTags = dom.getElementsByTagName('station')

#        for elem in xmlTags:
#            for child in elem.childNodes:
# #                if child.tagName == 'name':
# #                    station_name = child.firstChild.data
#                if child.tagName == 'code' \
#                        and child.firstChild.data != code:
#                    return None
#                return elem

#    def getComponent(self, elem, name):
#        """ """
#        meas = elem.getElementsByTagName('measurement')
#        result = {}
#        dtime = ''
#        val = ''

#        for items in meas:
#            flag = False
#            for child in items.childNodes:
#                if child.tagName == 'component' \
#                        and child.firstChild.data == name:
#                    flag = True
#                if flag:
#                    if child.tagName == 'datetime_to':
#                        dtime = child.firstChild.data
#                    if child.tagName == 'value':
#                        val = child.firstChild.data
#                    if dtime and val:
#                        result[dtime] = val

#        return result

#    def retrieveXMLData(self, filename, code):
#        f = open(filename)
#        data = f.read()
#        f.close()

#        dom = parseString(data)

#        datap = DataXMLParser()
#        elem = datap.getStation(dom, code)
#        pm10 = datap.getComponent(elem, 'PM10')
#        pm2_5 = datap.getComponent(elem, 'PM2_5')
#        cc = datap.getCountryCode(dom)

#        #st_name = "%s, %s" % (st_name, cc)

#        return pm10, pm2_5


# class TextParser2:
#    """ """

#    def __init__(self):
#        """ """
#        pass

#    def retrieveTXTData(self, filename, code, model=None, start_hour=0):
#        """ """

#        nomodels = ("AERONET", "AE1", "AE2", "VISIBILITY", "HAZE")

#        f = open(filename)
#        data = f.read()
#        f.close()

#        d1 = {}
#        lines = data.split('\n')

#        for line in lines:

#            if not line:
#                continue

#            #data = line.split('\t')
#            #model station date hour value
#            data = line.split()

#            mod = data[0]
#            if model != mod:
#                continue

#            cod = data[1]
#            if code != cod:
#                continue

#            fndat = os.path.basename(filename).split('.')[0]
#            if data[2] < fndat:
#                continue

#            dat = datetime.strptime(data[2], "%Y%m%d").strftime("%Y-%m-%d")
#            hour = int(float(data[3]))

#            # AERONET, AE1, AE2
#            mdate = "%s %02d:00" % (dat, hour)
#            if model in nomodels:
#                if d1.has_key(mdate):
#                    val = d1[mdate]
#                    if type(val) is float:
#                        d1[mdate] = [val]
#                    d1[mdate].append(float(data[4]))
#                else:
#                    d1[mdate] = float(data[4])
#                continue

#            hour = start_hour + hour
#            if hour < START_H and model not in nomodels:
#                continue

#            edelta = timedelta(days=1)
#            edat = (datetime.strptime(data[2], "%Y%m%d") + edelta).strftime("%Y-%m-%d")
#            if hour > 36:
#                continue
#            if hour >= NHOURS:
#                delta = timedelta(days=hour/NHOURS)
#                dat = (datetime.strptime(data[2], "%Y%m%d") + delta).strftime("%Y-%m-%d")
#                hour = hour % NHOURS

#            mdate = "%s %02d:00" % (dat, hour)
#            d1[mdate] = float(data[4])

#        #print "D1", d1
#        return d1


# class TextParser:
#    """ """

#    def __init__(self):
#        """ """
#        pass

#    def retrieveTXTData(self, filename, code):
#        """ """
#        f = open(filename)
#        data = f.read()
#        f.close()

#        d1 = {}
#        d2 = {}
#        lines = data.split('\n')

#        for line in lines:

#            if not line:
#                continue

#            #data = line.split('\t')
#            data = line.split()
#            cod = data[0]

#            if code != cod:
#                continue

#            dat = datetime.strptime(data[1], "%Y%m%d").strftime("%Y-%m-%d")
#            mdate = "%s %02d:00" % (dat, int(data[2]))
#            pm10 = data[3]
#            pm2_5 = data[4]

#            d1[mdate] = pm10
#            d2[mdate] = pm2_5

#        return d1, d2


# class PlotGenerator:

#    def __init__(self):
#        """ """
#        plt.clf()
#        plt.cla()

#    def setVar(self, xvals, var, mon, force_continue=False):
#        """ """
#        hrs = var.keys()
#        hrs.sort()
#        steps = {}
#        for dat in hrs:
#            #print dat, var[dat]
#            dt = datetime.strptime(dat, "%Y-%m-%d %H:%M")
#            day = dt.day
#            hour = dt.hour
#            if mon == dt.strftime("%Y%m"):
#                st = (day*NH)+(hour/INTERV)
#            else:
#                st = ((MR+day)*NH)+(hour/INTERV)
#            #print "DAT", dat, "ST", st, "V", var[dat]
#            steps[st] = var[dat]

#        res = []
#        xvtmp = []

#        for k in range(NH,(MR+1)*NH+4): #xvals:
#            val = NULLVAL
#            if k in steps.keys():
#                val = steps[k]
#                if type(val) is list:
#                    for v in val:
#                        if float(v) < 0:
#                            val[val.index(v)] = NULLVAL
#                else:
#                    if float(val) < 0:
#                        val = NULLVAL

#            if type(val) is list:
#                xvtmp.extend([k for i in range(0, len(val))])
#                res.extend(val)
#            else:
#                xvtmp.append(k)
#                res.append(val)

#        res = np.array(res)

#        return xvtmp, res+.005 #_masked


#    def generatePlot(self, varN, title, fname, month, MR):
#        """ """

#        f = plt.gcf()
#        DefaultSize = f.get_size_inches()

#        XTICKS_END = (MR+1)*NH + 4

# #        XTICKS_LABELS = np.arange(1,(MR+1))
#        XTICKS_LABEL_START = XOFF / XTICKS_INT
#        XTICKS_LABEL_END = XTICKS_END / XTICKS_INT + 1

#        XTICKS_DATE_START = month + "01"
#        XTICKS_DATE_START_FORMAT = "%Y%m%d"
#        XTICKS_DATE_NUM = (XTICKS_END - XTICKS_START) / NH
#        XTICKS_DATE_INT = 1

#        dates = [datetime.strptime(XTICKS_DATE_START, XTICKS_DATE_START_FORMAT) + timedelta(days=i) for i in range(XTICKS_DATE_NUM)]

#        XTL = [datetime.strftime(d, "%d") for d in dates]
#        XTICKS_LABELS = [(int(d) % 2) and d or '' for d in XTL]
#        XTICKS_LABELS.append('01')

#        for attrs in varN:
#            x = attrs['xvals']
#            y = attrs['var']
#            sym = attrs['symbol']
#            try:
#                plt.plot(
#                    x,
#                    y,
#                    sym,
#                    color=attrs['color'],
#                    label=attrs['label'],
#                    linewidth=attrs['linewidth'],
#                    markersize=attrs['markersize'],
#                    markerfacecolor=attrs['mec'],
#                )
#            except Exception, e:
#                print "ERROR", e
#                continue

#        ax = plt.axis([XMIN,XTICKS_END,YMIN,YMAX])

#        ll = plt.legend(
#            loc=LEGEND,
#            fancybox=True,
#            shadow=True,
#            ncol=2,
#            prop={'size':11},
#            )
#        lx = plt.xlabel(XLABEL % {'month': MONTH, 'year': YEAR})
#        tx = plt.xticks(np.arange(XTICKS_START, XTICKS_END, XTICKS_INT),
#            XTICKS_LABELS)

#        ty = plt.yticks(YTICKS, YTICKS_LABELS)

#        if EVAL_TYPE == 'VISIBILITY':
#            ly = plt.ylabel(YLABEL2)
#            plt.yscale('log')
#        else:
#            ly = plt.ylabel(YLABEL1)

#        tl = plt.title(title)
#        gr = plt.grid(GRID)

#        f.set_size_inches((DefaultSize[0]*1.5, DefaultSize[1]*1.5))
#        f.savefig(fname, dpi=72)
#        #if fname.find(FIGURE) >= 0:
#        if fname.find("Zinder") >= 0:
#            f.savefig("latest.png", bbox_inches='tight', pad_inches=.2, dpi=42)
#        plt.close('all')


# EVAL1_STATIONS = {
#    "Barcelona": u"Barcelona (Spain)",
#    "Capo_Verde": u"Capo_Verde (Cabo Verde)",
#    "Dakar": u"Dakar (Senegal)",
#    "Bambey-ISRA": u"Bambey (Senegal)",
#    "IER_Cinzana": u"IER_Cinzana (Mali)",
#    "Agoufou": u"Agoufou ",
#    "Banizoumbou": u"Banizoumbou (Niger)",
#    "Zinder_Airport": u"Zinder_Airport (Niger)",
#    "Santa_Cruz_Tenerife": u"Santa_Cruz_Tenerife (Spain)",
#    "Zouerate-Fennec": u"Zouerate-Fennec (Mauritania)",
#    "Tamanrasset_INM": u"Tamanrasset_INM (Algery)",
#    "Saada": u"Saada (Morocco)",
#    "Oujda": u"Oujda (Morocco)",
#    "Cairo_EMA_2": u"Cairo_EMA (Egypt)",
#    "Eilat": u"Eilat (Israel)",
#    "SEDE_BOKER": u"SEDE_BOKER (Israel)",
#    "Solar_Village": u"Solar_Village (Saudi Arabia)",
#    "IMS-METU-ERDEMLI": u"IMS-METU-ERDEMLI (Turkey)",
#    "IASBS": u"IASBS (Iran)",
#    "FORTH_CRETE": u"FORTH_CRETE (Greece)",
#    "Xanthi": u"Xanthi (Greece)",
#    "Lecce_University": u"Lecce_University (Italy)",
#    "Lampedusa": u"Lampedusa (Italy)",
#    "IMAA_Potenza": u"IMAA_Potenza (Italy)",
#    "Rome_Tor_Vergata": u"Rome_Tor_Vergata (Italy)",
#    "ETNA": u"ETNA (Italy)",
#    "Ersa": u"Ersa (France)",
#    "Villefranche": u"Villefranche (France)",
#    "Avignon": u"Avignon (France)",
#    "Porquerolles": u"Porquerolles (France)",
#    "Seysses": u"Seysses (France)",
#    "Cabo_da_Roca": u"Cabo_da_Roca (Portugal)",
#    "Evora": u"Evora (Portugal)",
#    "Caceres": u"Cáceres (Spain)",
#    "Granada": u"Granada (Spain)",
#    "Tabernas_PSA-DLR": u"Tabernas_PSA-DLR (Spain)",
#    "Palma_de_Mallorca": u"Palma_de_Mallorca (Spain)",
#    "Ouarzazate": u"Ouarzazate (Morocco)",
#    "Ilorin": u"Ilorin (Nigeria)",
#    "KAUST_Campus": u"KAUST_Campus (Saudi Arabia)",
#    "CUT-TEPAK": u"CUT-TEPAK (Cyprus)",
#    "Kuwait_University": u"Kuwait_University (Kuwait)",
# }

# #name : (var name, start hour, color, type, , )

# EVAL1_MODELS = {
# r'01-AE AERONET $>$ 0.6': ('AE1', 0, 'w', 'o', False, 1.0, 6, None),
# r'02-AE AERONET $\leq$ 0.6': ('AE2', 0, 'k', 'o', False, 1.0, 6, 'gray'),
# r'03-AOD$_{550}$ AERONET': ('AERONET', 0, 'y', '^', False, 1.8, 8, None),
# #r'04-DOD$_{550}$ NMMB/BSC-Dust': ('NMMB-BSC_OPER', 12, 'r', '-', True, 1.8, 8, None),
# r'05-DOD$_{550}$ NMMB/BSC-Dust': ('SDSWAS_NMMB-BSC-v2_OPER', 12, 'r', '-', True, 2.5, 8, None),
# #r'04-DOD$_{550}$ BSC_DREAM8b': ('BSC_DREAM8b', 12, 'r', '-', True, 1.8, 8, None),
# #r'05-DOD$_{550}$ MACC-ECMWF': ('MACC-ECMWF', 0, 'b', '-', True, 1.8, 8, None),
# #r'06-DOD$_{550}$ DREAM8-NMME-MACC': ('DREAM8-MACC', 12, 'm', '-', True, 1.8, 8, None),
# #r'07-DOD$_{550}$ CHIMERE': ('CHIMERE', 0, 'c', '-', True, 1.8, 8, None),
# #r'08-DOD$_{550}$ NMMB/BSC-Dust': ('NMMB-BSC', 12, 'g', '-', True, 1.8, 8, None),
# #r'09-DOD$_{550}$ U.K. MetOffice MetUM': ('_UKMET.', 0, 'DarkOrange', '-', True, 1.8, 8, None),
# #r'10-DOD$_{550}$ NASA GEOS-5': ('NASA-GE', 0, 'Brown', '-', True, 1.8, 8, None),
# #r'11-DOD$_{550}$ NCEP NGAC': ('NCEP-NG', 0, 'Chartreuse', '-', True, 1.8, 8, None),
# #r'12-DOD$_{550}$ MEDIAN': ('_MEDIAN', 0, 'k', '--', True, 2.5, 8, None),
# }

# EVAL2_STATIONS = {
# "DAUI": u"IN SALAH NORTH (Algeria)",
# "DAUZ": u"IN AMENAS/ZARZAI (Algeria)",
# "DATM": u"BORDJ MOKHTAR (Algeria)",
# "GQNN": u"NOUAKCHOTT (Mauritania)",
# "GQPP": u"NOUADHIBOU (Mauritania)",
# "LCRA": u"AKROTIRI (Cyprus)",
# "GGOV": u"BISSAU (Guinea-Bissau)",
# "HLLT": u"TRIPOLI INTL ARP (Libya)",
# "HLLB": u"BENINA/BENGHAZI (Libya)",
# "GMML": u"LAAYOUNE/HASSAN (Morocco)",
# "GMFK": u"ER-RACHIDIA (Morocco)",
# "DTTR": u"EL BORMA (Tunisia)",
# "GOTT": u"TAMBACOUNDA (Senegal)",
# "GOGS": u"CAPE SKIRING (Senegal)",
# "LTCJ": u"BATMAN (Turkey)",
# "OJAM": u"AMMAN/KING ABDUL (Jordan)",
# "HDAM": u"AMBOULI (Djibouti)",
# "HECA": u"CAIRO INTL AIRPORT (Egypt)",
# "HESH": u"ST CATHERINE (Egypt)",
# "OOMS": u"SEEB INTL (Oman)",
# "DNKN": u"KANO/MALLAM (Nigeria)",
# "OIKQ": u"GHESHM/DAYRESTAN (Iran)",
# "OIAW": u"AHWAZ (Iran)",
# "OIBB": u"BUSHEHR (Iran)",
# "FTTJ": u"NDJAMENA (Chad)",
# "OERF": u"RAFHA (Saudi Arabia)",
# "OERK": u"RIYADH (Saudi Arabia)",
# "OEAH": u"AL AHSA (Saudi Arabia)",
# "OEGS": u"GASSIM (Saudi Arabia)",
# "OENG": u"NEJRAN (Saudi Arabia)",
# "KQTZ": u"BAGHDAD (Irak)",
# "OMFJ": u"FUJAIRAH (U. Arab Emirates)",
# "OYHD": u"HODEIDAH (Yemen)",
# "OTBD": u"DOHA INTL AIRPOR (Qatar)",
# "OKBK": u"KUWAIT INTL (Kuwait)",
# "OBBI": u"BAHRAIN INTL ARP (Bahrain)",
# "GABS": u"BAMAKO/SENOU (Mali)",
# "DRRN": u"NIAMEY (Niger)",
# "DRZA": u"AGADEZ SOUTH (Niger)",
# }

# EVAL2_MODELS = {
# r'13-SCONC ($\mu$g/m$^3$) SAND/DUST': ('VISIBILITY', 0, 'r', '^', False, 1.8, 10, None),
# r'14-SCONC ($\mu$g/m$^3$) HAZE': ('HAZE', 0, 'r', '*', False, 1.8, 10, None),
# r'04-SCONC ($\mu$g/m$^3$) BSC_DREAM8b': ('BSC_DREAM8b', 12, 'r', '-', True, 1.8, 8, None),
# r'05-SCONC ($\mu$g/m$^3$) MACC-ECMWF': ('MACC-ECMWF', 0, 'b', '-', True, 1.8, 8, None),
# r'06-SCONC ($\mu$g/m$^3$) DREAM8-NMME-MACC': ('DREAM8-MACC', 12, 'm', '-', True, 1.8, 8, None),
# r'07-SCONC ($\mu$g/m$^3$) CHIMERE': ('CHIMERE', 0, 'c', '-', True, 1.8, 8, None),
# r'08-SCONC ($\mu$g/m$^3$) NMMB/BSC-Dust': ('NMMB-BSC', 12, 'g', '-', True, 1.8, 8, None),
# r'09-SCONC ($\mu$g/m$^3$) U.K. MetOffice MetUM': ('_UKMET.', 0, 'DarkOrange', '-', True, 1.8, 8, None),
# r'10-SCONC ($\mu$g/m$^3$) NASA GEOS-5': ('NASA-GE', 0, 'Brown', '-', True, 1.8, 8, None),
# r'11-SCONC ($\mu$g/m$^3$) NCEP NGAC': ('NCEP-NG', 0, 'Chartreuse', '-', True, 1.8, 8, None),
# r'12-SCONC ($\mu$g/m$^3$) MEDIAN': ('_MEDIAN', 0, 'k', '--', True, 2.5, 8, None),
# }

# EVAL_TYPE = ''

# NULLVAL = np.nan #None

# MONTH = YEAR = ""

# XLABEL = r"days" #r"%(month)s %(year)s"
# YLABEL1 = r"Aerosol Optical Depth (AOD$_{550}$), Dust Optical Depth (DOD$_{550}$)"
# YLABEL2 = r"Dust Surface Concentration - SCONC ($\mu$g/m$^3$)"

# LEGEND = 'upper center' #'upper right'
# GRID = False

# NUMDAYS = 31
# DAYSTART = 1

# NHOURS = 24
# INTERV = 3
# NH = NHOURS/INTERV #8

# XOFF = NH * DAYSTART
# XMAX = NH * NUMDAYS + XOFF #768 - NH*32
# XMIN = 0 + XOFF

# YOFF = 0
# YMAX = 2.0 + YOFF #00
# YMIN = 0 + YOFF

# XTICKS_START = XMIN
# XTICKS_END = XMAX
# XTICKS_INT = NH
# XTICKS_LABEL_START = XOFF / XTICKS_INT
# XTICKS_LABEL_END = XMAX / XTICKS_INT + 1
# XTICKS_LABEL_INT = 1

# XTICKS_DATE_START = "20110501"
# XTICKS_DATE_START_FORMAT = "%Y%m%d"
# XTICKS_DATE_NUM = (XTICKS_END - XTICKS_START) / NH
# XTICKS_DATE_INT = 1

# dates = [datetime.strptime(XTICKS_DATE_START,
#    XTICKS_DATE_START_FORMAT) + timedelta(days=i) for i in range(XTICKS_DATE_NUM)]

# XTL = [datetime.strftime(d, "%d") for d in dates]
# XTICKS_LABELS = [(int(d) % 2) and d or '' for d in XTL]

# YTICKS_START = YMIN + 0.2
# YTICKS_END = YMAX + 0.1
# YTICKS_INT = 0.2 #25
# YTICKS_LABEL_START = YTICKS_START
# YTICKS_LABEL_END = YTICKS_END
# YTICKS_LABEL_INT = YTICKS_INT

# YTICKS = () #np.arange(YTICKS_START, YTICKS_END, YTICKS_INT)
# YTICKS_LABELS = () #np.arange(YTICKS_LABEL_START, YTICKS_LABEL_END, YTICKS_LABEL_INT)

# START_H = 15


# if __name__ == "__main__":

#    import glob
#    import sys

#    msg_usage = """
# Error: %s
# Usage: %s <path> <date>
# - <path>: where find files to parse (absolute path)
# - <date>: a date without day in format %%Y%%m
# - [AERONET|VISIBILITY]: evaluation type
# """

#    if len(sys.argv) != 4:
#        print msg_usage % ("Bad number argument", sys.argv[0])
#        sys.exit(1)

#    path = sys.argv[1]
#    month = sys.argv[2]
#    eval_type = sys.argv[3]
#    if eval_type not in ('AERONET', 'VISIBILITY'):
#        print msg_usage % ("Wrong evaluation type: " + eval_type, sys.argv[0])
#        sys.exit(1)

#    EVAL_TYPE = eval_type

#    try:
#        dt = datetime.strptime(month, "%Y%m")
#    except Exception, e:
#        print msg_usage % (str(e), sys.argv[0])
#        sys.exit(1)

#    MONTH = dt.strftime("%B")
#    YEAR = dt.strftime("%Y")

#    filenames = glob.glob(path + month + '*obs')

#    MR = monthrange(dt.year, dt.month)[1]
#    num = (MR+1)*NH #days in one month x hours in a day
#    xvals = np.arange(XTICKS_START, num)
#    p = PlotGenerator()
#    tp = TextParser2()

#    if EVAL_TYPE == 'AERONET':
#        STATIONS = EVAL1_STATIONS
#        MODELS = EVAL1_MODELS
#        YTICKS = np.arange(YTICKS_START, YTICKS_END, YTICKS_INT)
#        YTICKS_LABELS = np.arange(YTICKS_LABEL_START, YTICKS_LABEL_END, YTICKS_LABEL_INT)
#    else:
#        STATIONS = EVAL2_STATIONS
#        MODELS = EVAL2_MODELS
#        YTICKS = (0, 5, 20, 50, 200, 500, 2000, 5000, 20000, 100000)
#        YTICKS_LABELS = ('0', '5', '20', '50', '2000', '5000', '20000', '100000')

#    #print STATIONS, MODELS
#    #print YTICKS, YTICKS_LABELS

#    FIGURE = STATIONS.keys()[randrange(len(STATIONS.keys()))]

#    for code in STATIONS.keys():
#        print "STAT", code
#        aod = {}
#        for filename in filenames:
#            if not os.path.isfile(filename):
#                continue
#            for model in MODELS:
#                (modname, start, color, symbol, force_continue, lw, msize, mec) = MODELS[model]
#                if not aod.has_key(model):
#                    aod[model] = {}
#                res = tp.retrieveTXTData(filename, code, modname, start)
#                aod[model].update(res)

#        st_name = STATIONS[code]
#        varz = []
#        mods = aod.keys()
#        mods.sort()
#        for mod in mods:
#            color = MODELS[mod][2]
#            symbol = MODELS[mod][3]
#            force_continue = MODELS[mod][4]
#            lw = MODELS[mod][5]
#            msize = MODELS[mod][6]
#            mec = MODELS[mod][7]
#            label = '-'.join(mod.split('-')[1:])
#            xvtmp, var = p.setVar(xvals, aod[mod], month, force_continue)
#            if EVAL_TYPE == 'VISIBILITY':
#                if MODELS[mod][0] not in ('VISIBILITY', 'HAZE'):
#                    var = var*(10**9)
#            #print mod, xvtmp, var
#            item = {
#                'xvals': xvtmp,
#                'var': var,
#                'color': color,
#                'symbol': symbol,
#                'label': label,
#                'linewidth': lw,
#                'markersize': msize,
#                'mec': mec,
#            }
#            varz.append(item)

#        title = unicode( "%s - %s %s\n" % (st_name, MONTH, YEAR)) #, date.strftime(dt, "%B %Y")))
#        figname = "%s-%s.png" % (month, code)

#        p.generatePlot(
#                varz,
#                title,
#                figname,
#                month,
#                MR,
#           )


# ### AIR QUALITY

# import matplotlib
# matplotlib.use('Agg')

# import matplotlib.pyplot as plt
# import numpy as np
# from xml.dom.minidom import parseString
# from datetime import datetime
# from datetime import date
# from calendar import monthrange
# import os.path


# STATIONS = {
#    "CY0002R": u"Cyprus: Ayia Marina",
#    "HU0002R": u"Hungary: k-Puszta",
#    "SI0033A": u"Slovenia: Murska Sobota",
#    "IT1478A": u"Italy: Claut-Localita Porto Pinedo",
#    "IT2099A": u"Italy: Monte Martano",
#    "IT0009R": u"Italy: Monte Cimone",
#    "ITXXXXA": u"Italy: Roma Tiburtina",
#    "CH0002R": u"Switzerland: Payerne",
#    "CH0033A": u"Switzerland: Magadino-Cadenazzo",
#    "ES0009R": u"Spain: Campisábalos",
#    "ES0012R": u"Spain: Zarra",
#    "ES0013R": u"Spain: Peñausende",
#    "ES0016R": u"Spain: O Saviñao",
#    "ES1348A": u"Spain (Generalitat de Cat.): Bellver de Cerdanya",
#    "ES1864A": u"Spain (Gob. Canarias): Costa-Teguise",
#    "ES1760A": u"Spain (Gob. Canarias): Granadilla",
#    "MT0001G": u"Malta (Gozo): Gharb",
#    "EG0001G": u"Egypt: Cairo",
#    "FR23124": u"La Tardière: France",
#    "FR35006": u"Tulle - Hugo: France",
#    "FR02005": u"Martigues l'Ile: France",
# }

# LABEL1 = ''
# LABEL2 = ''

# XLABEL = ''
# YLABEL = ''

# M = 50
# OFFS = 10


# class DataXMLParser:
#    """ """

#    def __init__(self):
#        """ """
#        pass

#    def getCountryCode(self, dom):
#        """ """
#        xmlTags = dom.getElementsByTagName('country_isocode')
#        elem = xmlTags[0]
#        return elem.firstChild.data

#    def getStation(self, dom, code):
#        """ """
#        station_name = ''
#        xmlTags = dom.getElementsByTagName('station')

#        for elem in xmlTags:
#            for child in elem.childNodes:
# #                if child.tagName == 'name':
# #                    station_name = child.firstChild.data
#                if child.tagName == 'code' \
#                        and child.firstChild.data != code:
#                    return None
#                return elem

#    def getComponent(self, elem, name):
#        """ """
#        meas = elem.getElementsByTagName('measurement')
#        result = {}
#        dtime = ''
#        val = ''

#        for items in meas:
#            flag = False
#            for child in items.childNodes:
#                if child.tagName == 'component' \
#                        and child.firstChild.data == name:
#                    flag = True
#                if flag:
#                    if child.tagName == 'datetime_to':
#                        dtime = child.firstChild.data
#                    if child.tagName == 'value':
#                        val = child.firstChild.data
#                    if dtime and val:
#                        result[dtime] = val

#        return result

#    def retrieveXMLData(self, filename, code):
#        f = open(filename)
#        data = f.read()
#        f.close()

#        dom = parseString(data)

#        datap = DataXMLParser()
#        elem = datap.getStation(dom, code)
#        pm10 = datap.getComponent(elem, 'PM10')
#        pm2_5 = datap.getComponent(elem, 'PM2_5')
#        cc = datap.getCountryCode(dom)

#        #st_name = "%s, %s" % (st_name, cc)

#        return pm10, pm2_5


# class TextParser:
#    """ """

#    def __init__(self):
#        """ """
#        pass

#    def retrieveTXTData(self, filename, code):
#        """ """
#        f = open(filename)
#        data = f.read()
#        f.close()

#        d1 = {}
#        d2 = {}
#        lines = data.split('\n')

#        for line in lines:

#            if not line:
#                continue

#            #data = line.split('\t')
#            data = line.split()
#            cod = data[0]

#            if code != cod:
#                continue

#            dat = datetime.strptime(data[1], "%Y%m%d").strftime("%Y-%m-%d")
#            mdate = "%s %02d:00" % (dat, int(data[2]))
#            pm10 = data[3]
#            pm2_5 = data[4]

#            d1[mdate] = pm10
#            d2[mdate] = pm2_5

#        return d1, d2


# class PlotGenerator:

#    def __init__(self):
#        """ """
#        plt.clf()
#        plt.cla()

#    def setVar(self, var, mon, MR):
#        """ """
#        hrs = var.keys()
#        hrs.sort()
#        steps = {}
#        for dat in hrs:
#            try:
#                dt = datetime.strptime(dat, "%Y-%m-%d %H:%M")
#            except Exception, e:
#                #print e, "--", var
#                continue
#            day = dt.day
#            hour = dt.hour
#            if mon == dt.strftime("%Y%m"):
#                steps[(day*24)+hour] = var[dat]

#        res = []
#        for k in range(24,(MR+1)*24):
#            val = np.nan
#            if k in steps.keys():
#                val = steps[k]
#                if float(val) < 0:
#                    val = np.nan
#            #if val != 0: print val, k
#            res.append(val)

#        return res #np.array(res)

#    def generatePlot(self, xvals, varN, title, fname, MR):
#        """ """

#        mxs = []
#        for attrs in varN:
#            #print xvals, attrs['var'], type(attrs['var']), max(attrs['var'])
#            plt.plot(xvals,attrs['var'],attrs['color']+attrs['symbol'],label=attrs['label'])
#            values = [float(i) for i in attrs['var']]
#            #if title.find('Cairo') >= 0: print values, "MAX:", np.max(values)
#            mxs.append(np.nanmax(values))

#        f = plt.gcf()
#        DefaultSize = f.get_size_inches()

#        mx = np.nanmax(mxs)
#        #print title, mx
#        if np.isnan(mx): mx = 0
#        M = 50
#        if mx < M: mx = 50
#        INTY = mx/OFFS
#        INTY -= INTY%M
#        if INTY == 0: INTY = OFFS
#        MAXY = mx + INTY #200
#        ARGY = int((MAXY/OFFS)-(MAXY/OFFS)%INTY)
#        if ARGY == 0: ARGY = INTY
#        MAXX = (MR+1)*24 #768

#        ax = plt.axis([24,MAXX,0,MAXY])
#        ll = plt.legend(loc='upper right')
#        lx = plt.xlabel(XLABEL)
#        tx = plt.xticks(np.arange(24,(MR+1)*24,24),np.arange(1,(MR+1)))
#        ly = plt.ylabel(YLABEL)
#        ty = plt.yticks(np.arange(0,MAXY+1,ARGY))
#        tl = plt.title(title)
#        gr = plt.grid(True)

#        f.set_size_inches((DefaultSize[0]*1.5, DefaultSize[1]*1.5))
#        f.savefig(fname, dpi=72)
#        plt.close('all')


# if __name__ == "__main__":

#    import glob
#    import sys

#    msg_usage = """
# Error: %s
# Usage: %s <path> <date>
# - <path>: where find files to parse
# - <date>: a date without day in format %%Y%%m
# """

#    if len(sys.argv) != 3:
#        print msg_usage % ("bad number argument", sys.argv[0])
#        sys.exit(1)

#    path = sys.argv[1]
#    month = sys.argv[2]

#    try:
#        dt = datetime.strptime(month, "%Y%m")
#    except Exception, e:
#        print msg_usage % (str(e), sys.argv[0])
#        sys.exit(1)

#    filenames = glob.glob(path + '*')

#    MR = monthrange(dt.year, dt.month)[1]
#    num = (MR+1)*24 #days in one month x hours in a day
#    xvals = np.arange(24,num)
#    p = PlotGenerator()
#    tp = TextParser()

#    for code in STATIONS.keys():

#        if code == "IT0009R":
#            LABEL1 = 'Total'
#            LABEL2 = 'Coarse'
#            XLABEL = u'days'
#            YLABEL = r"number concentration  $(n/cm^3)$"
#            M = 1
#            OFFS = 3
#        else:
#            LABEL1 = 'PM10'
#            LABEL2 = 'PM2.5'
#            XLABEL = u'days'
#            YLABEL = r"mass concentration  $(\mu g/m^3)$"
#            M = 50
#            OFFS = 10

#        pm10 = {}
#        pm2_5 = {}
#        for filename in filenames:
#            if not os.path.isfile(filename):
#                continue
#            #d1, d2 = retrieveXMLData(filename)
#            d1, d2 = tp.retrieveTXTData(filename, code)
#            pm10.update(d1)
#            pm2_5.update(d2)

#        st_name = STATIONS[code]
#        var1 = p.setVar(pm10, month, MR)
#        var2 = p.setVar(pm2_5, month, MR)

#        title = unicode( "%s\n%s\n" % (st_name, date.strftime(dt, "%B %Y")))
#        figname = "%s-%s.png" % (month, code)

#        p.generatePlot(
#               xvals,
#               (
#                   {'var':var1,'color':'r','symbol':'-','label':LABEL1},
#                   {'var':var2,'color':'y','symbol':'-','label':LABEL2}
#               ),
#               title,
#               figname,
#               MR,
#           )

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
        self.plt_type = 'xy'
        # types:
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
            'date': dd.strftime(self.date_fmt),
            'year': dd.strftime('%Y'),
            'month': dd.strftime('%m'),
            'day': dd.strftime('%d'),
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
        obs = pd.read_table(
            obs_file,
            delimiter=' ',
            skiprows=1,
            # skipfooter=4,
            usecols=(0, 1, 2, 3),
            names=('datetime', 'lon', 'lat', self.obs_name),
            warn_bad_lines=False,
            error_bad_lines=False,
        )

        if self.mylogger:
            self.mylogger.debug("PARTIAL OBS:\n%s", obs.head())

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
                 '06': -3,
                 '12': -2,
                 '18': -1,
                 '00':  0,  # next day, so must go to previous
                }
        ostep = obs_date[-2:]
        cstep = rstep[ostep]  # current step

        if cstep == 0:
            # previous day
            odate = datetime.strptime(obs_date[:-2], self.date_fmt)
            odate -= timedelta(days=1)
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
                    usecols=(0, 1, 2, 3),
                    names=('datetime', 'lon', 'lat', self.obs_name),
                )

                if self.mylogger:
                    self.mylogger.debug(
                        "CSTEP: %s REJ VALS: %s", type(cstep),
                        tmp['datetime'].dtype
                    )
                # extract valid values
                tmp = tmp[tmp['datetime']==cstep]
                obs_rej_tmp.append(tmp)

        obs_rej = pd.concat(
            obs_rej_tmp, names=('datetime', 'lon', 'lat', self.obs_name)
        )
        if self.mylogger:
            self.mylogger.debug(
                "SHAPE: %s\tOBS TO BE REJECTED 1:\n%s", obs_rej.shape, obs_rej
            )

        # convert reject observation to the same format
        obs_rej['datetime'] = obs_rej['datetime'].replace(cstep, obs_date)
        obs_rej['lon'] = ((360.0/(129-1)) * (obs_rej['lon']-1-4)).round(2)
        obs_rej['lon'][obs_rej['lon']>180.] = (obs_rej['lon'] - 360).round(2)
        obs_rej['lat'] = (((180.0/(91-1)) * (91+4-obs_rej['lat']))-90).round(2)
        obs_rej[self.obs_name] = obs_rej[self.obs_name].round(2)

        if self.mylogger:
            self.mylogger.debug(
                "SHAPE: %s\tOBS TO BE REJECTED 2:\n%s", obs_rej.shape, obs_rej
            )
        if self.mylogger:
            self.mylogger.debug("OBS SHAPE BEFORE:\n%s", obs.shape)
        # remove from obs value present in obs_rej, rounded at the 2nd decimal
        obs = obs[~obs.round({'lon': 2, 'lat': 2}).isin(obs_rej)].dropna()
        if self.mylogger:
            self.mylogger.debug("OBS SHAPE AFTER:\n%s", obs.shape)

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
            self.mylogger.debug(
                "BEFORE\n\tOBSTMP: %s\n\tMODTMP: %s", obs_tmp, mod_tmp
            )
        obs_tmp, mod_tmp = self.checkFileMatch(obs_tmp, mod_tmp)
        if self.mylogger:
            self.mylogger.debug(
                "AFTER\n\tOBSTMP: %s\n\tMODTMP: %s",obs_tmp, mod_tmp
            )

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
            lon_idx = np.where(
                (lon >= self.lon_bnds[0]) & (lon <= self.lon_bnds[1])
            )
        else:
            lon_idx = (np.arange(lon.size),)

        if self.lat_bnds:
            lat_idx = np.where(
                (lat >= self.lat_bnds[0]) & (lat <= self.lat_bnds[1])
            )
        else:
            lat_idx = (np.arange(lat.size),)

        if self.mylogger:
            self.mylogger.debug(
                "LON_IDX: %s LAT_IDX: %s", lon_idx[0].size, lat_idx[0].size
            )

        # in case of observation lon and lat vector must have the same size
        if len(mod.shape) == 1:
            idx = np.intersect1d(lon_idx, lat_idx)
            return lon[idx], lat[idx], mod[idx]

        return (
            lon[lon_idx],
            lat[lat_idx],
            mod.squeeze()[lat_idx[0], :][:,lon_idx[0]].T
        )

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
            # if self.mylogger: self.mylogger.debug("DATA:\n%s" % (data))
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
            if self.mylogger:
                self.mylogger.debug(
                    "NLON: %s NLAT: %s NMOD: %s", nlon.shape, nlat.shape,
                    nmod.shape
                )

            # select region for obs
            xobs, yobs, nobs = self.selectRegion(obs['lon'].values, obs['lat'].values, obs[self.obs_name].values)
            if self.mylogger:
                self.mylogger.debug(
                    "XOBS: %s YOBS: %s NOBS: %s",
                    xobs.shape, yobs.shape, nobs.shape
                )

            # interpolate netcdf values to observation coords
            interp_func = RectBivariateSpline(nlon, nlat, nmod)
            interp_mod = interp_func(xobs, yobs, grid=False)
            if self.mylogger:
                self.mylogger.debug("INTERP_MOD: %s", interp_mod.shape)
            f.close()

            # create dataframe with a column for observations and another one
            # with interpolated model values
            d = {
                'datetime': pd.Series(obs['datetime']),
                self.obs_name: pd.Series(nobs),
                self.mod_name: pd.Series(interp_mod),
            }

            # append to the dataframe list
            frame_list.append(pd.DataFrame(d))

        if frame_list:
            if self.mylogger:
                self.mylogger.debug("FRAME LIST LEN: %s" % len(frame_list))
            # concatenate all dataframes into one
            data = pd.concat(frame_list)
            if self.mylogger:
                self.mylogger.debug("DATA:\n%s", data)

            # generate statistics
            self.genStats(data)  # model, obsrv)

            # generate plots
            self.genPlots(data)  # model, obsrv)

        else:
            if self.mylogger:
                self.mylogger.debug("Empty file list. Exit.")

        # remove tmp filelist
        self.cleanTmp()


def test_da():
    # /scratch/Earth/editomas/observations/modis_nrl_oceanland_aquaterra_AE_AI_count_selected/200705/2007051106_oceanland_aquaterra_obsnew.txt
    # /scratch/Earth/editomas/observations/modis_nrl_oceanland_aquaterra_AE_AI_count_selected/200705/2007051112_oceanland_aquaterra_obsnew.txt
    # /scratch/Earth/editomas/observations/modis_nrl_oceanland_aquaterra_AE_AI_count_selected/200705/2007051118_oceanland_aquaterra_obsnew.txt
    # /scratch/Earth/editomas/observations/modis_nrl_oceanland_aquaterra_AE_AI_count_selected/200705/2007051200_oceanland_aquaterra_obsnew.txt
    # /scratch/Earth/editomas/observations/modis_DB_land_aqua_AE_AI_Count_selected/200705/2007051112_deepblue_aqua_obsnew.txt
    # /scratch/Earth/editomas/data/nmmb-bsc-ctm-v2.0_DA-2007-NRLDB-bincorr1-uss-1aer/ENS/departures/2007051106-2007051200/obs_dep_rejected.txt

    str_date = "20070611"
    end_date = "20070612"

    # num = "84"

    obs_path = (
        "/scratch/Earth/editomas/observations/"
        "modis_nrl_oceanland_aquaterra_AE_AI_count_selected/",
        "/scratch/Earth/editomas/observations/"
        "modis_DB_land_aqua_AE_AI_Count_selected/",
    )
    obs_tmpl = (
        "%(year)s%(month)s/%(date)s*_oceanland_aquaterra_obsnew.txt",
        "%(year)s%(month)s/%(date)s*_deepblue_aqua_obsnew.txt",
    )

    rej_path = None
    # ("/scratch/Earth/editomas/data/"
    # "nmmb-bsc-ctm-v2.0_DA-2007-NRLDB-bincorr1-uss-1aer/ENS/departures/",)
    rej_tmpl = None  # ("%(date)s*/obs_dep_rejected.txt",)

    # MOD_PATH = "/scratch/Earth/editomas/data/"
    # "nmmb-bsc-ctm-v2.0_FC%s_CONTROL-2007-LR-5dd-IC-AN/ENS/"
    # "nc_analysis_validation/" % NUM
    mod_path = "/scratch/Earth/editomas/data/" \
        "nmmb-bsc-ctm-v2.0_FG-2007-NRLDB-bincorr1-uss-1aer/ENS/" \
        "nc_analysis_validation/"
    # FIX_TMPL = "_FC%(num)s_FC%(num)s_CONTROL-2007-LR-5dd-IC-AN.nc" % \
    #            { 'num' : NUM }
    fix_tmpl = "_FG-2007-NRLDB-bincorr1-uss-1aer.nc"
    mod_tmpl = "%(date)s*" + fix_tmpl

    dir_outp = "./OUT/"

    debug = True

    # create Class
    ev = Evaluator(
        str_date, end_date, obs_path, mod_path, obs_tmpl, mod_tmpl, dir_outp,
        rej_path, rej_tmpl, debug
    )

    # setting attributes
    ev.plt_xlim = (0, 4)
    ev.plt_ylim = (0, 4)
    # ev.lon_bnds = (-25, 60)
    # ev.lat_bnds = (0, 65)
    # ev.mod_name = ""
    # ev.obs_name = ""
    ev.plt_titl = "Glob FG 2007 (REJ)"  # % NUM
    ev.plt_imag = "glob_fg2007_image_rej.png"  # % NUM
    ev.fil_stat = "glob_fg2007_stats_rej.txt"  # % NUM

    # run
    ev.runEval()


def test_pollen():
    str_date = "20130328"
    end_date = "20130331"

    obs_path = "/home/Earth/fbeninca/Programs/ACtools/evaluation/tests/polen/"
    obs_tmpl = "Pollen_barcelona_2013-14_Pinus_Platanus_massa.csv"

    mod_path = "/home/Earth/fbeninca/Programs/ACtools/evaluation/tests/polen/"
    mod_tmpl = "%(date)s00/%(date)s00_NMMB-BSC-CTM_regular.nc"

    dir_outp = "./OUT/"

    debug = True

    # create Class
    ev = Evaluator(
        str_date, end_date, obs_path, mod_path, obs_tmpl, mod_tmpl, dir_outp,
        en_debug=debug
    )

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
    ev.plt_titl = u"Pollen March 2013 (g/m$^3$)"  # % NUM
    ev.plt_imag = "pollen_201303_scatter.png"  # % NUM
    ev.fil_stat = "pollen_201303.txt"  # % NUM

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
        # print "EXEC_ALL"
        try:
            test_da()
        except Exception as e:
            print("Error (DA):", e)
        try:
            test_pollen()
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
        hasattr(current_module, attr) and getattr(current_module, attr)()
        # or exec_all()
