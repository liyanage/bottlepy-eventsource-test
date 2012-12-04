#!/bin/sh


server_type=$1

if [ -z $server_type ]; then
	echo Usage: $0 'server_name'
	echo Server name is one of wsgiref, paste, rocket, waitress, cherrypy
	exit 1
fi

echo server type: $server_type

PYTHONPATH=lib/Rocket-1.2.4:lib/waitress-master:lib/CherryPy-3.2.2:lib/Paste-1.7.5.1:lib/bottle-master ./generatortest.py $server_type



