# Подготовить базу данных

Используется [*PostgreSQL*](https://www.enterprisedb.com/) (13.2).
1) [*скачать*](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) PostgreSQL
2) [*создать пользователя*](#создать-пользователя)
    1) логин и пароль есть в [*secure/login_password.py*](/secure/login_password.py) (словарь DATABASE)
3) [*выдать пользователю все привилегии*](#выдать-пользователю-все-привилегии)
4) [*сделать пользователя суперпользователем*](#сделать-пользователя-суперпользователем)
5) добавить в базу отслеживаемые сайты, выполнив скрип [*add_sites_to_db.py*](/service_app/scripts/add_sites_to_db.py)
    1) `python manage.py runscript add_sites_to_db`

### Особенные типы полей (для PostgreSQL)
1) [*HStoreField*](https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/fields/#hstorefield) - для хранения
   словарей.
2) [*ArrayField*](https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/fields/#arrayfield) - для хранения списков

### Создать пользователя
```
CREATE USER <username> WITH PASSWORD '<password>';
```

### Выдать пользователю все привилегии
```
GRANT ALL PRIVILEGES ON DATABASE discount_waiter TO <username>;
```

### Сделать пользователя суперпользователем
```
ALTER USER <username> WITH SUPERUSER;
```
