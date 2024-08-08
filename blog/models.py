from django.db import models

from config.settings import NULLABLE
from libs.truncate_table_mixin import TruncateTableMixin


# ----- БЛОГ -----
class Blog(TruncateTableMixin, models.Model):
    header = models.CharField(verbose_name="Заголовок", max_length=100)
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(upload_to='images', verbose_name='Изображение', default='empty_file.png', **NULLABLE)
    views_count = models.PositiveIntegerField(verbose_name="Количество просмотров", default=0)
    published_at = models.DateTimeField(verbose_name="Дата первой публикации", auto_now_add=True)

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "блоги"

    def __str__(self):
        return f"{self.header} (опубликован {self.published_at.strftime("%d-%m-%Y %H:%M")})"
