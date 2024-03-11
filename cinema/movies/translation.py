from modeltranslation.translator import register, TranslationOptions
from movies.models import Category, Actor, Movie, Genre, MovieShots


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    """Перевод категорий."""

    # Указываем те поля, которые хотим чтобы участвовали в переводе.
    fields = ('name', 'description')


@register(Actor)
class ActorTranslationOptions(TranslationOptions):
    """Перевод актёров."""

    fields = ('name', 'description')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    """Перевод жанров фильмов."""

    fields = ('name', 'description')


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    """Перевод фильмов."""

    fields = ('title', 'tagline', 'description', 'country')


@register(MovieShots)
class MovieShotsTranslationOptions(TranslationOptions):
    """Перевод кадров фильмов."""

    fields = ('title', 'description')

