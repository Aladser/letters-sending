from django.db.models import Model


def seed_table(model:Model, data_list: list):
    """
        Заполняет таблицу БД
        :param model: модель
        :param data_list: массив строк таблицы
    """

    method_obj_list = [model(**param) for param in data_list]
    model.objects.bulk_create(method_obj_list)
