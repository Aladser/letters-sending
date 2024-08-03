from django import db


class TruncateTableMixin:
    """удаление записей таблицы со сбросом автооинкремента"""

    @classmethod
    def truncate(cls):
        """удаляет записи таблицы и сбрасывает автооинкремент"""

        truncate_query = f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE;'
        with db.connection.cursor() as cursor:
            cursor.execute(truncate_query)
