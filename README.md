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
    python manage.py runserver
```
