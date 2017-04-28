#!/bin/bash
/usr/sbin/httpd
exec /opt/geoserver-${GEOSERVER_VERSION}/bin/startup.sh
