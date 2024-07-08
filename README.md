# MADSOFT Тестовое задание Python-разработчик 
Тестовое задание
##### Стек: Pyton, FastAPI, SQLAlchemy

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:CrockoMan/madsoft_test.git
```

```
cd madsoft_test
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:
* Если у вас Linux/macOS

    ```
    python3 -m pip install --upgrade pip
    ```
* Если у вас windows
* 
    ```
    pip install -r requirements.txt
    ```

Заполнить файл конфигурации .env
```
APP_TITLE=Мемы
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=SECRET
S3_ACCESS_KEY=
S3_SECRET_KEY=
S3_ENDPOINT_URL=
S3_BUCKET_NAME=
S3_VERIFY=
S3_BUCKET_PUBLIC_PATH=
```

Применить миграции

```
alembic upgrade head
```

Запустить сервис:

```
uvicorn main:app --reload
```

### API сервиса доступен после запуска 
[Redoc](http://127.0.0.1:8000/docs/)  http://127.0.0.1:8000/docs  </br>
[Swagger](http://127.0.0.1:8000/redoc/)  http://127.0.0.1:8000/redoc  </br>

Автор: [К.Гурашкин](https://github.com/CrockoMan)
