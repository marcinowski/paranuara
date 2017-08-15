#!/usr/bin/env bash
cd `dirname "$0"`
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
    echo "Virtualenv directory not found."
    pip install virtualenv
    echo "Setting up venv"
    virtualenv venv
fi
echo "Activating venv"
source venv/bin/activate
echo "Installing requirements."
pip install -r requirements.txt
echo "Setting up mongoDB"
mongo < mongo_setup.js
mongod --dbpath `dirname "$0"`/mongodb &
cd src
echo "Populating database"
python manage.py populate_db
echo "Runserver on port 8000"
python manage.py runserver
