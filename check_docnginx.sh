#!/bin/bash

CONTAINER=$(docker ps --filter "name=nginx" --format "{{.Names}}")
LOGFILE="/var/log/check_nginx.log"
#echo $CONTAINER
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOGFILE
}
if [ -z $CONTAINER ]; then
  docker run -d --name nginx nginx:latest
  log_message "Container nginx started"
else
  log_message "Container nginx is running"
fi
