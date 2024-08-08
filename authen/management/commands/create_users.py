from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from authen.models import User, Country
from letters_sending.models import LettersSending


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Group.objects.all().delete()

        # Группа менеджеров
        interface_managers_group, created = Group.objects.get_or_create(name='interface_manager')

        letters_sending_content_type = ContentType.objects.get_for_model(LettersSending)
        user_content_type = ContentType.objects.get_for_model(User)
        view_letterssending_perm = Permission.objects.get(codename='view_letterssending', content_type=letters_sending_content_type)
        activate_letterssending_perm = Permission.objects.get(codename='deactivate_letterssending', content_type=letters_sending_content_type)
        view_user_perm = Permission.objects.get(codename='view_user', content_type=user_content_type)
        activate_user_perm = Permission.objects.get(codename='block_user', content_type=user_content_type)

        interface_managers_group.permissions.add(view_letterssending_perm)
        interface_managers_group.permissions.add(activate_letterssending_perm)
        interface_managers_group.permissions.add(view_user_perm)
        interface_managers_group.permissions.add(activate_user_perm)

        # страны пользователей
        country_obj_list = [
            {'name': 'russia', 'description': 'Россия'},
            {'name': 'ukraine', 'description': 'Украина'},
            {'name': 'belarus', 'description': 'Беларусь'},
            {'name': 'kazakhstan', 'description': 'Казахстан'},
            {'name': 'armenia', 'description': 'Армения'},
        ]
        Country.truncate()
        Country.objects.bulk_create([Country(**param) for param in country_obj_list])
        russia_model = Country.objects.get(name='russia')

        # суперпользователь
        User.truncate()
        user = User.objects.create(
            email='admin@test.ru',
            country=russia_model,
            first_name='Админ',
            last_name='Админов',
            is_superuser=True,
            is_staff=True
        )

        user.set_password("admin@123")
        user.save()

        # обычный пользователь
        user = User.objects.create(
            email='user@test.ru',
            country=russia_model,
            first_name='Пользователь',
            last_name='Обычный'
        )

        user.set_password("user@123")
        user.save()

        # менеджер
        user = User.objects.create(
            email='manager@test.ru',
            country=russia_model,
            first_name='Менеджер',
            last_name='Интерфейса'
        )

        user.set_password("manager@123")
        user.groups.add(interface_managers_group)
        user.save()
