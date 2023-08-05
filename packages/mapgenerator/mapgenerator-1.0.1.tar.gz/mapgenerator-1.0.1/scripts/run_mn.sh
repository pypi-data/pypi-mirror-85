#!/bin/bash 

PATH="/gpfs/apps/IMAGEMAGICK/6.7.3-5/bin/:/gpfs/apps/GRADS/2.0.a9/bin/:$PATH"
PYTHON=/gpfs/apps/PYTHON/2.7.1/32/bin/python 
BASEDIR=/gpfs/projects/bsc32/bsc32359/CMAQ-mat/FORECAST/AQ/IMG
DEFAULT_DATADIRBASE=/gpfs/projects/bsc32/bsc32359/CMAQ-mat/FORECAST/

usage(){
	echo "Usage: "
	echo "$(basename $0) [-abcdopr] DATE DOMAIN SUBDOMAIN CLASS"
	echo -e "  DATE in YYYYMMDD format"
    echo -e "  CLASS in {aq, emis}"
	echo -e "\nOPTIONS:"
	echo -e "  -a:\tAdditional arguments to pass to the python executable"
	echo -e "  -b:\tSet basedir to given value"
	echo -e "  -c:\tSet configuration dir to given value"
	echo -e "  -C:\tCreate configuration files only (inside $RUNDIR)"
    echo -e "  -d:\tSet data dir base to given value"
    echo -e "  -o:\tSet out dir base to given value"
    echo -e "  -p:\tUse the given python executable"
    echo -e "  -r:\tUse specified release"
    echo -e "  -s:\tUse specified source dir"
    echo -e "  -S:\tMatch string"
	[[ -n $2 ]] && echo "Message: $2"
        [[ -n $1 ]] && exit $1
}

get_release() {
 echo $(ls -l $0 | sed 's/.*r\([0-9]*\)\/.*/\1/')
}

exitError() {
    EXIT_VALUE=$1
    shift 
    echo $*
    exit $EXIT_VALUE
}

#EXTERNAL FLAGS
while getopts a:b:Cc:d:o:p:r:s:S: o
do case "$o" in
    a)
        echo "Additional arguments '${OPTARG}'"
        ADDARGS=${OPTARG}
        ;;
    b)
        echo "Using basedir: ${OPTARG}"
        BASEDIR="${OPTARG}"
        ;;
    C)  CONF_ONLY=1;;
    c)
        echo "Using configuration dir: ${OPTARG}"
        CONFDIR=${OPTARG}
        ;;
    d)  echo "Using data base dir: ${OPTARG}"
        DATADIRBASE="${OPTARG}"
        ;;
    o)  
        echo "Using output base dir : ${OPTARG}"
        OUTDIRBASE=${OPTARG}
        ;;
    p)
        echo "Using python: ${OPTARG}"
        PYTHON="${OPTARG}"
        ;;
    r)
        echo "Using release: ${OPTARG}"
        USING_RELEASE=${OPTARG}
        ;;
    s)  
        echo "Using srcdir: ${OPTARG}"
        SRCDIR=${OPTARG}
        ;;
    S)  MATCH=${OPTARG};;
	?) 
        usage 1 
		;;
esac
done
shift $((OPTIND - 1))

