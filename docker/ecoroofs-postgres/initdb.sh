#!/bin/bash
set -e

if [ "${1:0:1}" = "-" ]; then
    set -- postgres "$@"
fi

# This will only be run if a non-postgres COMMAND is passed to Docker.
if [ "$1" != "postgres" ]; then
    # Run some other command if indicated.
    exec "$@"
fi

mkdir -p "$PGDATA"

if [ ! -s "$PGDATA/PG_VERSION" ]; then
    su $PGUSER -c initdb

    # Don't require passwords.
    echo >> "$PGDATA/pg_hba.conf"
    echo "host all all 0.0.0.0/0 trust" >> "$PGDATA/pg_hba.conf"

    # Replaces the default `listen_addresses = 'localhost'` with
    # `listen_addresses = '*'` to allow connections from outside the
    # container.
    sed -ri "s!^#?(listen_addresses)\s*=\s*\S+.*!\1 = '*'!" "$PGDATA/postgresql.conf"
fi

chmod 700 "$PGDATA"
chown -R $PGUSER "$PGDATA"

# Run postgres.
exec su $PGUSER -c "$@"
