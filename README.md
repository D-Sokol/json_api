#Веб-сервер для хранения и подачи объявлений.
Этот проект представляет собой веб-сервер, предоставляющий API для создания и чтения объявлений в формате JSON в соответствии с [предъявляемыми требованиями](https://github.com/avito-tech/verticals/blob/master/trainee/backend.md). Веб-сервер написан на языке `Python 3` с использованием фреймворков `Flask` и `SQLAlchemy`.


## Установка
Проект может быть поднят при помощи `docker-compose` или развернут вручную на любом сервере, предоставляющем доступ к базе данных MySQL. В этом разделе описан процесс подготовки проекта к запуску для ОС Linux в предположении, что содержимое этого репозитория скопировано в активную директорию.

### Docker
В целях безопасности данные для доступа к базе данных должны быть предоставлены в переменных окружения. Необходимые переменные определены в файле `env.template`. Перед созданием контейнера их значения можно изменить желаемым образом, но выбранные значения по умолчанию позволяют создать рабочий контейнер.
Таким образом, перед созданием контейнера нужно загрузить переменные в оболочку:
```bash
source env.template
```

Затем нужно создать контейнер при помощи следующей команды:
```bash
docker-compose build
```

### Развертывание вне контейнера
1. При развертывании проекта без использования Docker следует использовать другой подход к хранению настроек. Вместо редактирования файла `env.template` следует скопировать его в `.env` и, при необходимости, изменять значения переменных в файле `.env`. Обязательно должны быть заданы следующие переменные:
* `MYSQL_USER` - имя пользователя для доступа к базе данных.
* `MYSQL_PASSWORD` - пароль пользователя для доступа к базе данных.
* `MYSQL_DATABASE` - название базы данных.
* `MYSQL_HOST` - сервер, предоставляющий доступ к базе данных. В большинстве случаев следует указывать `localhost`.
* `MYSQL_PORT` - порт, через который осуществляется доступ к базе данных. В большинстве случаев следует указывать 3306.

При этом указанная база данных и пользователь должны существовать, база данных не должна содержать таблиц. Кроме того, пользователю должны быть предоставлены привилегии SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, REFERENCES, ALTER (не все из них действительно необходимы для работы, однако рекомендуется представить их для дальнейшего развития приложения) по отношению к этой бд.

2. Далее необходимо создать виртуальное окружение и установить зависимости при помощи следующих команд:
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```


## Запуск

### Docker
Запуск приложения производится с помощью команды `docker-compose up`

### Развертывание вне контейнера
Запуск приложения производится с помощью следующих команд:
```bash
source venv/bin/activate
gunicorn app:app
```

## Используемые модели
* Пример модели объявления в формате JSON в ответе сервера на запрос типа GET со всеми дополнительными полями (см. описание методов):
```json
{
  "all_photos": [
    "http://example.com/images/11.png",
    "http://example.com/images/12.png"
  ],
  "description": "string",
  "id": 1,
  "main_photo": "http://example.com/images/11.png",
  "price": 495.0,
  "title": "string"
}
```

* Пример модели объявления в формате JSON, ожидаемой сервером в запросе типа POST:
```json
{
  "title": "string",
  "description": "string",
  "price": 495.0,
  "photo_links": [
    "http://example.com/images/11.png",
    "http://example.com/images/12.png"
  ]
}
```

* Пример ответа сервера на корректный запрос типа POST:
```json
{
  "id": 1
}
```

* Пример ответа сервера на некорректный запрос типа POST:
```json
"price: -1 is less than the minimum of 0.0"
```


# Ссылки на этот проект
* [https://bitbucket.org/sokol61/json-api]
* [https://github.com/D-Sokol/json_api]
