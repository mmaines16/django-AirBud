cd /var/www/airbud
sudo rm db.sqlite3.backup
sudo mv db.sqlite3 db.sqlite3.backup
cd settings 
sudo rm -rf migrations/
sudo rm -rf __pycache__
sudo mv admin.py admin_temp.py
sudo mv forms.py forms_temp.py
sudo rm admin.pyc
sudo rm forms.pyc
cd ..
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations settings
python manage.py migrate settings
cd settings
sudo mv admin_temp.py admin.py
sudo mv forms_temp.py forms.py
cd ..
python manage.py createsuperuser
