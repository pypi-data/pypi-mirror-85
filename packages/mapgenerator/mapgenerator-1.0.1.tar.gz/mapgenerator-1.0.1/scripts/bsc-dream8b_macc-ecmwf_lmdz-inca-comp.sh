#!/bin/bash

YYYY=`date +%Y --d='yesterday'`
MM=`date +%m --d='yesterday'`
mm=`date +%b --d='yesterday' | tr '[a-z]' '[A-Z]'`
DD=`date +%d --d='yesterday'`

#MM=04
#mm="APR"
#DD=30

DATE=$YYYY$MM$DD

echo $DATE

MOD1="BSC_DREAM8b"
MOD2="3H_MACC-ECMWF"
MOD3="DD_LMDZINCAecmwf"

VAR1="SCONC_DUST"
VAR2="OD550_DUST"

FNAME1="$DATE"_"$MOD1".nc
FNAME2="$DATE"00_"$MOD2".nc
FNAME3="$DATE"00_"$MOD3".nc

CURDIR="/opt/mapgenerator"
#TODIR1="/srv/www/vhosts/sds-was/sites/all/images/products/"
TODIR="/opt/plone/zeocluster/var/reflector/files/products/"

echo $FNAME1
echo $FNAME2
echo $FNAME3

cd $CURDIR

#download
cp /home/bsccns/products/BSC-DREAM8b/archive/"$FNAME1" ./STORAGE/files/
cp /home/bsccns/products/ECMWF/archive/"$FNAME2" ./STORAGE/files/
cp /home/bsccns/products/LMDZINCA/archive/"$FNAME3" ./STORAGE/files/

sleep 1

#create map
./map_generator.py "$FNAME1","$FNAME2","$FNAME3" "$VAR1"
./map_generator.py "$FNAME1","$FNAME2","$FNAME3" "$VAR2"

#12Z25APR2011

LNAME1=$MOD1-$MOD2-$MOD3-$VAR1-loop
LNAME2=$MOD1-$MOD2-$MOD3-$VAR2-loop
RNAME1=$LNAME1-12Z$DD$mm$YYYY
RNAME2=$LNAME2-12Z$DD$mm$YYYY


mkdir /home/bsccns/products/comparison/archive/$DATE
#cd /home/products/comparison/archive/$DATE
cd ./STORAGE/archive
for i in `ls $MOD1-$MOD2-$MOD3-*-12Z$DD$mm$YYYY.gif`
    do
        tmp=`echo $i | sed "s/$MOD1-$MOD2-$MOD3-\(.*\)-12Z$DD$mm$YYYY/comparison-\1/g"`
        tmp=`echo $tmp | sed "s/loop/-loop-/g"`
        tmp2=`echo $tmp | sed "s/.gif/-LARGE.gif/g"`
        mv $i /home/bsccns/products/comparison/archive/$DATE/$tmp2
        cd /home/bsccns/products/comparison/archive/$DATE/
        convert $tmp2 -resize 768x768\> $tmp
        cd $CURDIR/STORAGE/archive
    done

##copy 
##cp ./STORAGE/archive/$DATE-$MOD1-$MOD2-compared-map-$VAR1-loop.gif $TODIR1/$MOD1-$MOD2-compared-map-$VAR1-loop.gif
##cp ./STORAGE/archive/$DATE-$MOD1-$MOD2-compared-map-$VAR2-loop.gif $TODIR1/$MOD1-$MOD2-compared-map-$VAR2-loop.gif
#
##cp ./STORAGE/archive/$RNAME1.gif $TODIR/$LNAME1-LARGE.gif
##cp ./STORAGE/archive/$RNAME2.gif $TODIR/$LNAME2-LARGE.gif
##
##cd $TODIR
##convert $LNAME1-LARGE.gif -resize 768x768\> $LNAME1.gif
##convert $LNAME2-LARGE.gif -resize 768x768\> $LNAME2.gif
