from django.core.management import BaseCommand
from pytils.translit import slugify

from authen.models import User
from letters_sending.models import Message, Client, DatePeriod, Status, LettersSending, Attempt
from libs.env import env


class Command(BaseCommand):
    # Периодичность рассылки
    SECONDS_IN_MINUTE = 60
    period_list = [
        {'pk': 1, 'name': 'minute', 'description': 'минута', 'interval': SECONDS_IN_MINUTE},
        {'pk': 2, 'name': 'five_minutes', 'description': '5 минут', 'interval': SECONDS_IN_MINUTE * 5},
        {'pk': 3, 'name': 'hour', 'description': 'час', 'interval': SECONDS_IN_MINUTE * 60},
        {'pk': 4, 'name': 'day', 'description': 'день', 'interval': SECONDS_IN_MINUTE * 60 * 24},
        {'pk': 5, 'name': 'week', 'description': 'неделя', 'interval': SECONDS_IN_MINUTE * 60 * 24 * 7},
        {'pk': 6, 'name': 'month', 'description': 'месяц', 'interval': SECONDS_IN_MINUTE * 60 * 24 * 30},
    ]

    # Статус рассылки
    status_list = [
        {'pk': 1, 'name': 'created', 'description': 'Создана'},
        {'pk': 2, 'name': 'launched', 'description': 'Запущена'},
        {'pk': 3, 'name': 'completed', 'description': 'Завершена'},
    ]


    # Клиенты
    clients_list = [
        {'surname': 'Софронов', 'name': 'Александр', 'patronym': 'Глебович', 'owner_id': 2},
        {'surname': 'Калугин', 'name': 'Матвей', 'patronym': 'Александрович', 'owner_id': 2},
        {'surname': 'Попов', 'name': 'Даниил', 'patronym': 'Станиславович', 'owner_id': 2},
        {'surname': 'Дроздова', 'name': 'Надежда', 'patronym': 'Александровна', 'owner_id': 2},
        {'surname': 'Виноградов', 'name': 'Вадим', 'patronym': 'Михайлович', 'owner_id': 2},
        {'surname': 'Макаров', 'name': 'Ян', 'patronym': 'Андреевич', 'owner_id': 3},
        {'surname': 'Еремин', 'name': 'Степан', 'patronym': 'Владимирович', 'owner_id': 3},
        {'surname': 'Лазарева', 'name': 'Александра', 'patronym': 'Святославовна', 'owner_id': 3},
        {'surname': 'Мельникова', 'name': 'Алиса', 'patronym': 'Эмировна', 'owner_id': 3}, ]

    # Сообщения
    subjects_list = [
        'РыбаТекст помогает животным',
        'Принцип работы генератора бредотекста',
        'Универсальный код речей',
        'Если вам есть, что сказать',
        'Не работает DebugView в Google Analytics 4?',
        'Установка PyCharm и создание проекта',
        'Станьте постоянным автором!',
        'Режим согласия Google (Consent Mode) V2',
        'Как рекламировать себя?',
        'Первичная настройка виртуального сервера (VPS)'
    ]
    contents_list = [
        'Мы любим животных и стараемся поддерживать тех из них, кому не посчастливилось иметь ласковых хозяев и тёплый кров. Один из проверенных способов это сделать — помочь благотворительному фонду «Луч Добра». Благодаря их труду ежегодно сотни питомцев находят свой новый дом.',
        'Внезапно, активно развивающиеся страны третьего мира неоднозначны и будут своевременно верифицированы. Приятно, граждане, наблюдать, как представители современных социальных резервов неоднозначны и будут описаны максимально подробно. Сложно сказать, почему базовые сценарии поведения пользователей, вне зависимости от их уровня, должны быть в равной степени предоставлены сами себе.',
        'Случайный текст похож на ласковый перезвон вертикали власти',
        'C помощью этого онлайн-генератора рыботекста можно пачками плодить как отдельные предложения и заголовки, так и целые абзацы отменнейшего рыбы-текста. ',
        'Прародителем текста-рыбы является известный "Lorem Ipsum" — латинский текст, ноги которого растут аж из 45 года до нашей эры. ',
        'Генерация рыбатекста происходит довольно просто: есть несколько фиксированных наборов фраз и словочетаний, из которых в опредёленном порядке формируются предложения. Предложения складываются в абзацы — и вы наслаждетесь очередным бредошедевром.',
        'Сама идея работы генератора заимствована у псевдосоветского "универсального кода речей", из которого мы выдернули используемые в нём словосочетания, запилили приличное количество собственных, в несколько раз усложнили алгоритм, добавив новые схемы сборки, — и оформили в виде быстрого и удобного сервиса для получения тестового контента.',
        'Другое название — "универсальный генератор речей". По легенде, всякие депутаты и руководители в СССР использовали в своих выступлениях заготовленный набор совмещающихся между собой словосочетаний, что позволяло нести псевдоумную ахинею часами. Что-то вроде дорвеев для политсобраний.',
        'Кстати, "универсальный код речей" насчитывает только 40 таких словосочетаний, тогда как в нашем случае — их уже 192. Из них наш генератор рыбатекста способен составить примерно 5 287 500 уникальных предложений-комбинаций (в оригинале же только 10 000). Просто вдумайтесь: около миллиарда символов случайного текста.',
        'То, что вы видите — не финальная версия РыбаТекста. Мы планируем развивать сервис, и для этого нам нужна обратная связь от вас, ваши советы и пожелания.'
    ]

    def handle(self, *args, **kwargs):
        if User.objects.all().count() == 0:
            raise Exception('Пользователи не найдены')

        user_pk = User.objects.get(email='user@test.ru').pk
        manager_pk = User.objects.get(email='manager@test.ru').pk

        LettersSending.objects.all().delete()
        Attempt.objects.all().delete()

        # -----------------------------
        # ----Периодичность рассылки---
        # -----------------------------
        DatePeriod.objects.all().delete()
        period_create_list = [DatePeriod(**params) for params in self.period_list]
        DatePeriod.objects.bulk_create(period_create_list)

        # -----------------------------
        # -------Статус рассылки-------
        # -----------------------------
        Status.objects.all().delete()
        status_create_list = [Status(**params) for params in self.status_list]
        Status.objects.bulk_create(status_create_list)

        # -----------------------------
        # ------------Клиенты----------
        # -----------------------------
        clients_obj_list = []
        for i in range(len(self.clients_list)):
            surname = slugify(self.clients_list[i]['surname'])
            name = slugify(self.clients_list[i]['name'])
            patronym = slugify(self.clients_list[i]['patronym'])
            email = f"{surname}_{name[:1]}{patronym[:1]}@test.ru"

            client = {
                'email': email,
                'surname': self.clients_list[i]['surname'],
                'name': self.clients_list[i]['name'],
                'patronym': self.clients_list[i]['patronym'],
                'owner_id': self.clients_list[i]['owner_id'],
            }
            clients_obj_list.append(client)

        Client.truncate()
        client_create_list = [Client(**params) for params in clients_obj_list]
        Client.objects.bulk_create(client_create_list)

        if env("MY_MAIL_1"):
            clients_obj_list.append({
                'email': env("MY_MAIL_1"),
                'surname': 'Антонов',
                'name': 'Иван',
                'patronym': 'Иванович',
                'owner_id': 1,
            })
        if env("MY_MAIL_2"):
            clients_obj_list.append({
                'email': env("MY_MAIL_2"),
                'surname': 'Антонов',
                'name': 'Игорь',
                'patronym': 'Игоревич',
                'owner_id': 1,
            })
        if env("MY_MAIL_3"):
            clients_obj_list.append({
                'email': env("MY_MAIL_3"),
                'surname': 'Антонов',
                'name': 'Сергей',
                'patronym': 'Сергеевич',
                'owner_id': 1,
            })

        # -----------------------------
        # --------Сообщения------------
        # -----------------------------
        message_obj_list = []
        half_count = int(len(self.subjects_list)/2)

        for i in range(half_count):
            message = {
                "subject": self.subjects_list[i],
                "content": self.contents_list[i],
                'owner_id': 2
            }
            message_obj_list.append(message)
        for i in range(half_count, len(self.subjects_list)):
            message = {
                "subject": self.subjects_list[i],
                "content": self.contents_list[i],
                'owner_id': 3
            }
            message_obj_list.append(message)

        Message.truncate()
        message_create_list = [Message(**params) for params in message_obj_list]
        Message.objects.bulk_create(message_create_list)
