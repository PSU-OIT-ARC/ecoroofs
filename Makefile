package := ecoroofs
venv ?= .env
venv_python ?= python3.5
bin = $(venv)/bin
arctasks = $(venv)/lib/$(venv_python)/site-packages/arctasks/__init__.py

# The init task creates a temporary virtualenv with arctasks installed
# for bootstrapping purposes and then delegates to the arctasks init
# task to do the actual initialization.
init: $(venv) local.dev.cfg local.test.cfg $(arctasks)
	$(bin)/inv init --overwrite
	$(bin)/inv test

reinit: clean-egg-info clean-pyc clean-venv init

$(arctasks):
	$(bin)/pip install git+https://github.com/PSU-OIT-ARC/arctasks#egg=psu.oit.arc.tasks

local.dev.cfg:
	echo '[dev]' >> $@
	echo 'extends = "local.base.cfg"' >> $@

local.test.cfg:
	echo '[test]' >> $@
	echo 'extends = "local.base.cfg"' >> $@

$(venv):
	virtualenv -p $(venv_python) $(venv)
clean-venv:
	rm -rf $(venv)

test:
	$(bin)/inv test

run:
	$(bin)/inv runserver

to ?= stage
deploy:
	$(bin)/inv --echo configure --env $(to) deploy

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

.PHONY = init reinit test run deploy \
         clean clean-all clean-build clean-dist clean-egg-info clean-node_modules clean-pyc \
         clean-static clean-venv
