#!/bin/bash

JOBIFY=/gpfs/projects/bsc32/share/bin/jobify.sh
IMG_NEW=/gpfs/projects/bsc32/bsc32359/CMAQ-mat/FORECAST/AQ/IMG
YEARMONTHDAY=`date +%Y%m%d`
AQ=1
EMI=0
IDIR=$IMG_NEW

while getopts a:d:e:i:x: opt; do
	case "$opt" in
		a) 
		    [[ $OPTARG -eq 1 ]] && AQ=1
		    [[ $OPTARG -eq 0 ]] && AQ=0
			;;
		d) 
		    echo "Setting date to $OPTARG"
		    YEARMONTHDAY=$OPTARG
			;;
		e) 
		    [[ $OPTARG -eq 1 ]] && EMI=1
		    [[ $OPTARG -eq 0 ]] && EMI=0
			;;
		i)
		    echo "Setting initial dir to $OPTARG"
		    IDIR=$OPTARG
			;;
		x)
		    echo "Setting additional options $OPTARG"
		    AOPTS=$OPTARG
			;;
	       \?) echo "Usage: $0 [-a 0|1] [-d DATE] [-e 0|1]"
			;;
	esac
done 

echo "IDIR : $IDIR"
echo "DATE : $YEARMONTHDAY"
echo "AQ?  : $AQ"
echo "EMIS?: $EMI"
[[ -n $AOPTS ]] && echo "AOPTS: $AOPTS"

for p in eu ip; do
        [[ $EMI -eq 1 ]] && $JOBIFY -n img_emis_${p} -w2h -a es1 -c benchmark -i $IDIR -l logs ./run_mn.sh -b $IDIR $AOPTS $YEARMONTHDAY ${p} ${p} emis
        [[ $AQ -eq 1 ]] && $JOBIFY -n img_aq_${p} -w2h -a es1 -c benchmark -i $IDIR -l logs ./run_mn.sh -b $IDIR $AOPTS $YEARMONTHDAY ${p} ${p} aq
done 
for p in andalucia aragon asturias baleares cantabria castillalamancha castillaleon catalunya extremadura galicia larioja madrid murcia navarra paisvasco valencia ; do
        [[ $EMI -eq 1 ]] && $JOBIFY -n img_emis_${p} -w1h -a es1 -c benchmark -i $IDIR -l logs ./run_mn.sh -b $IDIR $AOPTS $YEARMONTHDAY IP ${p} emis
        [[ $AQ -eq 1 ]] && $JOBIFY -n img_aq_${p} -w1h -a es1 -c benchmark -i $IDIR -l logs ./run_mn.sh -b $IDIR $AOPTS $YEARMONTHDAY IP ${p} aq
done
for p in canarias tenerife grancanaria fuerteventura lanzarote lagomera lapalma elhierro; do
        [[ $EMI -eq 1 ]] && $JOBIFY -n img_emis_${p} -w1h -a es1 -c benchmark -i $IDIR -l logs ./run_mn.sh -b $IDIR $AOPTS $YEARMONTHDAY CAN ${p} emis
        [[ $AQ -eq 1 ]] && $JOBIFY -n img_aq_${p} -w1h -a es1 -c benchmark -i $IDIR -l logs ./run_mn.sh -b $IDIR $AOPTS $YEARMONTHDAY CAN ${p} aq
done

[[ $EMI -eq 1 ]] && $JOBIFY -n img_emis_and -w1h -a es1 -c benchmark -i $IDIR -l logs ./run_mn.sh -b $IDIR $AOPTS $YEARMONTHDAY AND and emis
[[ $AQ -eq 1 ]]  && $JOBIFY -n img_aq_and -w1h -a es1 -c benchmark -i $IDIR -l logs ./run_mn.sh -b $IDIR $AOPTS $YEARMONTHDAY AND and aq
[[ $EMI -eq 1 ]] && $JOBIFY -n img_emis_bcn -w1h -a es1 -c benchmark -i $IDIR -l logs ./run_mn.sh -b $IDIR $AOPTS $YEARMONTHDAY BCN bcn emis
[[ $AQ -eq 1 ]] && $JOBIFY -n img_aq_bcn -w1h -a es1 -c benchmark -i $IDIR -l logs ./run_mn.sh -b $IDIR $AOPTS $YEARMONTHDAY BCN bcn aq

