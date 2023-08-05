from datetime import datetime
import subprocess
import os
import logging

LOG = logging.getLogger(__name__)


def print_time(msg=None):
    """ Print time """
    # initial time
    if 'start_t' not in globals():
        global start_t, last_t
        LOG.info("Creating start_t")
        start_t = datetime.now()
        last_t = start_t

    now_t = datetime.now()
    diff_t = now_t - last_t
    if msg is not None:
        LOG.info('TIME: %s done in %s s', msg, diff_t.seconds)
    last_t = now_t


def run_command(comm_str):   # , fatal=True):
    """ Run command """
    LOG.info(comm_str)
    proc = subprocess.Popen(comm_str.split(), stderr=subprocess.PIPE)
    output, err = proc.communicate()
    LOG.info(output, '-----', err)
#        st, out = commands.getstatusoutput(comm_str)
#        if st != 0:
#            print "Error: %s" % str(out)
#            if (fatal == True):
#                sys.exit(1)


def gen_anim(inpattern, outfile, outdir, anim_delay):
    ''' Generate an animation starting from a set of
        images, specified by the inpattern parameter '''
    # print "Animation: ", indir, inpattern, outdir, outfile
    # Create animation
    run_command(
        "/usr/bin/convert -delay %s -loop 0 -layers Optimize %s/%s %s/%s"
        % (anim_delay, outdir, inpattern, outdir, outfile))
    # Remove intermediate files
    # run_command("rm %s/%s %s" % (indir, inpattern, map_name),
    # False)

#           ccc = []
#           ccc.extend(colors)
#           print "Filtering scatter data for date/hour: ",
#           curr_date.strftime("%Y%m%d"), s_time24 csv_lat, csv_lon, csv_val =
#           csv_handler.filter(curr_date.strftime("%Y%m%d"), s_time24)
#           #csv_col = dataTransform.setColorsFromBuckets(ccc,
#           bounds, csv_con)
#           if(len(csv_lat) > 0):
#               scatter_data = [csv_lon, csv_lat, 40, csv_col]
#               print "**************** SCATTER_DATA", scatter_data
#               print "Filtered %d records for scatterplot" % len(scatter_data)


def set_resolution(lon, lat):
    """ 110m, 50m, 10m """
    # lats = 36, 72, 108, 144, 180
    # lons = 72, 144, 216, 288, 360
    minlat, maxlat = lat[0], lat[-1]
    minlon, maxlon = lon[0], lon[-1]
    lats = maxlat + abs(minlat)
    lons = maxlon + abs(minlon)
    if lats > 100 and lons > 200:
        resolution = '110m'
        zoom = 1
    elif lats > 45 and lons > 75:
        resolution = '50m'
    elif lats <= 45 and lons <= 75:
        resolution = '10m'
        zoom = 4
    else:
        resolution = '110m'  # default
        zoom = 8
    return resolution, zoom


def set_title(title, sdate, cdate, step, stime):
    """ Set the title of the current image to the one provided, substituting the
        patterns """

    title_dic = {
        'syear':  sdate.strftime("%Y"),
        'smonth': sdate.strftime("%m"),
        'sMONTH': sdate.strftime("%b"),
        'sday':   sdate.strftime("%d"),
        'shour':  sdate.strftime("%H"),
        'year':   cdate.strftime("%Y"),
        'month':  cdate.strftime("%m"),
        'MONTH':  cdate.strftime("%b"),
        'day':    cdate.strftime("%d"),
        'hour':   cdate.strftime("%H"),
        'step':   step,
        'simday': "%d" % (int(stime)/24),
        'simhh':  stime,
        # 'simhh':  "%02d" % (int(stime)%24)
    }

    try:
        p_title = str(title) % title_dic  # ("%sh" % s_time, valid)
    except Exception as err:
        LOG.error("Title error: %s", str(err))
        p_title = title % title_dic  # ("%sh" % s_time, valid)

    return p_title


def gen_kml(fig_names, var_name, lon, lat, dims, outdir='.', online=True):
    """ Generate KML/KMZ files """
    from lxml import etree
    from pykml.factory import KML_ElementMaker as KML
    import zipfile

    LOG.info(fig_names)
    # kml_name = '-'.join(os.path.basename(fig_names[0]).split('-')[:-1])
    kml_name = os.path.basename(fig_names[0])[:-3]
    run_date0 = datetime.strptime(dims[0], "%HZ%d%b%Y")
    run_date1 = datetime.strptime(dims[1], "%HZ%d%b%Y")
    begindate = run_date0.strftime("%Y%m%d%H")
    dir_name = os.path.join(outdir, begindate + '-' +
                            var_name).replace('./', '')
    interval = run_date1 - run_date0
    datefmt = "%Y-%m-%dT%H:00:00Z"

    doc = KML.kml(
        KML.Folder(
            KML.name(kml_name),
            KML.LookAt(
                KML.longitude((lon[1]+lon[-1])/2),
                KML.latitude((lat[1]+lat[-1])/2),
                KML.range(8500000.0),
                KML.tilt(0),
                KML.heading(0),
            ),
            KML.ScreenOverlay(
                KML.name("Legend"),
                KML.open(1),
                KML.Icon(
                    KML.href("%s/%s-colorbar.png" % (dir_name, begindate)),
                ),
                KML.overlayXY(x="0", y="1", xunits="fraction",
                              yunits="fraction"),
                KML.screenXY(x=".01", y="0.55", xunits="fraction",
                             yunits="fraction"),
                KML.rotationXY(x="0", y="0", xunits="fraction",
                               yunits="fraction"),
                KML.size(x="0", y="0.5",
                         xunits="fraction",
                         yunits="fraction"),
                id="%s-ScreenOverlay" % begindate,
            ),
        )
    )

    os.makedirs(dir_name)

    if not online:
        zfile = zipfile.ZipFile("%s.kmz" % kml_name, 'w')

    for fig_name, dat in zip(fig_names, sorted(dims.keys())):
        dtime = dims[dat]
        fig_name = fig_name + ".png"
        fig_path = os.path.join(dir_name, os.path.basename(fig_name))
        startdate = datetime.strptime(dtime, "%HZ%d%b%Y")
        begdate = startdate.strftime(datefmt)
        enddate = (startdate + interval).strftime(datefmt)
        starth = startdate.hour
        doc.Folder.append(KML.GroundOverlay(
            KML.name("%02d:00:00Z" % starth),
            KML.TimeSpan(
                KML.begin(begdate),
                KML.end(enddate),
            ),
            KML.Icon(
                KML.href(fig_path),
                KML.viewBoundScale(1.0),
            ),
            KML.altitude(0.0),
            KML.altitudeMode("relativeToGround"),
            KML.LatLonBox(
                KML.south(lat[0]),
                KML.north(lat[-1]),
                KML.west(lon[0]),
                KML.east(lon[-1]),
                KML.rotation(0.0),
            ),
        ))

        if os.path.exists(fig_name):
            os.rename(fig_name, fig_path)
            zfile.write(fig_path)

    outf = open("%s.kml" % kml_name, 'w')
    outf.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    outf.write(etree.tostring(doc, pretty_print=True))
    outf.close()

    if not online:
        zfile.write("%s.kml" % kml_name)
        zfile.write("%s/%s-colorbar.png" % (dir_name, begindate))
        zfile.close()

        for img in os.listdir(dir_name):
            os.remove("%s/%s" % (dir_name, img))
        os.rmdir(dir_name)
        os.remove("%s.kml" % kml_name)
