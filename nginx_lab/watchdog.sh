#!/bin/bash


SERVICE="nginx"
logfile="/home/user/nginx_lab/watchdog.log"

if systemctl is-active --quiet "$SERVICE"; then
	exit 0
else 
	echo "$(date): $SERVICE is down. Attempting to restart" >> $logfile
	systemctl start "$SERVICE"


	#test working or not
	if systemctl is-active --quiet "$SERVICE"; then
		echo "$(date): $SERVICE is restarted" >> $logfile
	else
		echo "$(date): $SERVICE is down. Cant start" >> $logfile
	fi
fi
