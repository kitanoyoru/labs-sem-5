#!/bin/sh

set -e

# activate our virtual environment here
. /opt/pysetup/.venv/bin/activate

python3 -m src reset-db

# Evaluating passed command:
exec "$@"
