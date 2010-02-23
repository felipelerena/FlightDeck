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

### link jetpack application 
if [ ! -e $PROJECT_DIR/$PROJECT_NAME/media/jetpack ]
then
	ln -fs $PROJECT_DIR/$PROJECT_NAME/jetpack/media/ $PROJECT_DIR/$PROJECT_NAME/media/jetpack
fi

### adminmedia dir
if [ ! -e $PROJECT_DIR/$PROJECT_NAME/adminmedia ]
then
	ln -fs $SITE_PACKAGES/django/contrib/admin/media/ $PROJECT_NAME/adminmedia
fi


### Roar
cd $V_ENV/lib/
if [ ! -e $V_ENV/lib/Roar1.0 ]
then 
	mkdir Roar1.0
	cd Roar1.0
	wget http://digitarald.de/project/roar/1-0/source/Roar.js
	wget http://digitarald.de/project/roar/1-0/assets/Roar.css
	rm $V_ENV/lib/Roar
	ln -fs $V_ENV/lib/Roar1.0 $V_ENV/lib/Roar
fi
if [ ! -e $PROJECT_DIR/$PROJECT_NAME/media/roar ]
then
	ln -fs $V_ENV/lib/Roar/ $PROJECT_DIR/$PROJECT_NAME/media/roar
fi


### Bespin installation
cd $V_ENV/lib/
if [ ! -e $V_ENV/lib/BespinEmbedded-0.6.1 ]
then
	wget http://ftp.mozilla.org/pub/mozilla.org/labs/bespin/Embedded/BespinEmbedded-DropIn-0.6.1.tar.gz --no-check-certificate
	tar xfvz BespinEmbedded-DropIn-0.6.1.tar.gz
	rm BespinEmbedded-DropIn-0.6.1.tar.gz
	rm $V_ENV/lib/BespinEmbedded
	ln -fs $V_ENV/lib/BespinEmbedded-DropIn-0.6.1/ $V_ENV/lib/BespinEmbedded
	rm $PROJECT_DIR/$PROJECT_NAME/media/bespin
fi
if [ ! -e $PROJECT_DIR/$PROJECT_NAME/media/bespin ]
then
	ln -fs $V_ENV/lib/BespinEmbedded/ $PROJECT_DIR/$PROJECT_NAME/media/bespin
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
