#!/bin/bash


CURR_TIME=$(date +%Y-%m-%d)

SOURCE=./
DEST=./backup/$CURR_TIME.tar.gz

mkdir -p ./backup

tar -czf "$DEST" "$SOURCE" && echo "Backup completed successfully"

find ./backup -mtime +7 -delete

