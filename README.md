
DAILY ILLINI CRIME MAP
![alt tag](http://i.imgur.com/BsbcrNW.png)

Django app for tracking Clery-reported crime around the UIUC campus

create a python virtualenv named "crimemap"

pip install -r requirements.txt

just one quick import script so far, not yet automated. 

But for now,
createdb crimemap -T template_postgis -O crimemap

cd into crimemap/

run 'python manage.py syncdb'
run 'python manage.py import1'

