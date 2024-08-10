#  Сервис управления рассылками

### Настройки проекта
+ cоздать файл .env в корне проекта с настройками, аналогичными .env.example
+ заполнение БД
  * создание групп пользователей и пользователей ```python manage.py create_users```
  * сидирование таблиц БД ```python manage.py seed```
+ для запуска встроенной периодической задачи выставить ``settings.SCHEDULER_ACTIVE = True``

### Приложения
+ authen - Аутентификация
+ letters_sending - Почтовые рассылки
+ blog - Блоги

#### Модели (letters_sending/models.py)
* authen: ``User``, ``Country``, 
* letters_sending: ``Message``, ``Client``, ``LettersSending``,
  + ``DatePeriod`` - Интервал отправки,
  + ``Status`` - Статус рассылки,
  + ``Attempt`` - Попытка рассылки
* blog: ``Blog``
  
#### Контроллеры
* authen: 
  + ``CustomLoginView`` - АВТОРИЗАЦИЯ
  + ``CustomLogoutView`` - ВЫХОД ИЗ СИСТЕМЫ
  + ``RegisterView`` - РЕГИСТРАЦИЯ
  + ``ProfileView`` - ПРОФИЛЬ
  + ``verificate_email`` - ПОДТВЕРДИТЬ ПОЧТУ
  + ``CustomPasswordResetView`` - СБРОС ПАРОЛЯ - ОТПРАВКА ССЫЛКИ НА ПОЧТУ
  + ``CustomUserPasswordResetConfirmView`` - ВВОД НОВОГО ПАРОЛЯ
  + ``UserListView`` - СПИСОК ПОЛЬЗОВАТЕЛЕЙ
  + ``set_user_activation`` - УСТАНОВИТЬ АКТИВНОСТЬ ПОЛЬЗОВАТЕЛЯ
* letters_sending: контроллеры рассылок, клиентов, сообщений, статистики рассылок, главной страницы
* blog: ``BlogListView``, ``BlogDetailView``
 
#### Шаблоны
+ ``basic.html`` - базовый шаблон
+ ``index.html`` - главная страница
+ ``attempt_list.html`` - статистика попыток рассылки
+ ``confirm_delete.html`` - форма удаления объекта
+ ``form.html`` - форма заполнения объекта
+ ``components/`` - компоненты
+ ``client/`` - клиент
+ ``message/`` - сообщение
+ ``letters_sending/`` - рассылка
+ ``authen/templates`` - пользователь
+ ``blog/`` - блог 

#### Скрипт рассылки
``letters_sending/management/commands/scheduler.py`` - запуск консольной периодической задачи 

