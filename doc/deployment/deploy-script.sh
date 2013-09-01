#!/usr/bin/sh
# Scrtipt to collect django static files together.
#
# --link    Create a symbolic link to each file instead of copying.
# --noinput Do NOT prompt the user for input of any kind.

echo "-------------------"
echo "- Apache a dormir -"
echo "-------------------"
./../../../apache2/bin/stop

echo "-----------------------------------"
echo "- Actualizando repositporio local -"
echo "-----------------------------------"
git pull
echo "------------------------------------"
echo "- Sincronizando Archivos estaticos -"
echo "------------------------------------"
python2.7 ../../manage.py collectstatic -link
echo "--------------------------------------"
echo "- Todo bien (:  [Deployment Finised] -"
echo "--------------------------------------"

echo "--------------------"
echo "- Apache despierta -"
echo "--------------------"
./../../../apache2/bin/start
exit 0