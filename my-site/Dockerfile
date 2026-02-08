FROM nginx:alpine

WORKDIR /usr/share/nginx/html

COPY ./index.html .

COPY ./default.conf /etc/nginx/conf.d/default.conf

RUN apk add --no-cache bash tzdata

COPY ./backup.sh /usr/local/bin/backup.sh

RUN chmod +x /usr/local/bin/backup.sh

ENV TZ=Europe/Kiev

