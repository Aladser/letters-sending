# Generated by Django 4.2.13 on 2024-08-09 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('letters_sending', '0005_alter_letterssending_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='letterssending',
            options={'permissions': [('deactivate_letterssending', 'Выключить рассылку'), ('view_owner_letterssending', 'Показать свои рассылки'), ('view_owner_stat_letterssending', 'Показать статистику своих рассылок'), ('view_stat_letterssending', 'Показать статистику рассылков')], 'verbose_name': 'Почтовая рассылка', 'verbose_name_plural': 'почтовые рассылки'},
        ),
    ]
