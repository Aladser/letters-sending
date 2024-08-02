from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from blog.models import Blog
from product.models import Product


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Группа модераторов товаров
        product_moderators_group, created = Group.objects.get_or_create(name='product_moderator')
        product_content_type = ContentType.objects.get_for_model(Product)

        cancel_publication_permission = Permission.objects.get(codename='cancel_publication', content_type=product_content_type)
        edit_description_permission = Permission.objects.get(codename='edit_description', content_type=product_content_type)
        edit_category_permission = Permission.objects.get(codename='edit_category', content_type=product_content_type)

        product_moderators_group.permissions.add(cancel_publication_permission)
        product_moderators_group.permissions.add(edit_description_permission)
        product_moderators_group.permissions.add(edit_category_permission)

        # группа контент-менеджеров
        content_managers_group, created = Group.objects.get_or_create(name='content_manager')
        blog_content_type = ContentType.objects.get_for_model(Blog)
        set_publication_permission = Permission.objects.get(codename='set_publication', content_type=blog_content_type)
        content_managers_group.permissions.add( set_publication_permission)
