#!/bin/bash 

FIX=0
JOBIFY=/gpfs/projects/bsc32/share/bin/jobify.sh
WDIR="/gpfs/projects/bsc32/bsc32359/CMAQ-mat/FORECAST/AQ/IMG"

# Defaults class
CLASS=aq

usage(){
	echo -e "Usage: $(basename $0) [-c CLASS] [-f] [-w] [DATE]"
	echo -e "optional DATE parameter to specify a custom date, otherwise today"
	echo -e "\t-c: CLASS argument to choose in 'aq' or 'emis'"
	echo -e "\t-f: fix missing images (launches a job on MN)"
	echo -e "\t-w: use current directory as base dir" 
}

while getopts "c:fw" opt; do 
	case $opt in 
		c) 
		  echo "Using class ${OPTARG}"
		  CLASS=${OPTARG}
		  ;;
		f) 
		  echo "Will fix missing images"
		  FIX=1
		  ;;
		w)
		  echo "Using current dir $PWD as work dir"
		  WDIR=$PWD 
		  ;;
		\?)
		  usage
	          exit 1
		  ;;
	esac
done 		
shift $((OPTIND-1))

OUTDIRBASE="$WDIR/out/"
DATE=$1

exitError(){
	echo $1 2>&1 
	exit 1        
}

[[ -z $DATE ]] && DATE=$(date +%Y%m%d)

OUTDIR=$OUTDIRBASE/$DATE/${CLASS}

[[ -d $OUTDIR ]] || exitError "Directory $OUTDIR does not exist"

domains=( eu ip and can bcn )

case ${CLASS} in
  emis) 
	contaminants=( NO NO2 SO2 PM CO VOCs )
	pre="BSC-ES_EMISSIONS_"
	;;
  aq)
	contaminants=( O3 NOx CO SO2 PM10_DUST )
	pre="BSC-ES_FORECAST_"
	;;
esac

echo date: $DATE
for d in ${domains[*]}; do 
	case $d in
		eu)
			subdomains=( eu )
			;;
		ip)	
			subdomains=( andalucia asturias cantabria castillaleon  extremadura ip madrid navarra valencia \
				aragon baleares castillalamancha catalunya galicia larioja murcia paisvasco)
			;;
		can)
			subdomains=( canarias  elhierro  fuerteventura  grancanaria  lagomera  lanzarote  lapalma  tenerife )
			;;
		and)
			subdomains=( and )
			;;
		bcn)
			subdomains=( bcn )
			;;
			
	esac

	for s in ${subdomains[*]}; do
		for c in ${contaminants[*]}; do 
			COUNT=$(ls -1 $OUTDIR/$d/$s/${pre}${c}_*[0-9][0-9].gif 2>/dev/null| wc -l )
			if [[ $COUNT -ne 49 || ! -f $OUTDIR/$d/$s/${pre}${c}_ANIM.gif ]] ; then 
				[[ ! -f $OUTDIR/$d/$s/${pre}${c}_ANIM.gif ]] && echo "No anim $OUTDIR/$d/$s/${pre}${c}_ANIM.gif" 
				[[ $COUNT -ne 49 ]] && echo "Images for ${CLASS}/$d/$s/$c ($COUNT): error!"
				FDOM=( ${FDOM[@]} $(echo $d | tr [a-z] [A-Z]) )
				FSUB=( ${FSUB[@]} $(echo $s | tr [A-Z] [a-z]) )
				FCON=( ${FCON[@]} $(echo $c | tr [a-z] [A-Z]) ) 
			else 
				echo "Images for ${CLASS}/$d/$s/$c ($COUNT): OK"
			fi
		done 
	done 
done 

echo "***** REPORT *****" 
echo "${#FDOM[@]} packs with issues"
echo "domains = ${FDOM[@]}"
echo "subdoms = ${FSUB[@]}"
echo "conts   = ${FCON[@]}"

if [[ $FIX -eq 1 ]]; then
	for c in $(seq 0 $(( ${#FDOM[@]} - 1 )) ); do 
		echo "Launching job for ${FDOM[$c]}/${FCON[$c]}/${FSUB[$c]}"
		mkdir ${WDIR}/logs/${DATE} 2>/dev/null
		#Patch to fix NOX -> NOx  VOCS -> VOCs
		[[ "${FCON[$c]}" == "NOX" ]]  && FCON[$c]="NOx"
		[[ "${FCON[$c]}" == "VOCS" ]] && FCON[$c]="VOCs"
		$JOBIFY -n im_${CLASS}_${FSUB[$c]}_${FCON[$c]}_fix -i ${WDIR} -l logs/${DATE} -w1h ./run_mn.sh -b ${WDIR} -S ${FCON[$c]} $DATE ${FDOM[$c]} ${FSUB[$c]} ${CLASS}
	done 
fi
