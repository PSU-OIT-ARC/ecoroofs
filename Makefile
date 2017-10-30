package = ecoroofs
venv ?= .env
venv_python ?= python3
bin = $(venv)/bin


local.dev.cfg:
	echo '[dev]' >> $@
	echo 'extends = "local.base.cfg"' >> $@

local.docker.cfg:
	echo '[docker]' >> $@
	echo 'extends = "local.base.cfg"' >> $@

local.test.cfg:
	echo '[test]' >> $@
	echo 'extends = "local.base.cfg"' >> $@

venv: $(venv)
$(venv):
	$(venv_python) -m venv $(venv)

install: $(venv)
	$(venv)/bin/pip install -r requirements.txt

init: install local.dev.cfg local.test.cfg
	$(bin)/runcommand init
reinit: clean-egg-info clean-pyc clean-venv init

test:
	$(bin)/runcommand test

run:
	$(bin)/runcommand runserver

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

.PHONY = init reinit docker-externals docker-init test run run-docker run-services deploy \
         clean clean-all clean-build clean-dist clean-egg-info clean-node_modules clean-pyc \
         clean-static clean-venv
