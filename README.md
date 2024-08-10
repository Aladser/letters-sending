#  Сервис управления рассылками

## Настройки проекта
+ cоздать файл .env в корне проекта с настройками, аналогичными .env.example
+ заполнение БД
  * создание групп пользователей, разрешений групп, пользователей ```python manage.py create_users```
  * сидирование таблиц БД ```python manage.py seed```
+ для запуска встроенной периодической задачи выставить ``settings.SCHEDULER_ACTIVE = True``

## Приложения
+ authen - Аутентификация
+ letters_sending - Почтовые рассылки
+ blog - Блоги

## Модели
* authen: ``User``, ``Country``, 
* letters_sending: ``Message``, ``Client``, ``LettersSending``,
  + ``DatePeriod`` - Интервал отправки,
  + ``Status`` - Статус рассылки,
  + ``Attempt`` - Попытка рассылки
* blog: ``Blog``
  
## Контроллеры
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
 
## Шаблоны
+ ``letters_sending .. basic.html`` - базовый шаблон
+ ``letters_sending .. index.html`` - главная страница
+ ``letters_sending .. attempt_list.html`` - статистика попыток рассылки
+ ``letters_sending .. confirm_delete.html`` - форма удаления объекта
+ ``letters_sending .. form.html`` - форма заполнения объекта
+ ``letters_sending .. components/`` - компоненты
+ ``letters_sending .. client/`` - клиент
+ ``letters_sending .. message/`` - сообщение
+ ``letters_sending .. letters_sending/`` - рассылка
+ ``authen .. `` - пользователь
+ ``blog .. blog/`` - блог 

## Рассылка писем

+ *letters_sending/management/commands/scheduler.py* - запуск консольной периодической задачи рассылок
+ ``letters_sending.services.letsend_schedulrer.LettersSendingScheduler`` - встроенный планировщик рассылок
+ ``letters_sending.views.views.AttemptListView`` - контроллер статистики рассылок

Одновременно может быть запущен только один тип рассылки

## Права 

Все пользователи могут смотреть блоги. На главной странице ссылка на все блоги

###  Менеджер
+ ``view_client,view_message,view_letterssending,view_user`` - просмотр всех клиентов, сообщений, рассылок, пользователей
+ ``view_custom_client,view_message,view_custom_letterssending,view_custom_user`` - просмотр своих клиентов, сообщений, рассылок, пользователей
+ ``block_user`` - блокировать пользователей
+ ``deactivate_letterssending`` - отключать рассылки

### Пользователь
+ добавление клиентов, сообщений, рассылок
+ обновление своих клиентов, сообщений, рассылок
+ удаление своих клиентов, сообщений, рассылок

При регистрация пользователь попадает в группу пользователей

### Блогер
+ добавление, обновление и удаление блогов

## Кэширование

Кэширование реализовано через собственные классы:
+ ``ManagedCache`` - кэширует страницы для каждого пользователя. При обновлении данных страниц кэши страницы всех пользователй сбрасываются
+ ``ManagedCachedMixin`` - миксин CBV-контроллеров для управления кэшем страниц. Заменяет get-,render_to_response-методы.
