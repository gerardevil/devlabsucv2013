#!/usr/bin/sh
# Scrtipt to collect django static files together.
#
# --link    Create a symbolic link to each file instead of copying.
# --noinput Do NOT prompt the user for input of any kind.

echo "---------------"
echo "- Apache STOP -"
echo "---------------"
./../../../apache2/bin/stop

echo "---------------------------"
echo "- Update local repository -"
echo "---------------------------"
git pull
echo "--------------------------"
echo " Syncronize Static Files -"
echo "--------------------------"
python2.7 ../../manage.py collectstatic -link

echo "----------------"
echo "- Apache START -"
echo "----------------"
./../../../apache2/bin/start


echo "-------------------------------"
echo "- OK (:  [Deployment Finised] -"
echo "-------------------------------"

exit 0