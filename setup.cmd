@ECHO OFF
echo Starting MongoDB server
REM I do it before anything else so it's ready when needed
start /B /HIGH mongod --dbpath %~dp0\mongodb
timeout /t 20 /nobreak > nul
REM Giving db some time to setup.
cd %~dp0
IF NOT EXIST %~dp0\venv (
    echo Virtualenv directory not found.
    pip install virtualenv 1> nul
    echo Setting up venv.
    virtualenv venv
) ELSE (
    echo Virtualenv directory found.
)
echo Activating virtualenv.
call venv\Scripts\activate.bat
echo Installing requirements.
pip install -r requirements.txt
echo Setting up mongoDB
mongo < mongo_setup.js
echo Populating database
python src\manage.py populate_db
echo Runserver on port 8000
python src\manage.py runserver
