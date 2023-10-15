# SolidLabTestApp

## Конфигурация и запуск

Перед запуском необходимо создать и добавить в виртуальное окружение данные, по шаблону из .dev.env

Установка библиотек:
```shell
pip install -r Requirements.txt
```

Создание таблиц в бд:

  1.
  ```shell
  python manage.py makemigrations test_app
  ```
  2.
  ```shell
  python manage.py migrate
  ```

Тесты:
```shell
python manage.py test
```

Запуск приложения:
```shell
python manage.py runserver 8000
```
