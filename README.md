# Общее
1) если не сказано иное, команды выполняются из корня проекта
2) полезности расположены в [*attachments/*](/attachments)
3) проект построен на основе Django
4) каждый пользователь идентифицируется по имени пользователя (username) и идентификатору чата(chat_id)

# Интерпретер
[*Как*](https://www.jetbrains.com/help/idea/creating-virtual-environment.html) создать виртуальное окружение.  
Папка для интерпретера - [*discount_waiter_env/*](/discount_waiter_env).

## Активация интерпретера
```
source discount_waiter_env/bin/activate                 # Unix
discount_waiter_env/Scripts/activate.bat                # Windows
```
Если используется conda-окружение, смотреть
[*сюда*](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment).

# Требуемые библиотеки
`pip install -r requirements.txt`

[*requirements.txt*](https://pip.pypa.io/en/stable/user_guide/#requirements-files)  
Версии библиотек могут быть не самыми новыми, но с ними все должно работать.

# Описание модулей проекта
1) [*discount_waiter/*](/discount_waiter) - настройки Django-проекта
2) [*scrapers_app/*](/scrapers_app) - все, что связано со скрапингом данных с сайтов
    1) [*scrapers_app/scrapers/*](/scrapers_app/scrapers) - скраперы
3) [*telegram_bot_app/*](/telegram_bot_app) - все, что связано с Telegram-ботом
    1) [*telegram_bot_app/telegram_bot/*](/telegram_bot_app/telegram_bot) -
       Telegram-бот (использование библиотеки pyTelegramBotAPI)
4) [*service_app*](/service_app) - реализация общих для проекта функций, как, например, модели (для БД)

## Не модули
1) [*attachments/*](/attachments) - обычно не код, но важное для проекта
2) [*discount_waiter_env/*](/discount_waiter_env) - тут должен лежать интерпретер
3) [*secure/*](/secure) - тут должно лежать то, что не сохраняется в git (например, пароли)
4) [*service_app/scripts/*](/service_app/scripts) - скрипты Django-проекта
5) [*logs/*](logs) - логи

# База данных
[*attachments/manuals/DATABASE.md*](/attachments/manuals/DATABASE.md)

# Django
[*attachments/manuals/DJANGO.md*](/attachments/manuals/DJANGO.md)

# Веб-скрапинг
[*attachments/manuals/SCRAPING.md*](/attachments/manuals/SCRAPING.md)

# Telegram-бот
[*attachments/manuals/TELEGRAM.md*](/attachments/manuals/TELEGRAM.md)

# Периодические действия
[*timeloop*](https://pypi.org/project/timeloop/)
