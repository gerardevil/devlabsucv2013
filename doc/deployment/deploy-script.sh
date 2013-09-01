#!/usr/bin/sh
# Scrtipt to collect django static files together.
#
# --link    Create a symbolic link to each file instead of copying.
# --noinput Do NOT prompt the user for input of any kind.
#
echo "Actualizando repositporio local"
git pull
echo "Sincronizando Archivos estaticos"
python2.7 ../manage.py collectstatic -link
echo "Todo bien (:  [Deplot Finised]"
exit 0