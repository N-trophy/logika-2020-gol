# N-trophy 2020 qualification task web

Game of Life

## How to run server for development

```
$ cp gol/settings/development.py.txt gol/settings/development.py
Edit gol/settings/development.py as you wish.
$ virtualenv -p python3 djangoenv
$ source djangoenv/bin/activate
$ pip3 install -r requirements.txt
$ ./manage.py collectstatic --settings=gol.settings.development
$ ./manage.py runserver --settings=gol.settings.development
```

## How to deploy to production

```
$ cp gol/settings/production.py.txt gol/settings/production.py
Edit gol/settings/development.py as you wish.
$ ./manage.py collectstatic --settings=gol.settings.production
```

## How to create db structure

```
$ ./manage.py migrate --settings=gol.settings.development
$ ./manage.py makemigrations gol --settings=gol.settings.development
$ ./manage.py migrate gol --settings=gol.settings.development
```
