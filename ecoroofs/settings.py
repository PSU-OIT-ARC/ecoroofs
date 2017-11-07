from arcutils.settings import init_settings
from emcee.aws.processors import (set_secret_key,
                                  set_database_parameters)


init_settings(settings_processors=[set_secret_key,
                                   set_database_parameters])
