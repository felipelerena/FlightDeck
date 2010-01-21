#!/bin/bash

# copy configuration files to local 
for loc in flightdeck/*_local-default.py
do
	cp $loc flightdeck/`basename $loc "-default.py"`.py
	echo $loc "->" flightdeck/`basename $loc "-default.py"`.py
done

for wsgi in apache/*_local-default.wsgi
do
	cp $wsgi apache/`basename $wsgi "-default.wsgi"`.wsgi
	echo $wsgi "->" apache/`basename $wsgi "-default.wsgi"`.wsgi
done

for sh in scripts/*_local-default.sh
do
	cp $sh scripts/`basename $sh "-default.sh"`.sh
	echo $sh "->" scripts/`basename $sh "-default.sh"`.sh
done

# force exclude local files
cp tools/git-exclude .git/info/exclude
echo tools/git-exclude "->" .git/info/exclude
