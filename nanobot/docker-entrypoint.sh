#!/bin/bash
set -e

# If running as root, exec as nonroot user
if [ "$(id -u)" = "0" ]; then
    exec gosu nonroot "$@"
fi

# Otherwise just run the command
exec "$@"
