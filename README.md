#  Сервис управления рассылками

## Настройки проекта
+ cоздать файл *.env* в корне проекта с настройками, аналогичными *.env.example*
+ заполнение БД
  ```
  python manage.py migrate
  python manage.py create_users && python manage.py seed
  ```
+ ``settings.SCHEDULER_ACTIVE = True`` - выставить для запуска встроенной периодической задачи
+ запуск одной копии проекта
  ```
  python manage.py runserver --noreload
  ```

## Приложения
+ **authen** - Аутентификация
+ **letters_sending** - Почтовые рассылки
+ **blog** - Блоги

## Модели
* **authen**: ``User``, ``Country``, 
* **letters_sending**: ``Message``, ``Client``, ``LettersSending``,
  + ``DatePeriod`` - Интервал отправки,
  + ``Status`` - Статус рассылки,
  + ``Attempt`` - Попытка рассылки
* **blog**: ``Blog``
  
## Контроллеры (CBV-стиль) 
* **authen**
  + ``CustomLoginView`` - авторизация
  + ``CustomLogoutView`` - выход из системы
  + ``RegisterView`` - регистрация пользователя
  + ``ProfileView`` - профиль пользователя
  + ``verificate_email``(FBV) - подтвердить почту
  + ``CustomPasswordResetView`` - сброс пароля - отправка ссылки на почту
  + ``CustomUserPasswordResetConfirmView`` - сброс пароля - ввод нового пароля
  + ``UserListView`` - список пользователей
  + ``set_user_activation``(FBV) - устанавливает активность пользователя
* **letters_sending**
  + CRUD рассылок
    * ``LettersSendingListView`` - список
    * ``LettersSendingDetailView`` - детали
    * ``LettersSendingCreateView`` - создание
    * ``LettersSendingUpdateView`` - обновление
    * ``LettersSendingDeleteView`` - удаление
    * ``deactivate_letterssending``(FBV) - выключить активную рассылку
  + CRUD клиентов:
    * ``ClientListView`` - список
    * ``ClientCreateView`` - создание
    * ``ClientUpdateView`` - обновление
    * ``ClientDeleteView`` - удаление
  + CRUD сообщений
    * ``MessageListView`` - список
    * ``MessageDetailView`` - детали
    * ``MessageUpdateView`` - обновление
    * ``MessageDeleteView`` - удаление
  + ``AttemptListView`` - статистика рассылок
  + ``index_page``(FBV) - главная страница 
* **blog**
  + ``BlogListView`` - список
  + ``BlogDetailView`` - детали

## Рассылка писем

+ ``letters_sending/management/commands/scheduler.py`` - запуск консольной периодической задачи рассылок
+ ``letters_sending.services.letsend_schedulrer.LettersSendingScheduler`` - встроенный планировщик рассылок
  *  ``letters_sending.LetterConfig.ready()`` - запуск планировщика
+ ``letters_sending.views.views.AttemptListView`` - статистика рассылок

Одновременно может быть запущен планировщик или консольная команда. 


## Права 

+ Все пользователи могут смотреть блоги. На главной странице ссылка на все блоги
+ ``OwnerVerificationMixin`` - миксин модификации GET и POST методов для проверки владельца объекта
+ ``OwnerListVerificationMixin`` - миксин модификации get_queryset() на просмотр списка всех или своих объектов

###  Менеджер
+ ``view_client,view_message,view_letterssending,view_user`` - просмотр всех клиентов, сообщений, рассылок, пользователей
+ ``view_custom_client,view_message,view_custom_letterssending`` - просмотр своих клиентов, сообщений, рассылок
+ ``block_user`` - блокировать пользователей
+ ``deactivate_letterssending`` - отключать рассылки

### Пользователь
* ``view_*_perm`` - права на просмотр списка объектов
* ``view_owner_*_perm`` - доступ к ListView - контроллерам

+ просмотр своих клиентов, сообщений, рассылок, пользователей
+ добавление клиентов, сообщений, рассылок
+ обновление своих клиентов, сообщений, рассылок
+ удаление своих клиентов, сообщений, рассылок

При регистрации пользователь попадает в группу пользователей

### Блогер
+ добавление, обновление и удаление блогов

## Кэширование

Кэширование реализовано через собственные классы:
+ ``ManagedCache`` - кэширует страницы для каждого пользователя. При обновлении данных страницы кэши страницы всех пользователй сбрасываются
+ ``ManagedCachedMixin`` - миксин CBV-контроллеров для управления кэшем страниц. Заменяет get-,render_to_response-методы.

Добавлено кэширование:
+ главная страница
+ список рассылок, сообщений, клиентов, блогов
+ детальная страница рассылок, блогов

## Главная страница
![main](/readme/main.png)

## Профиль пользователя
![profile](/readme/user_profile.png)

## Рассылки 
![sendings](/readme/sendings.png)

## Статистика рассылок
![stat](/readme/stat.png)

## Клиенты
![clients](/readme/clients.png)

## Сообщения
![messages](/readme/messages.png)

## Блоги
![blogs](/readme/blogs.png)