[[ $# -eq 4 ]] || usage 2 
[[ -z $USING_RELEASE ]] && USING_RELEASE=$(get_release)

DATE=$1
DOMAIN=$(echo $2 | tr [A-Z] [a-z])
UCDOMAIN=$(echo $2 | tr [a-z] [A-Z])
SUBDOMAIN=$3 
CLASS=$(echo $4 | tr [A-Z] [a-z])

MAIN=map_main.py
RUNDIR="$BASEDIR/run"
[[ -n $SRCDIR ]] || SRCDIR=$BASEDIR/releases/r${USING_RELEASE}
[[ -d $SRCDIR ]] || usage 3 "$SRCDIR is not a valid source directory"
[[ -n $DATADIRBASE ]] || DATADIRBASE=$DEFAULT_DATADIRBASE
[[ -n $OUTDIRBASE ]] || OUTDIRBASE="$BASEDIR/out"
[[ -n $CONFDIR ]] || CONFDIR="$SRCDIR/conf"
[[ -n $CLASS ]] || CLASS=aq
[[ -d $RUNDIR ]] || mkdir $RUNDIR 
[[ -d $RUNDIR/$CLASS ]] || mkdir $RUNDIR/$CLASS

echo "Using release #$USING_RELEASE"
echo "Basedir is: $BASEDIR"
echo "Srcdir  is: $SRCDIR"
echo "Rundir  is: $RUNDIR"
echo "Datadir base is: $DATADIRBASE"
echo "Using config directory $CONFDIR"
echo "Using output directory $OUTDIRBASE"

JULDATE=$( date --date=$DATE +%Y%j )
ALTDATE=$( date --date=$DATE +%d%b%Y | tr [A-Z] [a-z] )
ALTDATE_1DAGO=$( date --date="$DATE 1 day ago" +%d%b%Y | tr [A-Z] [a-z] )
UCCLASS=$(echo $CLASS | tr [a-z] [A-Z])

echo "Running $DOMAIN/$SUBDOMAIN for $DATE"
#Expected name for configuration file 
CONF="$CONFDIR/$CLASS/${DOMAIN}.${SUBDOMAIN}.conf"
BNCONF="$(basename $CONF)"
WINDS_CONF="$RUNDIR/winds.$SUBDOMAIN.sdf"
POLLS_CONF="$RUNDIR/pollutants.$SUBDOMAIN.sdf"
DUST_CONF="$RUNDIR/dust.$SUBDOMAIN.sdf"
EMIS_CONF="$RUNDIR/emissions.$SUBDOMAIN.sdf"
METEO_CONF="$RUNDIR/meteo.$SUBDOMAIN.sdf"
OUTDIR=$OUTDIRBASE/$DATE/$CLASS/$DOMAIN/$SUBDOMAIN
SECTIONS=(  
            $(cat $CONF | grep "^\[BSC" | xargs | sed -e 's/\[//g' -e 's/\]//g')
         )

NR_CONT="NR=>nr 11 t,z,y,x Non_reactive"
case $DOMAIN in
    eu)
    SPATH=F-EU12
	PDEF="pdef  478 398 lcc  19.70644    -22.32898   1   1   37.0  43.0 -3.0  12000.  12000."
	XDEF="xdef  590 linear  -40.9  0.16216218"
	YDEF="ydef  465 linear   15.1  0.10810812"
    METEO_PDEF="pdef 480 400 lcc  19.585  -22.411    1.000    1.000  43.  37.   -3.000  12000.  12000."
    METEO_SIM_START="12z$ALTDATE_1DAGO"
    METEO_DATAFILE="ARW1.dat"
    METEO_TSTEPS=61
	ZCOEF=15
	DUST_IN="IN/IMAGE/CALIOPE8_D01_bilin.nc"
    EMIS_DOM=01
    EMIS_DATA=${DATADIRBASE}/EMIS-2011/OUT/Emisiones_EU12_${JULDATE}.nc
    NR_CONT="UNR=>nr 11 t,z,y,x Non_reactive"
        ;;
    ip)
	SPATH=F-IP4
	PDEF="pdef  397 397 lcc   32.51078    -11.5483   1   1   37.0   43.0    -3.0  4000.  4000."
	XDEF="xdef  506 linear  -14.6  0.04504505"
	YDEF="ydef  450 linear   31.5  0.03603604"
    METEO_PDEF="pdef 399 399 lcc  32.472  -11.587    1.000    1.000  43.  37.   -3.000   4000.   4000."
    METEO_SIM_START="18z$ALTDATE_1DAGO"
    METEO_DATAFILE="ARW2.dat"
    METEO_TSTEPS=55
	ZCOEF=15
	DUST_IN="IN/IMAGE/IMAGENES/CALIOPE8_D02_bilin.nc"
    EMIS_DOM=02
    EMIS_DATA=${DATADIRBASE}/EMIS/OUT/CALIOPE_D${EMIS_DOM}_${JULDATE}.nc
	;;
    can)
        SPATH=F-CAN2
	PDEF="pdef  302 202 lcc   26.35292  -18.58478   1   1   37.0   43.0    -3.0  2000.  2000."
	XDEF="xdef  571 linear  -19.4  0.012"
	YDEF="ydef  280 linear   26.25  0.016"
    METEO_PDEF="pdef 304 204 lcc  26.333  -18.601    1.000    1.000  43.  37.   -3.000   2000.   2000."
    METEO_SIM_START="00z$ALTDATE"
    METEO_DATAFILE="ARW1.dat"
    METEO_TSTEPS=49
    METEO_NVARS=19
	ZCOEF=8
	DUST_IN="IN/IMAGE/IMAGENES/CALIOPE8_CAN_bilin.nc"
    EMIS_DOM=03
    EMIS_DATA=${DATADIRBASE}/EMIS/OUT/CALIOPE_D${EMIS_DOM}_${JULDATE}.nc
        ;; 
    and)
	SPATH=F-AND2
	PDEF="pdef  332 178 lcc   35.72874  -7.968964   1   1   37.0   43.0    -3.0  2000.  2000."
	XDEF="xdef  340 linear  -7.9  0.0215"
	YDEF="ydef  180 linear   35.9  0.017"
	ZCOEF=15
    METEO_PDEF="pdef 334 180 lcc  35.710   -7.990    1.000    1.000  43.  37.   -3.000   2000.   2000."
    METEO_SIM_START="00z$ALTDATE"
    METEO_DATAFILE="ARW1.dat"
    METEO_TSTEPS=49
    METEO_NVARS=19
	DUST_IN="IN/IMAGE/CALIOPE8_AND_bilin.nc"
    EMIS_DOM=05
    EMIS_DATA=${DATADIRBASE}/EMIS/OUT/CALIOPE_D${EMIS_DOM}_${JULDATE}.nc
	;;
    bcn)
	SPATH=F-BCN1
	PDEF="pdef  146 146 lcc   40.76655  0.9212646   1   1   37.0   43.0    -3.0  1000.  1000."
	XDEF="xdef  380 linear  0.90  0.005"
	YDEF="ydef  300 linear  40.65  0.005"
	ZCOEF=8
    METEO_PDEF="pdef 148 148 lcc  40.758     .909    1.000    1.000  43.  37.   -3.000   1000.   1000."
    METEO_SIM_START="00z$ALTDATE"
    METEO_DATAFILE="ARW1.dat"
    METEO_TSTEPS=49
    METEO_NVARS=19
	DUST_IN="IN/IMAGE/CALIOPE8_BCN_bilin.nc"
    EMIS_DOM=04
    EMIS_DATA=${DATADIRBASE}/EMIS/OUT/CALIOPE_D${EMIS_DOM}_${JULDATE}.nc
	;;
    *)
        echo "Domain $DOMAIN invalid or not yet supported"
        ;; 
