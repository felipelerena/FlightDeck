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

### flightdeck media dir 
if [ ! -e $PROJECT_DIR/$PROJECT_NAME/media/ ]
then
	mkdir $PROJECT_DIR/$PROJECT_NAME/media/
fi

### Bespin installation
cd $V_ENV/lib/
if [ ! -e $V_ENV/lib/BespinEmbedded-0.5.2 ]
then
	wget http://ftp.mozilla.org/pub/mozilla.org/labs/bespin/Embedded/BespinEmbedded-0.5.2.tar.gz
	tar xfz BespinEmbedded-0.5.2.tar.gz
	rm BespinEmbedded-0.5.2.tar.gz
fi
if [ ! -e $V_ENV/lib/BespinEmbedded ]
then
	ln -fs $V_ENV/lib/BespinEmbedded-0.5.2/ $V_ENV/lib/BespinEmbedded
fi
if [ ! -e $PROJECT_DIR/$PROJECT_NAME/media/bespin ]
then
	ln -fs $V_ENV/lib/BespinEmbedded/ $PROJECT_DIR/$PROJECT_NAME/media/bespin
fi

### link jetpack application 
if [ ! -e $PROJECT_DIR/$PROJECT_NAME/media/jetpack ]
then
	ln -fs $PROJECT_DIR/$PROJECT_NAME/jetpack/media/ $PROJECT_DIR/$PROJECT_NAME/media/jetpack
fi

### Grappelli section
# checkout the repository
# TODO: wait with grappelli for the newer Django
#svn checkout http://django-grappelli.googlecode.com/svn/trunk/grappelli/ $SRC/django-grappelli
# link to site-packages
#if [ ! -e $SITE_PACKAGES/grappelli ]
#then
#	ln -fs $SRC/django-grappelli $SITE_PACKAGES/grappelli
#fi
# link adminmedia within project
#if [ ! -e $PROJECT_DIR/$PROJECT_NAME/adminmedia ]
#then
#	ln -fs $SRC/grappelli/media $PROJECT_DIR/$PROJECT_NAME/adminmedia
#fi
