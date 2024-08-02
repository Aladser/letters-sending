from django.db import models
from config.settings import NULLABLE


class Message(models.Model):
    """Сообщение"""

    subject = models.CharField(verbose_name="Заголовок", max_length=100)
    content = models.TextField(verbose_name="Содержание")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "сообщения"
        ordering = ("subject",)

    def __str__(self):
        return self.subject


class Client(models.Model):
    """Клиент"""

    email = models.EmailField(verbose_name="Почта", unique=True)
    surname = models.CharField(verbose_name="Фамилия", max_length=100)
    name = models.CharField(verbose_name="Имя", max_length=100)
    patronym = models.CharField(verbose_name="Отчество", max_length=100, **NULLABLE)
    comment = models.CharField(verbose_name="Комментарий", max_length=255, **NULLABLE)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "клиенты"
        ordering = ("surname", "name", "patronym", "email")

    def __str__(self):
        if self.patronym:
            return f"{self.surname} {self.name} {self.patronym} ({self.email})"
        else:
            return f"{self.surname} {self.name} ({self.email})"


class DatePeriod(models.Model):
    """Интервал отправки"""

    name = models.CharField(verbose_name="Название", max_length=30)
    description = models.CharField(verbose_name="Описание", max_length=100)
    interval = models.PositiveIntegerField(verbose_name="Интервал (в секундах)")

    class Meta:
        verbose_name = "Интервал рассылки"
        verbose_name_plural = "интервалы рассылки"
        ordering = ("pk",)

    def __str__(self):
        return self.description


class Status(models.Model):
    """Статус рассылки"""

    name = models.CharField(verbose_name="Название", max_length=10)
    description = models.CharField(verbose_name="Описание", max_length=100)

    class Meta:
        verbose_name = "Статус рассылки"
        verbose_name_plural = "статусы рассылки"
        ordering = ("pk",)

    def __str__(self):
        return self.description


class LettersSending(models.Model):
    """Рассылка"""

    message = models.ForeignKey(
        to=Message,
        on_delete=models.CASCADE,
        related_name="message",
        verbose_name="Сообщение",
    )
    clients = models.ManyToManyField(Client, verbose_name="Клиенты")
    period = models.ForeignKey(
        to=DatePeriod,
        on_delete=models.CASCADE,
        related_name="newsletter_period",
        verbose_name="Интервал",
    )
    status = models.ForeignKey(
        to=Status,
        on_delete=models.CASCADE,
        related_name="newsletter_status",
        verbose_name="Статус",
        default=1,
    )
    first_sending = models.DateTimeField(verbose_name="Дата и время первой отправки", **NULLABLE)
    next_sending = models.DateTimeField(verbose_name="Дата и время следующей отправки", **NULLABLE)

    class Meta:
        verbose_name = "Почтовая рассылка"
        verbose_name_plural = "почтовые рассылки"
        ordering = ("pk",)

    def __str__(self):
        clients_list = ", ".join([client.email for client in self.clients.all()])
        return f"{self.message} - {clients_list}"


class Attempt(models.Model):
    """Попытка рассылки"""

    letters_sending = models.ForeignKey(
        to=LettersSending,
        on_delete=models.CASCADE,
        related_name="letters_sending",
        verbose_name="Рассылка",
    )
    recipient = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE,
        related_name="recipient",
        verbose_name="Получатель",
    )
    created_at = models.DateTimeField(verbose_name="Дата и время", auto_now_add=True)
    is_sent = models.BooleanField(verbose_name="Отправлен")
    response = models.CharField(verbose_name="Ответ сервера", max_length=255, **NULLABLE)

    class Meta:
        verbose_name = "Попытка отправки"
        verbose_name_plural = "попытки отправки"
        ordering = ("created_at", "is_sent")

    def __str__(self):
        return f"{self.letters_sending.pk} \"{self.letters_sending.message}\" - {self.response}"
