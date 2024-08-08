import os.path

from django import template
from config.settings import BASE_DIR, MEDIA_URL, STATIC_URL, APP_NAME

register = template.Library()


@register.filter()
def site_name_prefix(value):
    return f"{value} - {APP_NAME}" if value != '' else APP_NAME


@register.filter()
def full_image_path(image_file):
    if image_file != '' and os.path.isfile(BASE_DIR / MEDIA_URL.replace('/', '') / str(image_file)):
        return MEDIA_URL + str(image_file)
    else:
        return STATIC_URL + "empty_file.png"


@register.filter()
def custom_label(value, required_fields):
    if value in required_fields:
        return f"<label class='fw-bolder' title='обязательно для заполнения'>{value}:*</label>"
    else:
        return f"<label>{value}:</label>"


@register.filter()
def custom_status(status):
    if status.description == 'Запущена':
        return f"<div class='text-warning fw-bolder'>{status}</div>"
    elif status.description == 'Завершена':
        return f"<div class='text-success fw-bolder'>{status}</div>"
    else:
        return f"<div>{status}</div>"


@register.filter()
def activation_action(is_active):
    return 'Блокировать' if is_active else 'Активировать'

@register.filter()
def full_image_path(image_file):
    if image_file != '' and os.path.isfile(BASE_DIR / MEDIA_URL.replace('/', '') / str(image_file)):
        return MEDIA_URL + str(image_file)
    else:
        return STATIC_URL + "empty_file.png"