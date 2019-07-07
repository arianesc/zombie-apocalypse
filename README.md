# zombie-apocalypse

## Setup enviroment
* Create virtual enviroment

```
    $ python3 -m venv my_env
```
* activate venv

```
    $ source my_env/bin/activate
```
* Install dependencies

```
    $ pip install -r requirements.txt
```

## Running API
### Migrations
* Execute migrations

```
    $ python manage.py makemigrantions

    $ python manage.py migrate
```

### Running Server
```
    $ python manage.py runserver
```
## Create surviver with httpie
* To create surviver you should with enviroment loaded and server running
```
    $ http --json POST http://127.0.0.1:8000/api/survivers/create name=tux age:=4 gender=male latitude=121212 longitude=121212 food:=11 water:=2 ammunition:=2 medication:=2
```

## Update surviver location with httpie
* To update surviver location you should load your enviroment and your server should be running
```
    $ http --json PUT http://127.0.0.1:8000/api/survivers/update_location/id_surviver/ latitude=121212 longitude=121212 
```
## Relate infected surviver with httpie
* To relate infected surviver you should load your enviroment and your server should be running
```
    $ http --json PUT http://127.0.0.1:8000/api/survivers/relate_infected/id_surviver/ infected:=1
```
