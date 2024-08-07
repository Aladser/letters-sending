from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from authen.models import User
from letters_sending.models import LettersSending


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Group.objects.all().delete()

        # Группа менеджеров
        interface_managers_group, created = Group.objects.get_or_create(name='interface_manager')

        letters_sending_content_type = ContentType.objects.get_for_model(LettersSending)
        view_letterssending_perm = Permission.objects.get(
            codename='view_letterssending', content_type=letters_sending_content_type)
        activate_letterssending_perm = Permission.objects.get(
            codename='activate_letterssending', content_type=letters_sending_content_type)

        user_content_type = ContentType.objects.get_for_model(User)
        view_user_perm = Permission.objects.get(codename='view_user', content_type=user_content_type)
        activate_user_perm = Permission.objects.get(codename='activate_user', content_type=user_content_type)

        interface_managers_group.permissions.add(view_letterssending_perm)
        interface_managers_group.permissions.add(activate_letterssending_perm)
        interface_managers_group.permissions.add(view_user_perm)
        interface_managers_group.permissions.add(activate_user_perm)
