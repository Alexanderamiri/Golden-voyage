task=()
timeittok=()
ranonce=0
started=0
runningtask=""
track() {
touch LOGFILE.txt
if [[ "$1"=="start" ]] && [[ $started -eq 0 ]] && [[ $# -eq 2 ]]; then
runningtask=$2
SECONDS=0
started=1
task+=("$2")
echo "START $(date)" >> LOGFILE
echo "LABEL $2" >> LOGFILE
ranonce=$(($ranonce + 1))
elif [[ $1=="stop" ]] && [[ $started -eq 1 ]] && [[ $# -eq 1 ]] ; then
started=0
runningtask=""
duration=$SECONDS
timeittok+=($duration)
echo -e "STOP $(date)\n" >> LOGFILE
elif [[ "$1"=="status" ]] && [[ $# -eq 1 ]]; then
echo "The tracker status is currently runstatus=$started"
echo "Current tracking task is > $runningtask (empty if no task is being tracket)"	
else 
	echo "To start tracking write track start <taskname>"
	echo "Stop other trackers by writing track stop"
	echo "You cannot stop a tracker unless one has started"
fi
}
log(){ 
	if [[ $ranonce -ge 1 ]]; then
		for ((i=0 ; i < $ranonce ; i++)); do
			printf "TASK ${task[$i]}:  "
			TZ=UTC0 printf '%(%H:%M:%S)T\n' "${timeittok[$i]}"
		done
		fi
}
log
