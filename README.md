# api_yamdb
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Живопись» или «Ювелирка»).

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

### Основные ресурсы api:

- AUTH - Регистрация пользователей и выдача токенов
- CATEGORIES - Категории (типы) произведений
- GENRES - Категории жанров
- TITLES - Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- REVIEWS - Отзывы
- COMMENTS - Комментарии к отзывам
- USERS - Пользователи

Более подробнее см в /redoc/

### Как запустить проект:

Образ есть на DockerHub

Docker Pull Command:

```
docker pull vladyyp/infra_web
```

1. Создать в /infra файл .env
Шаблон заполнения:

```
- DB_ENGINE=django.db.backends.postgresql
- DB_NAME=
- POSTGRES_USER=
- POSTGRES_PASSWORD=
- DB_HOST=
- DB_PORT=

- SECRET_KEY=
- ALLOWED_HOSTS=
```

2. Запуск docker-compose

```
docker-compose up -d --build 
```

3. Выполнить по очереди команды:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

В проекте есть дамп БД с тестовыми данными, можно заполнить командой:
```
docker-compose exec web python manage.py loaddata fixtures.json
```

### Авторы проекта:
- Команда Яндекс.Практикума
- Дмитрий Филимонов - Тимлид
- Григорьева Мария - Разработчик
- Максимов Владислав - Разработчик


### Примеры запросов:
К проекту подключен модуль redoc, содержащий документацию по доступным эндпоинтам и примерам запросов. Адрес для redoc - [base]/redoc/.

Основные запросы:

**CATEGORIES**

#### Получение списка всех категорий

request:

```
GET [base]api/v1/categories/
```

response:

```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```

#### Добавление новой категории

```
POST [base]api/v1/categories/
```

request:
```json
{

    "name": "string",
    "slug": "string"

}
```

response:

```json
{

    "name": "string",
    "slug": "string"

}
```

#### Удаление категории

```
DELETE [base]api/v1/categories/{slug}/
```

**GENRES**

#### Получение списка всех жанров

request:
```
GET [base]api/v1/genres/
```

response:
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```

#### Добавление жанра


request:
```
POST [base]api/v1/genres/
```
```json
{
  "name": "string",
  "slug": "string"
}
```


response:
```json
{
  "name": "string",
  "slug": "string"
}
```

#### Удаление жанра

```
DELETE [base]api/v1/genres/{slug}/
```

**TITLES**

#### Получение списка всех произведений

request:
```
GET [base]api/v1/titles/
```

response:
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```

#### Добавление произведения

request:
```
POST [base]api/v1/titles/
```

```json
{

    "name": "string",
    "year": 0,
    "description": "string",
    "genre": 

    [
        "string"
    ],
    "category": "string"

}
```

response:
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

#### Получение информации о произведении

request:
```
GET [base]api/v1/titles/{titles_id}/
```

response:
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

#### Частичное обновление информации о произведении

request:
```
PATCH [base]api/v1/titles/{titles_id}/
```
```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

response:
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

#### Удаление произведения

request:
```
PATCH [base]api/v1/titles/{titles_id}/
```

**REVIEWS**

#### Получение списка всех отзывов

request:
```
GET [base]api/v1/titles/{title_id}/reviews/
```

response:
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```

#### Добавление нового отзыва

request:
```
POST [base]api/v1/titles/{title_id}/reviews/
```

```json
{

    "text": "string",
    "score": 1

}
```

response
```json
{

    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"

}
```

#### Полуение отзыва по id

request:
```
GET [base]api/v1/titles/{title_id}/reviews/{review_id}/
```

response
```json
{

    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"

}
```

#### Частичное обновление отзыва по id

request:
```
PATCH [base]api/v1/titles/{titles_id}/
```

```json
{

    "text": "string",
    "score": 1

}
```

response
```json
{

    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"

}
```

#### Удаление отзыва по id

request:
```
DELETE [base]api/v1/titles/{title_id}/reviews/{review_id}/
```

**COMMENTS**

#### Получение списка всех комментариев к отзыву

request:
```
GET [base]api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

response
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```

#### Добавление комментария к отзыву

request:
```
POST [base]api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

```json
{

    "text": "string"

}
```

response
```json
{

    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"

}
```

#### Получение комментария к отзыву

request:
```
GET [base]api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

response
```json
{

    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"

}
```

#### Частичное обновление комментария к отзыву

request:
```
PATCH [base]api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

```json
{

    "text": "string"

}
```

response
```json
{

    "id": 0,
    "text": "string",
    "author": "string",
    "pub_date": "2019-08-24T14:15:22Z"

}
```

#### Удаление комментария к отзыву

request:
```
DELETE [base]api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

**USERS**

#### Получение списка всех пользователей

request:
```
GET [base]api/v1/users/
```

response
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```

#### Добавление пользователя

request:
```
POST [base]api/v1/users/
```

```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
response
```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

#### Получение пользователя по username

request:
```
GET [base]api/v1/users/{username}/
```

response
```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

#### Изменение данных пользователя по username

request:
```
PATCH [base]api/v1/users/{username}/
```

```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

response
```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

#### Удаление пользователя по username

request:
```
DELETE [base]api/v1/users/{username}/
```

#### Получение данных своей учетной записи

request:
```
GET [base]api/v1/users/me/
```

response
```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

#### Изменение данных своей учетной записи

request:
```
PATCH [base]api/v1/users/me/
```

```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

response
```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```


