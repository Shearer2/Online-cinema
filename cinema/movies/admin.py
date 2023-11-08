from django.contrib import admin
from django.utils.safestring import mark_safe
from movies.models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории фильмов."""

    list_display = ('id', 'name', 'url')
    # Чтобы переходить в редактирование категории по заданному полю.
    list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
    """Добавление отзывов в редактировании фильмов."""

    model = Reviews
    readonly_fields = ('name', 'email')
    extra = 0


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Отображение фильмов."""

    list_display = ('title', 'category', 'url', 'draft', 'get_poster')
    fields = (
        'title', 'description', ('poster', 'get_poster'), 'year', 'country', 'directors', 'actors', 'genres',
        'world_premiere', 'budget', 'fees_in_usa', 'fees_in_world', 'category', 'url', 'draft'
    )
    # Добавляем фильтрацию фильмов по категории.
    list_filter = ('category',)
    # Делаем поиск по названию фильма.
    search_fields = ('title',)
    # Выстраиваем фильмы в алфавитном порядке.
    ordering = ('title',)
    # Подключаем отзывы к фильму.
    inlines = (ReviewInline,)
    # Переносим меню с сохранением вверх, чтобы не пролистывать все отзывы.
    save_on_top = True
    # Если нужно изменить только несколько полей, а остальная информация дублируется, то добавляем save_as, который
    # позволяет сохранять информацию как новый объект.
    save_as = True
    # Чтобы можно было редактировать определённое поле с галочкой, например, черновик, необходимо использовать
    # list_editable.
    list_editable = ('draft',)
    readonly_fields = ('get_poster',)

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="60" height="50">')

    get_poster.short_description = "Постер"


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Отзывы к фильмам."""

    list_display = ('name', 'email', 'parent', 'movie')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры фильмов."""

    list_display = ('name', 'url')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильмов."""

    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="60" height="50">')

    get_image.short_description = "Изображение"


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актёры."""

    # Добавляем сюда имя нашего метода.
    list_display = ('name', 'age', 'get_image')
    # Чтобы выводить в редактировании не ссылку на изображение, а само изображение.
    readonly_fields = ('get_image',)

    # Добавляем метод для вывода изображений, а не просто ссылок, в админ-панели.
    def get_image(self, obj):
        # Метод mark_safe выводит html не как строку, а как тег.
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    # Пишем описание, как будет называться наш столбец.
    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг фильмов."""

    list_display = ('star', 'movie')


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    """Количество звёзд у фильмов."""

    list_display = ('value',)

