from django.apps import AppConfig
from config.settings import SCHEDULER_ACTIVE


class LetterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'letters_sending'
    verbose_name = 'Рассылки'

    def ready(self):
        from libs import LettersSendingScheduler

        print(f"ЗАПУСК ПРИЛОЖЕНИЯ {LetterConfig.name.upper()}")
        if SCHEDULER_ACTIVE:
            scheduler = LettersSendingScheduler.get_instance()
            scheduler.start()

