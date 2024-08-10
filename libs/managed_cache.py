from django.core.cache import cache


class ManagedCache:
    """Управляемый кэш"""

    @staticmethod
    def get_data(key, pk):
        """
        Получает данные из кэша
        :param key: ключ хранилища ключей страницы
        :param pk: pk пользователя
        """

        user_key = f'{key}_{pk}'
        # получение хранилищца ключей кэшей
        key_store_list = cache.get(key)

        # извлечение кэша текущего пользователя
        if key_store_list is None:
            cache.set(key, [])
            return None
        elif user_key in key_store_list:
            return cache.get(user_key)

        return None

    @staticmethod
    def save_data(key, pk, data):
        """
        Сохранят данные в кэше
        :param key: ключ хранилища ключей страницы
        :param pk: pk пользователя
        :param data: данные
        """

        user_key = f'{key}_{pk}'

        # обновляет хранилище ключей
        key_store_list = cache.get(key)
        key_store_list.append(user_key)
        cache.set(key, key_store_list)

        # сохраняем страницу пользователя
        cache.set(user_key, data)

    @staticmethod
    def clear_data(key):
        """Очищает кэш страницы"""

        key_store_list = cache.get(key)
        if key_store_list is not None:
            [cache.delete(key) for key in key_store_list]
        cache.delete(key)
