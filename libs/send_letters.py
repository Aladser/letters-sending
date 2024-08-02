import smtplib
from datetime import datetime, timedelta
from django.core.mail import send_mail
from config.settings import DATETIME_FORMAT, EMAIL_HOST_USER
from letters_sending.models import Attempt, LettersSending


def log(task, client, response):
    print(f"\"{task.message}\" - {client.email}: {response}")


def send_letters(task: LettersSending):
    """Запускает рассылку сообщений"""

    print(f"Рассылка {task.pk} \"{task.message}\"")
    attempt_params_obj = {"letters_sending": task}
    for client in task.clients.all():
        attempt_params_obj["recipient"] = client
        try:
            # ***** отправка сообщения *****
            response = send_mail(
                task.message.subject,
                task.message.content,
                EMAIL_HOST_USER,
                (client.email,),
            )

            if response == 1:
                attempt_params_obj["is_sent"] = True
                response = "Отправлено"
                attempt_params_obj["response"] = response
                log(task, client, response)
            else:
                attempt_params_obj["is_sent"] = False
                attempt_params_obj["response"] = response
                log(task, client, response)
        except smtplib.SMTPException as e:
            error_str = str(e).split(" ")
            if "Message rejected under suspicion of SPAM;" in str(e):
                # ошибка спама
                error_str = error_str[2:len(error_str)-2]
            else:
                error_str = error_str[2:len(error_str)-1]
            error_str = ' '.join(error_str)

            attempt_params_obj["is_sent"] = False
            attempt_params_obj["response"] = error_str
            log(task, client, f"SMTPException = {error_str}")
        except Exception as e:
            print(e)
            return
        finally:
            Attempt.objects.create(**attempt_params_obj)

    task.next_sending = datetime.now() + timedelta(seconds=task.period.interval)
    task.save()
    print(f"Следующая отправка сообщений: {task.next_sending.strftime(DATETIME_FORMAT)}", end="\n\n")