esac

DUST_DATA=${DATADIRBASE}/$UCCLASS/$SPATH/$DUST_IN
POLL_DATA=${DATADIRBASE}/$UCCLASS/$SPATH/OUT/CCTM/$JULDATE/CCTM_FORECAST_${UCDOMAIN}CONC.FORECAST_$UCDOMAIN
WIND_DATA=${DATADIRBASE}/$UCCLASS/$SPATH/OUT/MCIP3/OUTPUT_MCIP_$JULDATE/METDOT3D_$UCDOMAIN
METEO_DATA=${DATADIRBASE}/$UCCLASS/IN/Images/WRF2GRADS-$UCDOMAIN/$METEO_DATAFILE

if [[ $DATADIRBASE != $DEFAULT_DATADIRBASE ]]; then
    EMIS_DATA=${DATADIRBASE}/$(basename $EMIS_DATA)
    POLL_DATA=${DATADIRBASE}/$(basename $POLL_DATA)
    DUST_DATA=${DATADIRBASE}/$(basename $DUST_DATA)
    WIND_DATA=${DATADIRBASE}/$(basename $WIND_DATA)
fi

echo -e "**** Data sources\n$EMIS_DATA\n$POLL_DATA\n$WIND_DATA\n$DUST_DATA"

cd $SRCDIR/bin
[[ -d $OUTDIR ]] || mkdir -p $OUTDIR
#rm -f $OUTDIR/*
## Modify the content of the configuration files upgrading the sdf files to the 
## ones dinamycally generated below
sed -e s/pollutants.sdf/$(basename $POLLS_CONF)/g \
    -e s/dust.sdf/$(basename $DUST_CONF )/g \
    -e s/winds.sdf/$(basename $WINDS_CONF | sed 's/\//\\\//g')/g \
	<$CONF >$RUNDIR/$CLASS/$BNCONF
