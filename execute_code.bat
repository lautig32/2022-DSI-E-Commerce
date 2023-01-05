echo 'Activate enviroment'
. venv/bin/activate

echo 'Makemigrations create data base and create migrations'
python manage.py makemigrations

echo 'Migrate migrations to data base'
python manage.py migrate

echo 'Open url'
open http://127.0.0.1:8000/

echo 'Runserver to execute code'
python manage.py runserver