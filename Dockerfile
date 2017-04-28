FROM django-mod_wsgi-postgres

ENV PROJECT_NAME ecoroofs
ENV PROJECT_DIR /webapps/${PROJECT_NAME}
ENV SOURCE_DIR ${PROJECT_DIR}/src
ENV STATIC_SOURCE_DIR ${PROJECT_DIR}/src/${PROJECT_NAME}/static
ENV STATIC_ROOT ${PROJECT_DIR}/static
ENV VENV_DIR ${PROJECT_DIR}/venv
ENV LOCAL_SETTINGS_FILE ${SOURCE_DIR}/local.docker.cfg

ENV PATH $PATH:/usr/pgsql-9.4/bin
ENV PIP_CACHE_DIR /pip/cache
ENV PIP_WHEEL_DIR /pip/wheels
ENV PYTHONUNBUFFERED 1

RUN mkdir -p ${PROJECT_DIR}
ADD . ${PROJECT_DIR}/src

RUN adduser -M -d ${PROJECT_DIR} ${PROJECT_NAME}

WORKDIR ${SOURCE_DIR}
RUN ln -s local.docker.cfg local.cfg
RUN virtualenv -p python3.5 ${VENV_DIR}
RUN ${VENV_DIR}/bin/pip install wheel

# Build wheels
RUN ${VENV_DIR}/bin/pip wheel \
    --find-links https://pypi.research.pdx.edu/dist/ \
    git+https://github.com/PSU-OIT-ARC/arctasks#egg=psu.oit.arc.tasks \
    .

# Install from wheels
RUN ${VENV_DIR}/bin/pip install \
    --no-index \
    --find-links ${PIP_WHEEL_DIR} \
    psu.oit.wdt.ecoroofs

WORKDIR ${STATIC_SOURCE_DIR}
RUN npm install >/dev/null
RUN ./node_modules/.bin/node-sass -o . base.scss
RUN node build.js

WORKDIR ${SOURCE_DIR}
RUN ${VENV_DIR}/bin/python manage.py collectstatic --no-input >/dev/null
