# Общее
1) если не сказано иное, команды выполняются из корня проекта
2) полезности расположены в [*attachments/*](/attachments)
3) проект построен на основе Django

# Интерпретер
[*Как*](https://www.jetbrains.com/help/idea/creating-virtual-environment.html) создать виртуальное окружение.  
Папка для интерпретера - [*zara_bot_env/*](/zara_bot_env)

## Активация интерпретера
```
source zara_bot_env/bin/activate                # Unix
zara_bot_env/Scripts/activate.bat               # Windows
```
Но я использую conda, поэтому смотреть
[*сюда*](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment).

# Требуемые библиотеки
[*Оригинал решения*](https://stackoverflow.com/a/38609653)
1) установка через conda тех модулей, которые возможно так установить (все из-за scrapy, который через pip на Windows
нормально не устанавливается)
    1) Windows: `FOR /F "delims=~" %f in (requirements.txt) DO conda install --yes "%f" || pip install "%f"`
    2) Unix: `while read requirement; do conda install --yes $requirement || pip install $requirement; done < requirements.txt`
2) возможно, у Unix проблем не возникает, но на Windows скрипт зацикливается, поэтому, когда он зациклился, 
его нужно прервать и доустановить оставшиеся пакеты командой `pip install -r requirements.txt`
  
[*requirements.txt*](https://pip.pypa.io/en/stable/user_guide/#requirements-files)  
Версии библиотек могут быть не самыми новыми, но с ними все должно работать.

# Описание модулей проекта
1) [*discount_waiter/*](/discount_waiter) - проект Django
2) [*scrapers_app/*](/scrapers_app) - все, что связано со скрапингом данных с сайтов

## Не модули
1) [*attachments/*](/attachments) - обычно не код, но важное для проекта
2) [*zara_bot_env/*](/zara_bot_env) - тут должен лежать интерпретер
3) [*constants/*](/constants) - константы
    1) [*constants/secure/*](/constants/secure) - тут должно лежать то, что не сохраняется в git (например, пароли)
4) [*scripts/*](/scripts) - скрипты проекта Django

# База данных
[*attachments/manuals/DATABASE.md*](/attachments/manuals/DATABASE.md)

# Веб-скрапинг
[*attachments/manuals/SCRAPING.md*](/attachments/manuals/SCRAPING.md)

# Django
[*attachments/manuals/DJANGO.md*](/attachments/manuals/DJANGO.md)
