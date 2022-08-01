# CI и CD проекта api_yamdb
## Статус проекта
![workflow](https://github.com/single1709/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## Адрес сервера, где запущен проект
`51.250.21.44`
## Кратко о проекте
Проект api_yamdb - реализация API для другого учебного проекта Yatube.
API необходим для унифицированного доступа к функциям проекта Yatube.
Настроено Continuous Integration и Continuous Deployment, а именно:
 - автоматический запуск тестов,
 - обновление образов на Docker Hub,
 - автоматический деплой на боевой сервер при пуше в главную ветку main.
 - оповещение о деплое в Telegram через бота

## Secrets GitHub Actions переменные окружения:

`DB_ENGINE` - указываем, что работаем с postgresql

`DB_NAME` - имя базы данных

`POSTGRES_USER` - логин для подключения к базе данных

`POSTGRES_PASSWORD` - пароль для подключения к БД

`DB_HOST` - название сервиса (контейнера)

`DB_PORT` - порт для подключения к БД 

`DOCKER_PASSWORD` - пароль Docker Hub

`DOCKER_USERNAME` - логин Docker Hub

`HOST` - IP-адрес вашего сервера

`USER` - имя пользователя для подключения к серверу

`PASSPHRASE` - если при создании ssh-ключа вы использовали фразу-пароль

`SSH_KEY` - приватный ключ с компьютера, имеющего доступ к серверу

`TELEGRAM_TO` - ID своего телеграм-аккаунта

`TELEGRAM_TOKEN` - токен бота

## Запуск приложения
Если запуск выполняется на сервере, проследите, чтобы там присутствовали файлы `docker-compose.yaml` и `nginx/default.conf`.
Добавьте в Secrets GitHub Actions переменные окружения:

Внесите изменения в коде и выполните`push`.

Далее выполните по очереди команды:

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

## Заполнения базы данными
Для загрузки данных в БД используйте команду:

`docker-coppose exec web python manage.py loaddata fixtures.json`

Если запуск выполняется на сервере, проследите, чтобы там присутствовал файл `fixtures.json`

## Автор
Сергей,

Студент факультета Backend-разработки в Яндекс.Практикум.

## Используемые технологии

* Django
* Docker
* NGINX
* Яндекс.Облако
