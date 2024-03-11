from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя."""

    # Добавляем поле для работы с изображениями, расширяя родительский класс, указываем, что данное поле не обязательно
    # для заполнения.
    image = models.ImageField(upload_to='users_image', null=True, blank=True)
