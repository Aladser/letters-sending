#  Сервис управления рассылками

### Настройки проекта
+ cоздать файл .env в корне проекта с настройками, аналогичными .env.example
+ заполнение БД
  * создание групп пользователей и пользователей ```python manage.py init_users```
  * создание клиентов, сообщений и вспомогательных таблиц ```python manage.py seed```
+ для запуска встроенной периодической задачи выставить ``settings.SCHEDULER_ACTIVE = True``

#### Модели (letters_sending/models.py)
+ ``Message`` - Сообщение
+ ``Client`` - Клиент
+ ``DatePeriod`` - Интервал отправки
+ ``Status`` - Статус рассылки
+ ``LettersSending`` - Рассылка
+ ``Attempt`` - Попытка рассылки


#### Контроллеры
+ ``client`` (*letters_sending/views/client/*) - Сообщение CRUID
+ ``lettersSending`` (*letters_sending/views/message/*) - Клиент CRUID
+ ``message`` (*lettersSending/views/letters_sending/*) - Рассылка CRUID
+ ``attempt_list`` (*lettersSending/views/views.py/AttemptListView*) - статистика попыток рассылки
 
#### Шаблоны
+ ``basic.html`` - базовый шаблон
+ ``components/`` - компоненты
+ ``client/`` - клиент
+ ``message/`` - сообщение
+ ``letters_sending/`` - рассылка
+ ``attempt_list.html`` - статистика попыток рассылки


#### Скрипт рассылки
``letters_sending/management/commands/scheduler.py`` - консольная команда запуска периодической задачи

``python manage.py scheduler`` - запуск консольной периодической задачи 
