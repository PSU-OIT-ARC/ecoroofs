from runcommands import command
from runcommands.util import abort, abs_path, args_to_str, printer

from emcee.commands import *
from emcee.commands.deploy import deploy

from emcee.backends.dev.db import provision_database as provision_database_local
from emcee.backends.aws.provision.python import provision_python
from emcee.backends.aws.provision.gis import provision_gis
from emcee.backends.aws.provision.services.local import provision_nginx
from emcee.backends.aws.provision.services.remote import provision_database
from emcee.backends.aws.deploy import AWSDjangoDeployer
from emcee.backends.aws.infrastructure.commands import *


@command(env='dev', timed=True)
def init(config, overwrite=False, drop_db=False):
    virtualenv(config, overwrite=overwrite)
    install(config)
    npm_install(config, where='{package}:static', modules=[])
    # provision_database_local(config, drop=drop_db, with_postgis=True)
    manage(config, 'migrate --no-input')
    sass(config)
    # test(config, force_env='test')


@command
def deploy_app(config, provision=False, createdb=False):
    if provision:
        provision_python(config)
        provision_gis(config)
        provision_nginx(config)
    if createdb:
        provision_database(config, with_postgis=True,
                           extensions=['postgis', 'hstore'])

    deploy(config, deployer_class=AWSDjangoDeployer)
