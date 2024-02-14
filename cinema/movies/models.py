from django.db import models
from datetime import date


# Create your models here.
# Модель для распределения фильмов по категориям.
class Category(models.Model):
    name = models.CharField('Категория', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# Модель для информации об актёрах и режиссёрах.
class Actor(models.Model):
    name = models.CharField('Имя', max_length=100)
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='actors/')
    link_video = models.CharField(verbose_name='Ссылка на видео', max_length=160, default='')
    link_image = models.CharField(verbose_name='Ссылка на изображение', max_length=160, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актёры и режиссёры'
        verbose_name_plural = 'Актёры и режиссёры'


# Модель для жанров фильмов.
class Genre(models.Model):
    name = models.CharField('Жанр', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


# Модель для годов фильмов.
class Year(models.Model):
    name = models.CharField('Год', max_length=4)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Год'
        verbose_name_plural = 'Года'


# Модель для фильмов.
class Movie(models.Model):
    title = models.CharField('Название', max_length=100)
    tagline = models.CharField('Слоган', max_length=100, default='')
    description = models.TextField('Описание')

    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.ManyToManyField(Year, verbose_name='Дата выхода')
    country = models.CharField('Страна', max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name='режиссёр', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='актёры', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='жанры')
    world_premiere = models.DateField('Премьера в мире', default=date.today)
    budget = models.PositiveIntegerField('Бюджет', default=0, help_text='')
    fees_in_usa = models.PositiveIntegerField('Сборы в США', default=0, help_text='указывать сумму в долларах')
    fees_in_world = models.PositiveIntegerField('Сборы в мире', default=0, help_text='указывать сумму в долларах')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField('Черновик', default=False)
    link_video = models.CharField(verbose_name='Ссылка на видео', max_length=160, default='')
    link_image = models.CharField(verbose_name='Ссылка на изображение', max_length=160, default='')

    def __str__(self):
        return self.title

    # Данный метод возвращает список отзывов, прикреплённых к фильму, с фильтрацией по полю parent со значением Null.
    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


# Модель для кадров из фильмов.
class MovieShots(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='movie_shots/')
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'


# Модель рейтинга.
class RatingStar(models.Model):
    value = models.SmallIntegerField('Значение', default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звёзды рейтинга'
        # Чтобы выводить звёзды всегда отсортированные в нужном порядке указываем ordering с value.
        ordering = ('-value',)


class Rating(models.Model):
    ip = models.CharField('IP адрес', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='звезда')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='фильм')

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


# Модель отзывов к фильму.
class Reviews(models.Model):
    # EmailField это CharField, который проверяет, что значение является действительно адресом электронной почты.
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    # self указывает, что запись будет ссылаться на запись в этой же таблице.
    # Поле не является обязательным для заполнения.
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    # Каскадное удаление удалит отзыв вместе с фильмом.
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)
    link_image = models.CharField(verbose_name='Ссылка на изображение', max_length=160, default='')

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Contact(models.Model):
    """Подписка по email"""
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
