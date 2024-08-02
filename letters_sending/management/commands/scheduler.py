from time import sleep

from apscheduler.schedulers import SchedulerAlreadyRunningError
from django.core.management import BaseCommand
from config.settings import SCHEDULER_INTERVAL
from libs import LettersSendingScheduler


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            scheduler = LettersSendingScheduler.get_instance()
            scheduler.start()
            while True:
                sleep(SCHEDULER_INTERVAL)
        except SchedulerAlreadyRunningError as e:
            print("Планировщик уже запущен")
