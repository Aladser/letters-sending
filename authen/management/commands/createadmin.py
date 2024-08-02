from django.core.management import BaseCommand

from authen.models import User, Country


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        country_obj_list = [
            {'pk': 1, 'name': 'russia', 'description': 'Россия'},
            {'pk': 2, 'name': 'ukraine', 'description': 'Украина'},
            {'pk': 3, 'name': 'belarus', 'description': 'Беларусь'},
            {'pk': 4, 'name': 'kazakhstan', 'description': 'Казахстан'},
            {'pk': 5, 'name': 'armenia', 'description': 'Армения'},
        ]

        Country.objects.all().delete()
        Country.objects.bulk_create([Country(**param) for param in country_obj_list])
        russia_model = Country.objects.get(name='russia')

        User.objects.all().delete()
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

