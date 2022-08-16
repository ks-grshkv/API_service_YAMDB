# api_yamdb
api_yamdb

### Описание проекта:

API для ресурса YAMDB. У нас есть:
Произведения, их категории и жанры, а также отзывы и оценки к ним.
Для регистрации пользователь получает код подтверждения на почту.


### Примеры запросов:

###
POST http://127.0.0.1:8000/api/v1/auth/signup/
Content-Type: application/json

{
    "email": "ex1@example.ex",
    "username": "ExampleUser1"
}

###
GET http://127.0.0.1:8000/api/v1/users/me
Content-Type: application/json
Authorization: Bearer (insert jwt token here)


Подробная документация проекта:
http://127.0.0.1:8000/redoc/

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/ks-grshkv/api_yamdb.git
```

```
cd yatube_api
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```