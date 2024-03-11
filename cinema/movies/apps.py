from django.apps import AppConfig


class MoviesConfig(AppConfig):
    """Настройка фильмов в админ-панели."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
    # Делаем вывод названия таблицы в админ-панели на русском языке.
    verbose_name = "Фильмы"
