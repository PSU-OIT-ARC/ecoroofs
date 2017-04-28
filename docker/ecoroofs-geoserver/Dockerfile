FROM centos:7

ENV LANG en_US.utf8

ENV JAVA_VERSION 1.7.0
ENV JAVA_HOME /usr/lib/jvm/jre-${JAVA_VERSION}

ENV GEOSERVER_VERSION 2.7.1.1
ENV GEOSERVER_DOWNLOAD_URL https://cdn.research.pdx.edu/geoserver/geoserver-${GEOSERVER_VERSION}-bin.zip
ENV GEOSERVER_DOWNLOAD_PATH /tmp/geoserver-${GEOSERVER_VERSION}-bin.zip
ENV GEOSERVER_INSTALL_DIR /opt/geoserver-${GEOSERVER_VERSION}
ENV GEOSERVER_HOME ${GEOSERVER_INSTALL_DIR}
ENV GEOSERVER_DATA_DIR /var/geoserver/data

RUN mv /etc/localtime /etc/localtime.orig
RUN ln -s /usr/share/zoneinfo/America/Los_Angeles /etc/localtime

RUN yum update -y
RUN yum upgrade -y
RUN yum install -y epel-release

RUN yum install -y curl
RUN yum install -y httpd
RUN yum install -y java-${JAVA_VERSION}-openjdk
RUN yum install -y unzip

RUN rm /etc/httpd/conf.d/*
COPY etc/httpd/vhost.d/geoserver.conf /etc/httpd/conf.d/00-geoserver.conf

RUN adduser -M -s /bin/bash geoserver
RUN test -d ${GEOSERVER_DOWNLOAD_PATH} || curl -L -o ${GEOSERVER_DOWNLOAD_PATH} ${GEOSERVER_DOWNLOAD_URL}
RUN rm -rf ${GEOSERVER_INSTALL_DIR}
RUN unzip -d /opt ${GEOSERVER_DOWNLOAD_PATH}
RUN chown -R geoserver ${GEOSERVER_INSTALL_DIR}
RUN ls -l /opt
RUN ls -l ${GEOSERVER_INSTALL_DIR}

COPY entrypoint.sh /usr/local/bin
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
