#! /bin/bash
export PYTHONUNBUFFERED=TRUE
WORKERS=3
# This is a concurrent server
exec gunicorn api \
     -w $WORKERS \
     -b 0.0.0.0:5001 \
     --timeout 1800 \
     --log-file "-"
     --enable-stdio-inheritance \
     --reload \
     --log-level "debug"