#    -e s/max\[\ \]\*=.\*/max\ =\ 0,/ \
#    -e s/outdir.*/outdir=$(echo $OUTDIR | sed 's/\//\\\//g')/g \
#    -e s/indir.*/indir=\./g 

## Dynamically generate sdf files 


case $CLASS in 
    emis)
cat >$EMIS_CONF <<EMISSIONS.SDF 
dset ${EMIS_DATA}
title Models-3 DATA
dtype netcdf
undef -9999.
$PDEF
$XDEF
$YDEF
zdef 11 LINEAR 1 1
tdef 49 LINEAR 00:00Z$ALTDATE 01hr
vars 22
NH3=>nh3 11 t,z,y,x Ammonia
NO=>no 11 t,z,y,x Nitrogen_Monoxide
NO2=>no2 11 t,z,y,x Nitrogen_Dioxide
CO=>co 11 t,z,y,x Carbon_Monoxide
SO2=>so2 11 t,z,y,x Sulphur Dioxide
PAR=>par 11 t,z,y,x ASO4I
PMC=>pmc 11 t,z,y,x ACORS
PMFINE=>pmfine 11 t,z,y,x pm25
PEC=>pec 11 t,z,y,x elemental_carbon
POA=>poa 11 t,z,y,x POA
PSO4=>pso4 11 t,z,y,x PSO4
PNO3=>pno3 11 t,z,y,x PNO3
ALD2=>ald2 11 t,z,y,x Aldehydes
ETH=>eth 11 t,z,y,x Ethene
FORM=>form 11 t,z,y,x Formaldehyde
${NR_CONT}
OLE=>ole 11 t,z,y,x Olefines
PAR=>par 11 t,z,y,x Parafines
TOL=>tol 11 t,z,y,x Toluene
XYL=>xyl 11 t,z,y,x Xylene
ISOP=>isop 11 t,z,y,x Isoprene
TERPB=>terpb 11 t,z,y,x Biogenic_terpenes
endvars
EMISSIONS.SDF
    ;; 
meteo)
cat >${METEO_CONF}<<METEO.SDF
dset ${METEO_DATA}                            
undef 1.e35
${METEO_PDEF}
${XDEF}
${YDEF}
zdef   15 levels  
 1000.00000
  950.00000
  900.00000
  850.00000
  800.00000
  750.00000
  700.00000
  650.00000
  600.00000
  550.00000
  500.00000
  450.00000
  400.00000
  350.00000
  300.00000
tdef        $METEO_TSTEPS linear $METEO_SIM_START  1hr
vars   20
UMET            15 0 U Compoment of wind - rotated (diagnostic)        
VMET            15 0 V Component of wind - rotated (diagnostic)        
W               15 0 W Component of wind                               
TK              15 0 Temperature in K                                  
P               15 0 Pressure (HPa)                                    
Z               15 0 Height (m)                                        
QVAPOR          15 0 Vapor                                             
TD              15 0 Dewpoint Temperature (diagnostic)                 
RH              15 0 Relative Humidity (diagnostic)                    
HGT             0  0 Terrain Height                                    
Q2              0  0 QV at 2 M                                         
OLR             0  0 Outgoing longwave radiation
RAINC           0  0 ACCUMULATED TOTAL CUMULUS PRECIPITATION           
RAINNC          0  0 ACCUMULATED TOTAL GRID SCALE PRECIPITATION        
slvl            0  0 sea level pressure                                
T2              0  0 TEMP at 2 M                                       
U10M            0  0 U at 10 M - rotated                               
V10M            0  0 V at 10 M - rotated                               
PBLH            0  0 PBL height                                        
TCOL            0  0 total colum cloud water                           
endvars
METEO.SDF
;;
aq)
cat >$POLLS_CONF <<POLLUTANTS.SDF 
dset ${POLL_DATA}
title Models-3 DATA
dtype netcdf
undef -9999.
$PDEF
$XDEF
$YDEF
zdef 15 LINEAR 1 1
tdef 49 LINEAR 00:00Z$ALTDATE 01hr
vars 26
O3=>o3 15 t,z,y,x Ozone
NO=>no 15 t,z,y,x Nitrogen_Monoxide
NO2=>no2 15 t,z,y,x Nitrogen_Dioxide
CO=>co 15 t,z,y,x Carbon_Monoxide
SO2=>so2 15 t,z,y,x Sulphur Dioxide
ASO4I=>aso4i 15 t,z,y,x ASO4I
ASO4J=>aso4j 15 t,z,y,x ASO4J
ANO3I=>ano3i 15 t,z,y,x ANO3I
ANO3J=>ano3j 15 t,z,y,x ANO3J
ANH4I=>anh4i 15 t,z,y,x ANH4I
ANH4J=>anh4j 15 t,z,y,x ANH4J
AORGAI=>aorgai 15 t,z,y,x AORGAI
AORGAJ=>aorgaj 15 t,z,y,x AORGAJ
AORGPAI=>aorgpai 15 t,z,y,x AORGPAI
AORGPAJ=>aorgpaj 15 t,z,y,x AORGPAJ
AORGBI=>aorgbi 15 t,z,y,x AORGBI
AORGBJ=>aorgbj 15 t,z,y,x AORGBJ
AECI=>aeci 15 t,z,y,x AECI
AECJ=>aecj 15 t,z,y,x AECJ
ANAJ=>anaj 15 t,z,y,x ANAJ
ACLJ=>aclj 15 t,z,y,x ACLJ
ANAK=>anak 15 t,z,y,x ANAK
ACLK=>aclk 15 t,z,y,x ACLK
ASO4K=>aso4k 15 t,z,y,x ASO4K
A25J=>a25j 15 t,z,y,x A25J
ACORS=>acors 15 t,z,y,x ACORS
endvars
POLLUTANTS.SDF

