from modeltranslation.translator import register, TranslationOptions
from movies.models import Category, Actor, Movie, Genre, MovieShots


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    # Указываем те поля, которые хотим чтобы участвовали в переводе.
    fields = ('name', 'description')


@register(Actor)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Genre)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Movie)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'tagline', 'description', 'country')


@register(MovieShots)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

