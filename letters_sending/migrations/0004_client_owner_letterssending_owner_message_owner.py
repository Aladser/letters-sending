# Generated by Django 4.2.13 on 2024-08-07 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('letters_sending', '0003_alter_letterssending_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clients', to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.AddField(
            model_name='letterssending',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sendings', to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.AddField(
            model_name='message',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
    ]