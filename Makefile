venv ?= .env
venv_python ?= python3.5
bin = $(venv)/bin
site_packages = $(venv)/lib/$(venv_python)/site-packages

arctasks = $(site_packages)/arctasks
arctasks_url = https://github.com/PSU-OIT-ARC/arctasks/archive/master.tar.gz#egg=psu.oit.arc.tasks

# The init task creates a temporary virtualenv with arctasks installed
# for bootstrapping purposes and then delegates to the arctasks init
# task to do the actual initialization.
init: $(venv) local.dev.cfg local.test.cfg $(arctasks)
	$(bin)/runcommand init

reinit: clean-egg-info clean-pyc clean-venv init

docker-init: local.docker.cfg
	@if ! which docker >/dev/null; then \
	    echo "docker is not installed or not on PATH" >&2; \
	    exit 1; \
	fi

	@if ! which docker-compose >/dev/null; then \
	    echo "docker-compose is not installed or not on PATH" >&2; \
	    exit 1; \
	fi

	@printf "If this is the first time you're running 'docker-init', it may take a while.\n"

	@read -n 1 -t 10 \
	    -p "Continuing in 10 seconds. Hit N to abort or any other key to continue now... "; \
	    if [ "$${REPLY}" != "n" ] && [ "$${REPLY}" != "N" ]; then \
	        echo; \
	        docker-compose build; \
	    else \
	        printf "\nAborted\n"; \
	        exit 0; \
	    fi

install-arctasks: $(arctasks)

$(arctasks):
	$(bin)/pip install -f https://pypi.research.pdx.edu/dist/ $(arctasks_url)

local.dev.cfg:
	echo '[dev]' >> $@
	echo 'extends = "local.base.cfg"' >> $@

local.docker.cfg:
	echo '[docker]' >> $@
	echo 'extends = "local.base.cfg"' >> $@

local.test.cfg:
	echo '[test]' >> $@
	echo 'extends = "local.base.cfg"' >> $@

$(venv):
	virtualenv -p $(venv_python) $(venv)

test:
	$(bin)/runcommand test

run:
	$(bin)/runcommand runserver

run-docker: docker-init
	@echo "NOTE: It may take a minute or so for all the Docker services to come up." 1>&2
	@echo "NOTE: GeoServer is especially slow." 1>&2
	docker-compose up

to ?= stage
deploy:
	$(bin)/runcommand --echo --env $(to) deploy

clean: clean-pyc
clean-all: clean-build clean-dist clean-egg-info clean-node_modules clean-pyc clean-static clean-venv
clean-build:
	rm -rf build
clean-dist:
	rm -rf dist
clean-egg-info:
	rm -rf *.egg-info
clean-node_modules:
	rm -rf $(package)/static/node_modules
clean-pyc:
	find . -name __pycache__ -type d -print0 | xargs -0 rm -r
	find . -name '*.py[co]' -type f -print0 | xargs -0 rm
clean-static:
	rm -rf static
	rm -rf $(package)/static/bundles
	find $(package)/static -name '*.css' -type f -print0 | xargs -0 rm
clean-venv:
	rm -rf $(venv)

.PHONY = init reinit docker-init test run run-docker deploy \
         clean clean-all clean-build clean-dist clean-egg-info clean-node_modules clean-pyc \
         clean-static clean-venv
