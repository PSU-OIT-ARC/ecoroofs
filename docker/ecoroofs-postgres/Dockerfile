FROM centos:7

ENV LANG en_US.utf8
ENV PATH /usr/pgsql-9.4/bin:$PATH
ENV PGDATA /var/lib/pgsql/9.4/data
ENV PGUSER postgres

# XXX: Not sure what these do
ENV DBUSER dbuser
ENV DBNAME dbname

RUN mv /etc/localtime /etc/localtime.orig
RUN ln -s /usr/share/zoneinfo/America/Los_Angeles /etc/localtime

RUN yum update -y
RUN yum upgrade -y
RUN yum install -y epel-release
RUN yum localinstall -y https://download.postgresql.org/pub/repos/yum/9.4/redhat/rhel-7-x86_64/pgdg-centos94-9.4-3.noarch.rpm

RUN yum install -y postgresql94
RUN yum install -y postgresql94-contrib
RUN yum install -y postgresql94-libs
RUN yum install -y postgresql94-server
RUN yum install -y postgis2_94
RUN yum install -y postgis2_94-client

RUN yum clean all

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./initdb.sh /docker-entrypoint-initdb.d

ENTRYPOINT ["/docker-entrypoint-initdb.d/initdb.sh"]
CMD ["postgres"]
