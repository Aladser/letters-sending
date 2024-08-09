from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from authen.models import User, Country
from blog.models import Blog
from letters_sending.models import LettersSending, Client, Message


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Group.objects.all().delete()

        client_content_type = ContentType.objects.get_for_model(Client)
        message_content_type = ContentType.objects.get_for_model(Message)
        letters_sending_content_type = ContentType.objects.get_for_model(LettersSending)
        user_content_type = ContentType.objects.get_for_model(User)

        admin_panel_perm = Permission.objects.get(codename='view_admin_panel', content_type=user_content_type)

        view_owner_client_perm = Permission.objects.get(codename='view_owner_client', content_type=client_content_type)
        view_owner_message_perm = Permission.objects.get(codename='view_owner_message', content_type=message_content_type)
        view_owner_letterssending_perm = Permission.objects.get(codename='view_owner_letterssending', content_type=letters_sending_content_type)
        view_owner_stat_letterssending_perm = Permission.objects.get(codename='view_owner_stat_letterssending', content_type=letters_sending_content_type)

        """
        view_*_perm - права на просмотр списка объектов
        view_owner_*_perm - доступ к ListView - контроллерам
        deactivate_letterssending - выключить рассылку
        block_user - блокировать пользователя
        """

        # Группа менеджеров
        interface_managers_group, created = Group.objects.get_or_create(name='interface_manager')
        interface_manager_permissions = (
            Permission.objects.get(codename='view_client', content_type=client_content_type),
            Permission.objects.get(codename='view_message', content_type=message_content_type),
            Permission.objects.get(codename='view_letterssending', content_type=letters_sending_content_type),
            Permission.objects.get(codename='view_stat_letterssending', content_type=letters_sending_content_type),

            view_owner_client_perm,
            view_owner_message_perm,
            view_owner_letterssending_perm,
            view_owner_stat_letterssending_perm,

            Permission.objects.get(codename='view_user', content_type=user_content_type),
            Permission.objects.get(codename='deactivate_letterssending', content_type=letters_sending_content_type),
            Permission.objects.get(codename='block_user', content_type=user_content_type),

            admin_panel_perm
        )
        [interface_managers_group.permissions.add(perm) for perm in interface_manager_permissions]

        # Группа пользователей
        users_group, created = Group.objects.get_or_create(name='user')
        user_permissions = (
            Permission.objects.get(codename='add_client', content_type=client_content_type),
            Permission.objects.get(codename='change_client', content_type=client_content_type),
            Permission.objects.get(codename='delete_client', content_type=client_content_type),

            Permission.objects.get(codename='add_message', content_type=message_content_type),
            Permission.objects.get(codename='change_message', content_type=message_content_type),
            Permission.objects.get(codename='delete_message', content_type=message_content_type),

            Permission.objects.get(codename='add_letterssending', content_type=letters_sending_content_type),
            Permission.objects.get(codename='change_letterssending', content_type=letters_sending_content_type),
            Permission.objects.get(codename='delete_letterssending', content_type=letters_sending_content_type),

            view_owner_client_perm,
            view_owner_message_perm,
            view_owner_letterssending_perm,
            view_owner_stat_letterssending_perm
        )
        [users_group.permissions.add(perm) for perm in user_permissions]

        # Группа блогеров
        blog_content_type = ContentType.objects.get_for_model(Blog)
        blogers_group, created = Group.objects.get_or_create(name='bloger')
        bloger_permissions = (
            Permission.objects.get(codename='view_blog', content_type=blog_content_type),
            Permission.objects.get(codename='add_blog', content_type=blog_content_type),
            Permission.objects.get(codename='change_blog', content_type=blog_content_type),
            Permission.objects.get(codename='delete_blog', content_type=blog_content_type),

            admin_panel_perm
        )
        [blogers_group.permissions.add(perm) for perm in bloger_permissions]

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
        user.groups.add(users_group)
        user.save()

        # менеджер
        user = User.objects.create(
            email='manager@test.ru',
            country=russia_model,
            first_name='Менеджер',
            last_name='Интерфейса',
            is_staff = True
        )

        user.set_password("manager@123")
        user.groups.add(interface_managers_group)
        user.save()

        # блогер
        user = User.objects.create(
            email='bloger@test.ru',
            country=russia_model,
            first_name='Блогер',
            last_name='Великий',
            is_staff=True
        )

        user.set_password("bloger@123")
        user.groups.add(blogers_group)
        user.save()
