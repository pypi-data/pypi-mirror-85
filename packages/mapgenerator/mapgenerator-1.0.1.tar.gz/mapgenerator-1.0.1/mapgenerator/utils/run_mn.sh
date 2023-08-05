#!/bin/bash 

USING_RELEASE=601
PATH="/gpfs/apps/GRADS/2.0.a9/bin/:$PATH"
PYTHON=/gpfs/apps/PYTHON/2.7.1/32/bin/python 
BASEDIR=/gpfs/projects/bsc32/bsc32359/CMAQ-mat/FORECAST/AQ/IMG
SRCDIR=$BASEDIR/bin/r${USING_RELEASE}
MAIN=$SRCDIR/map_main.py
CONFDIR="$SRCDIR/conf"
RUNDIR="$BASEDIR/run"
OUTDIRBASE="$BASEDIR/out"

#EXTERNAL FLAGS
while getopts cs: o
do case "$o" in
	c) CONF_ONLY=1;;
	s) MATCH=${OPTARG};;
	?) 
		echo "Usage: "
		echo -e "-c:\tCreate configuration files only (inside $RUNDIR)"
		;;
esac
done
shift $((OPTIND - 1))

DATE=$1
DOMAIN=$(echo $2 | tr [A-Z] [a-z])
SUBDOMAIN=$3 
UCDOMAIN=$(echo $2 | tr [a-z] [A-Z])

JULDATE=$( date --date=$DATE +%Y%j )
ALTDATE=$( date --date=$DATE +%d%b%Y | tr [A-Z] [a-z] )
ALTDATE_DUST=$( date --date="$DATE 1 day ago" +%d%b%Y | tr [A-Z] [a-z] )

echo "Running $DOMAIN/$SUBDOMAIN for $DATE"
#Expected name for configuration file 
CONF="$CONFDIR/${DOMAIN}.${SUBDOMAIN}.conf"
BNCONF="$(basename $CONF)"
WINDS_CONF="$RUNDIR/winds.$SUBDOMAIN.sdf"
POLLS_CONF="$RUNDIR/pollutants.$SUBDOMAIN.sdf"
DUST_CONF="$RUNDIR/dust.$SUBDOMAIN.sdf"
OUTDIR=$OUTDIRBASE/$DOMAIN/$SUBDOMAIN
SECTIONS=(  
            $(cat $CONF | grep "^\[BSC" | xargs | sed -e 's/\[//g' -e 's/\]//g')
         )


case $DOMAIN in
    eu)
        SPATH=F-EU12
	PDEF="pdef  478 398 lcc  19.70644    -22.32898   1   1   37.0  43.0 -3.0  12000.  12000."
	XDEF="xdef  590 linear  -40.9  0.16216218"
	YDEF="ydef  465 linear   15.1  0.10810812"
	ZCOEF=15
	DUST_IN="IN/IMAGE/CALIOPE8_D01_bilin.nc"
        ;;
    ip)
	SPATH=F-IP4
	PDEF="pdef  397 397 lcc   32.51078    -11.5483   1   1   37.0   43.0    -3.0  4000.  4000."
	XDEF="xdef  506 linear  -14.6  0.04504505"
	YDEF="ydef  450 linear   31.5  0.03603604"
	ZCOEF=15
	DUST_IN="IN/IMAGE/IMAGENES/CALIOPE8_D02_bilin.nc"
	;;
    can)
        SPATH=F-CAN2
	PDEF="pdef  302 202 lcc   26.35292  -18.58478   1   1   37.0   43.0    -3.0  2000.  2000."
	XDEF="xdef  571 linear  -19.4  0.012"
	YDEF="ydef  280 linear   26.25  0.016"
	ZCOEF=8
	DUST_IN="IN/IMAGE/IMAGENES/CALIOPE8_CAN_bilin.nc"
        ;;
    *)
        echo "Domain $DOMAIN invalid or not yet supported"
        ;; 
esac

cd $BASEDIR 
[[ -d $OUTDIR ]] || mkdir -p $OUTDIR
#rm -f $OUTDIR/*
## Modify the content of the configuration files upgrading the sdf files to the 
## ones dinamycally generated below
sed -e s/pollutants.sdf/$(basename $POLLS_CONF)/g \
    -e s/dust.sdf/$(basename $DUST_CONF )/g \
    -e s/winds.sdf/$(basename $WINDS_CONF | sed 's/\//\\\//g')/g \
	<$CONF >$RUNDIR/$BNCONF
#    -e s/outdir.*/outdir=$(echo $OUTDIR | sed 's/\//\\\//g')/g \
#    -e s/indir.*/indir=\./g 

#exit
## Dynamically generate sdf files 
cat >$POLLS_CONF <<POLLUTANTS.SDF 
dset /gpfs/projects/bsc32/bsc32359/CMAQ-mat/FORECAST/AQ/$SPATH/OUT/CCTM/$JULDATE/CCTM_FORECAST_${UCDOMAIN}CONC.FORECAST_$UCDOMAIN
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
dset /gpfs/projects/bsc32/bsc32359/CMAQ-mat/FORECAST/AQ/$SPATH/OUT/MCIP3/OUTPUT_MCIP_$JULDATE/METDOT3D_$UCDOMAIN
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
dset /gpfs/projects/bsc32/bsc32359/CMAQ-mat/FORECAST/AQ/$SPATH/$DUST_IN
title eta model 
dtype netcdf
undef -9999.
$PDEF
$XDEF
$YDEF
zdef 1 LINEAR 1 1
tdef 73 linear 12Z$ALTDATE_DUST 1hr 
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

set -x
ln -fs $SRCDIR/data $RUNDIR 
if [[ $CONF_ONLY -eq 0 ]]; then 
	for s in ${SECTIONS[@]}; do  
	    DO=1
	    if [[ -n "$MATCH" ]]; then 
		DO=0
		if [[ "$s" == *${MATCH}* ]]; then 
		    DO=1
		fi
	    fi
	    if [[ $DO -eq 1 ]]; then 
	        echo "Starting section $s"
	        START=$(date +%s)
	        $PYTHON $MAIN -c $RUNDIR/$BNCONF -i $RUNDIR -o $OUTDIR $s
	        END=$(date +%s)
	        echo "Section $s done in $(( END - START )) s"
            fi
	done 
	#rm $POLLS_CONF $WINDS_CONF
fi
