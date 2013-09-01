#!/usr/bin/sh
# Scrtipt to collect django static files together.
#
# --link    Create a symbolic link to each file instead of copying.
# --noinput Do NOT prompt the user for input of any kind.
#
python manage.py collectstatic -link
exit 0