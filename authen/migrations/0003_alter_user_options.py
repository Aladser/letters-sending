# Generated by Django 4.2.13 on 2024-08-08 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authen', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('first_name', 'last_name', 'email'), 'permissions': [('block_user', 'Блокировать')], 'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
    ]