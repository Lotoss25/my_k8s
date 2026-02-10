#!/bin/bash


BACKUP_FILE=./backups/$(ls -th ./backups | head -1)

read -p "Are you really want to restore? (y/n)" ANSWER

if [[ "$ANSWER" == "y" || "$ANSWER" == "yes" ]]; then
  echo "Restoring... $BACKUP_FILE..."
  cat $BACKUP_FILE | docker exec -i my-site-web-1 tar -xvzf - -C /usr/share/nginx/html
else
  echo "Ok, dont restore ;)"
fi
