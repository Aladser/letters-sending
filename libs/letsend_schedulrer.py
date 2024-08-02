from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from config.settings import DATETIME_FORMAT, SCHEDULER_INTERVAL
from letters_sending.models import Status, LettersSending
from libs.send_letters import send_letters


class LettersSendingScheduler:
    """Планировщик рассылки сообщений"""

    __instance = False

    @staticmethod
    def job() -> None:
        status_launched = Status.objects.get(name="launched")
        launched_letters_sendings = LettersSending.objects.filter(status=status_launched, next_sending__lte=datetime.now())
        print(f"{datetime.now().strftime(DATETIME_FORMAT)} Число рассылок = {len(launched_letters_sendings)}")
        [send_letters(sending) for sending in launched_letters_sendings]

    @staticmethod
    def get_instance() -> BackgroundScheduler:
        if not LettersSendingScheduler.__instance:
            LettersSendingScheduler.__instance = BackgroundScheduler()
            LettersSendingScheduler.__instance.add_jobstore(DjangoJobStore(), "default")
            LettersSendingScheduler.__instance.add_job(
                func=LettersSendingScheduler.job,
                trigger='interval',
                id=f"send_letters",
                next_run_time=datetime.now(),
                replace_existing=True,
                seconds=SCHEDULER_INTERVAL)
        return LettersSendingScheduler.__instance
