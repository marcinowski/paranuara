#!/usr/bin/env bash

1. mkdir etc.
2. virtualenv & source '' & cd src/
pip install -r requirements.txt
mongo < mongo_setup.js
mongod --dbpath $pwd/mongodb
cd src
python manage.py populate_db
python manage.py runserver
