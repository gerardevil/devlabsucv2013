#!/usr/bin/sh
# Scrtipt to collect django static files together.
#
# --link    Create a symbolic link to each file instead of copying.
# --noinput Do NOT prompt the user for input of any kind.

echo "###################################"
echo "# Actualizando repositporio local #"
echo "###################################"
git pull
echo "####################################"
echo "# Sincronizando Archivos estaticos #"
echo "####################################"
python2.7 ../../manage.py collectstatic -link
echo "######################################"
echo "# Todo bien (:  [Deployment Finised] #"
echo "######################################"
exit 0