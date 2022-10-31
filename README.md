# api_yamdb

[EN] API service similar to IMDB. Authorised sers can leave reviews for movies, books
and music, and rate them accordingly. Pieces are sorted by genres and categories.

[RU] Сервис API, аналогичный IMDB. Авторизованные пользователи могут оставлять отзывы о фильмах, книгах
и музыку, а также оценивать их. Произведения отсортированы по жанрам и категориям.


### Project Description / Описание проекта:

[EN] In order to sign up, the user sends a request with their email and desired username.
If the email and username are successfully validated, the user receives a confirmation code by email.
Then, after sending a request with a username and a confirmation code, the user receives their own JWT token, with which
they can leave reviews, rate pieces or edit their bio.

Team project contributors:
- ks_grshkv (teamlead, developer)
- nata_shepina (developer)
- SmileHorn (developer)


[RU] Для регистрации пользователь отправляет запрос со своим имейлом и желаемым username.
В случае, если email и username проходят валидацию, пользователь получает код подтверждения на почту.
Отправив запрос с username и кодом подтверждения, пользователь получает собственный JWT токен, с которым
он может оставлять ревью, оценивать произведения, редактировать собственный профиль.

Контрибьюторы командного проекта:
- ks_grshkv (тимлмд, разработчик)
- nata_shepina (разработчик)
- SmileHorn (разработчик)


### Requests Examples / Примеры запросов:

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

### Launching project / Как запустить проект:

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