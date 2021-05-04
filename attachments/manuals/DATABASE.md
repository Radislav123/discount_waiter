# Подготовить базу данных
Используется [*PostgreSQL*](https://www.enterprisedb.com/) (13.2).
1) [*скачать*](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
2) логин и пароль есть в [*constants/secure/login_password.py*](/constants/secure/login_password.py) (словарь DATABASE)

### Создать пользователя
```
CREATE USER username WITH PASSWORD 'password';
```

### Выдать пользователю все привилегии
```
GRANT ALL PRIVILEGES ON DATABASE discount_waiter TO root;
```
