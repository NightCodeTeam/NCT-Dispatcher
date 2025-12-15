# Night Code Team Dispatcher

Это система для отслеживания и работой со сбоями, багами и ошибками в работе других сервисов. Проект был вдохновлен Netflix Dispatcher однако на данный момент функционально уступает.

## v0.2.0

- Теперь доступна web-версия проекта:
  - Полноценный список всех инцидентов и удобный способ их редактирования
  - Удобное отображение логов, статусов и собранных данных
  - Редактирование приложений возможность просмотра всех логов приложений
- Функционал telegram бота сведен к минимуму, теперь в момент получения ошибки отправляется сообщение в админ чат.

## Компоненты

### Web версия

Для запуска ознакомительной версии подготовлен `docker-compose.yml` файл. Не забудьте настроить .env файлы в `dispatcher_api` и `dispatcher_front`.

```sh
docker-compose up --build
```

#### Dispatcher FRONT

Dispatcher FRONT - это веб-приложение, которое предоставляет удобный интерфейс для просмотра и редактирования инцидентов. Оно позволяет администраторам и пользователям быстро находить и решать проблемы, связанные с приложениями и сервисами.

##### Запуск отдельной версии:

Перед запуском скопируйте файл .env.prod в .env и настройте его. Так же убедитесь что Dispatcher API запущен и доступен.

```sh
npm run dev
```

#### Dispatcher API

Dispatcher API - это REST API, написанное на python + FastAPI. 

##### Запуск отдельной версии:

Для корректной работы убедитесь что база данных уже создана и настроена. Так же скопируйте файл .env.prod в .env и настройте его.
Для запуска подготовлен Dockerfile или запустите скрипт запуска в корне проекта.

```sh
cd dispatcher_api
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python app
```

### Dispatcher Maker

Это пакет для отправки инцидентов. Добавте его в свой проект и отправляйте инциденты с помощью классов Dispatcher и DispatcherAsync.
Пример:

```python
from dispatcher_maker import Dispatcher

dispatcher = Dispatcher(
    dispatcher_url='https://dispatcher-api.example.com',   # url dispatcher api
    app_name='MyApp',   # название приложения добавленного в dispatcher api
    dispatcher_code='123456',   # сгенерированный код этого приложения
    loggers_paths=['/var/absolute/path/to/logger1.txt', './path/to/logger2.txt'],   # пути к логам желательно указывать в абсолютном формате
    max_logs_to_send=100    # сколько строк каждого лога будет отправлено вместе с инцидентом, можно переопределить в запросе
)

dispatcher.send(
    title='Error in user registration',   # название инцидента
    message='User registration failed',   # его подробное описание
    level='error',   # уровень инцидента debug, info, warning, error, crit
    logs=None,   # список логов, которые будут отправлены вместе с инцидентом, можно указать None так как их уже отправили выше
    max_logs_to_send=50   # переопределим для этого конкретного случая сколько логоф отправить
)
```

## Запрос для отправки инцидента

Если нет возможности использовать классы из `dispatcher_maker`, то:

1. Создайте приложение через web интерфейс
2. Сохраните имя и сгенерированныйкод приложения
3. Создайте запрос к URL dispatcher api и в json формате отправьте следующие:

```json
{
    "incident": {
        "title": "Error in user registration",
        "message": "User registration failed",
        "level": "error",
        "logs": "log 1\nlog 2\nlog 3\nlog 4\nlog 5",
    },
    "app_name": "your_app_name_here",
    "code": "your_generated_code_here",
}
```
