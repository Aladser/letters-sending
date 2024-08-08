from django.apps import AppConfig
from config.settings import SCHEDULER_ACTIVE


class LetterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'letters_sending'
    verbose_name = 'Почтовые рассылки'

    def ready(self):
        from letters_sending.services.letsend_schedulrer import LettersSendingScheduler

        print(f"ЗАПУСК ПРИЛОЖЕНИЯ {LetterConfig.name.upper()}")
        if SCHEDULER_ACTIVE:
            scheduler = LettersSendingScheduler.get_instance()
            scheduler.start()
