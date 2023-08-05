#!/bin/bash

#date
DATE=$(date +%Y%m%d)
#DATE=`expr $DATE - 1`
FNAME="$DATE"_BSC_DREAM8b.nc
CURDIR="/opt/mapgenerator"

cd $CURDIR

#download
cp /home/bsccns/products/BSC-DREAM8b/archive/"$FNAME" ./STORAGE/files/

sleep 1

#create map
./map_generator.py "$FNAME" SCONC_DUST
./map_generator.py "$FNAME" OD550_DUST

cd STORAGE/archive

upload1="$DATE"-BSC_DREAM8b-SCONC_DUST-loop.gif
upload2="$DATE"-BSC_DREAM8b-OD550_DUST-loop.gif

#upload
lftp << EOF
open ftp.wmo.int
put $upload1
mv $upload1 sdsanim.gif
put $upload1
put $upload2
mv $upload2 airqualanim.gif
put $upload2
bye
EOF
