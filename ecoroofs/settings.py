from arcutils.settings import init_settings
from emcee.backends.aws import processors


init_settings(settings_processors=[processors.set_secret_key,
                                   processors.set_sentry_dsn,
                                   processors.set_database_parameters])
