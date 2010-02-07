#!/bin/bash

source scripts/config_local.sh

# src dir
SRC=$V_ENV/src
# find last python dir
for i in $V_ENV/lib/python*
do
	SITE_PACKAGES=$i/site-packages
done

### PIP packages installation
export PYTHONPATH=
pip install -E $V_ENV/ -r $PROJECT_DIR/tools/pip-requirements.txt
# TODO: write a proper bash script which will install from configurable files

### Grappelli section
# checkout the repository
svn checkout -r 680 http://django-grappelli.googlecode.com/svn/trunk/grappelli/ $SRC/grappelli
# link to site-packages
if [ ! -e $SITE_PACKAGES/grappelli ]
then
	ln -fs $SRC/grappelli $SITE_PACKAGES/grappelli
fi
# link adminmedia within project
if [ ! -e $PROJECT_DIR/$PROJECT_NAME/adminmedia ]
then
	ln -fs $SRC/grappelli/media $PROJECT_DIR/$PROJECT_NAME/adminmedia
fi
