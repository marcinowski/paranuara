#!/usr/bin/env bash

if [ "$(python -c 'import sys; print(sys.version_info[0])')" -lt 3 ]; then
    echo "Incompatible python version. Must be greater than 3."
    return 0
else
    echo "Compatible python version found"
fi
pwd
if [[ -e `dirname "$0"`/venv ]]; then
    echo "Virtualenv directory found."
else
    pip install virtualenv
    virtualenv venv
fi
source venv/Scripts/activate
pip install -r requirements.txt
mongo < mongo_setup.js
mongod --dbpath `dirname "$0"`/mongodb &
cd src
python manage.py populate_db
python manage.py runserver