cat >$WINDS_CONF <<WINDS.SDF
dset ${WIND_DATA}
title Models-3 DATA
dtype netcdf
undef -9999.
$PDEF
$XDEF
$YDEF
zdef $ZCOEF LINEAR 1 1
tdef 49 LINEAR 00:00Z$ALTDATE 01hr
vars 2
UWIND=>uwind $ZCOEF t,z,y,x uwind
VWIND=>vwind $ZCOEF t,z,y,x vwind
endvars
WINDS.SDF

cat >$DUST_CONF <<DUST.SDF
dset ${DUST_DATA}
title eta model 
dtype netcdf
undef -9999.
$PDEF
$XDEF
$YDEF
zdef 1 LINEAR 1 1
tdef 73 linear 12Z$ALTDATE_1DAGO 1hr 
vars 16
tmp1=>tmp1 1 t, y, x tmp1
tmp2=>tmp2 1 t, y, x tmp2
tmp3=>tmp3 1 t, y, x tmp3
tmp4=>tmp4 1 t, y, x tmp4
tmp5=>tmp5 1 t, y, x tmp5
tmp6=>tmp6 1 t, y, x tmp6
tmp7=>tmp7 1 t, y, x tmp7
tmp8=>tmp8 1 t, y, x tmp8
dod1=>dod1 1 t, y, x dod1
dod2=>dod2 1 t, y, x dod2
dod3=>dod3 1 t, y, x dod3
dod4=>dod4 1 t, y, x dod4
dod5=>dod5 1 t, y, x dod5
dod6=>dod6 1 t, y, x dod6
dod7=>dod7 1 t, y, x dod7
dod8=>dod8 1 t, y, x dod8
endvars
DUST.SDF
    ;;
esac 

set -x
[[ ! -d $RUNDIR/data ]] && ln -fs $SRCDIR/data $RUNDIR 
if [[ $CONF_ONLY -eq 0 ]]; then 
	for s in ${SECTIONS[@]}; do  
	    DO=1
	    if [[ -n "$MATCH" ]]; then 
		DO=0
		if [[ "$s" == *${MATCH} ]]; then 
		    DO=1
		fi
	    fi
	    if [[ $DO -eq 1 ]]; then 
	        echo "Starting section $s"
	        START=$(date +%s)
	        $PYTHON $MAIN -c $RUNDIR/$CLASS/$BNCONF -i $RUNDIR -o $OUTDIR $ADDARGS $s
	        END=$(date +%s)
	        echo "Section $s done in $(( END - START )) s"
            fi
	done 
	#rm $POLLS_CONF $WINDS_CONF
fi
