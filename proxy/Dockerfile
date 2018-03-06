FROM nginx:mainline-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/
COPY ./geoserver /etc/nginx/conf.d/geoserver.conf
