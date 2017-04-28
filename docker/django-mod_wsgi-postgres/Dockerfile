FROM centos:7

ENV LANG en_US.utf8

ENV PATH $PATH:/usr/pgsql-9.4/bin

RUN mv /etc/localtime /etc/localtime.orig
RUN ln -s /usr/share/zoneinfo/America/Los_Angeles /etc/localtime

RUN sed -i -E 's#(\[(base|updates)\])#\1\nexclude=postgresql*#g' /etc/yum.repos.d/CentOS-Base.repo

RUN yum update -y
RUN yum upgrade -y

RUN yum install -y epel-release
RUN yum localinstall -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum localinstall -y https://download.postgresql.org/pub/repos/yum/9.4/redhat/rhel-7-x86_64/pgdg-centos94-9.4-3.noarch.rpm
RUN curl --silent --location https://rpm.nodesource.com/setup_7.x | bash -

RUN yum groupinstall -y 'Development Tools'
RUN yum install -y \
    gdal \
    geos \
    git \
    httpd \
    httpd-devel \
    nodejs \
    postgresql94 \
    postgresql94-devel \
    postgresql94-libs \
    proj \
    python35u \
    python35u-devel \
    python35u-mod_wsgi \
    which

RUN yum clean all

RUN /usr/bin/python3.5 -m ensurepip
RUN /usr/bin/pip3 install -U setuptools pip virtualenv mod_wsgi
