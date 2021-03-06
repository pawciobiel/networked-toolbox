Network Toolbox
===============


admin
=====
Only admin users can add, edit pages, tools etc.


development
===========
Install postgres database, redis-server and elasticsearch
or use the one from heroku by exporting environment variables.

(No spaces in project path)

```
virtualenv -p python3 .venv
. .venv/bin/activate
pip install -r requirements.txt
npm install
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

Subsequent runs:

```
. .venv/bin/activate && ./manage.py migrate && ./manage.py runserver
```

# Setting up the development environment to support task execution

## Get a celery supported broker (in this case Redis)

For ubuntu install the redis-server package

```
sudo apt-get install redis-server
```

On mac
```
brew install redis
```


And on a new terminal:

```
celery -A netbox worker --concurrency=1 -l debug --purge
```

# Load some test data into the database

## Pages

```
./manage.py loaddata pages/fixtures/test-pages.json
```

## Menus

```
./manage.py loaddata menus/fixtures/initial-menus.json
```
