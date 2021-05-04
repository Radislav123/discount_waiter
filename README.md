# Общее
1) если не сказано иное, команды выполняются из корня проекта
2) полезности расположены в [*attachments/*](/attachments)
3) проект построен на основе Django

# Интерпретер
[*Как*](https://www.jetbrains.com/help/idea/creating-virtual-environment.html) создать виртуальное окружение.  
Папка для интерпретера - [*discount_waiter_env/*](/discount_waiter_env)

## Активация интерпретера
```
source discount_waiter_env/bin/activate                 # Unix
discount_waiter_env/Scripts/activate.bat                # Windows
```
Но я использую conda, поэтому смотреть
[*сюда*](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment).

# Требуемые библиотеки
`pip install -r requirements.txt`
У Scrapy могут быть проблемы с установкой на Windows через pip, в таких случаях имеет смысл установить
conda-окружение и использовать его.
  
[*requirements.txt*](https://pip.pypa.io/en/stable/user_guide/#requirements-files)  
Версии библиотек могут быть не самыми новыми, но с ними все должно работать.

# Описание модулей проекта
1) [*discount_waiter/*](/discount_waiter) - проект Django
2) [*scrapers_app/*](/scrapers_app) - все, что связано со скрапингом данных с сайтов
    1) [*scrapers_app/scrapers/*](/scrapers_app/scrapers) - скраперы (использование библиотеки Scrapy)
3) [*telegram_bot_app/*](/telegram_bot_app) - все, что связано с Telegram-ботом
    1) [*telegram_bot_app/telegram_bot/*](/telegram_bot_app/telegram_bot) -
       Telegram-бот (использование библиотеки pyTelegramBotAPI)

## Не модули
1) [*attachments/*](/attachments) - обычно не код, но важное для проекта
2) [*discount_waiter_env/*](/discount_waiter_env) - тут должен лежать интерпретер
3) [*constants/*](/constants) - константы
    1) [*constants/secure/*](/constants/secure) - тут должно лежать то, что не сохраняется в git (например, пароли)
4) [*scripts/*](/scripts) - скрипты проекта Django

# База данных
[*attachments/manuals/DATABASE.md*](/attachments/manuals/DATABASE.md)

# Django
[*attachments/manuals/DJANGO.md*](/attachments/manuals/DJANGO.md)

# Веб-скрапинг
[*attachments/manuals/SCRAPING.md*](/attachments/manuals/SCRAPING.md)

# Telegram-бот
[*attachments/manuals/TELEGRAM.md*](/attachments/manuals/TELEGRAM.md)

# ToDo
[*attachments/TODO.md*](/attachments/TODO.md)

# Периодические действия
[*Timeloop*](https://pypi.org/project/timeloop/)
