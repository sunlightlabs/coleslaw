#!/bin/sh

DBNAME=coleslaw
DBUSER=django_dev

sudo su postgres -c "dropdb $DBNAME"
sudo su postgres -c "createdb -E utf8 -O $DBUSER $DBNAME"
python manage.py syncdb 
