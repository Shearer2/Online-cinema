from django.contrib import admin
from movies.models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    # Чтобы переходить в редактирование категории по заданному полю.
    list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
    model = Reviews
    readonly_fields = ('name', 'email')
    extra = 0


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
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


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('ip', 'star', 'movie')


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('value',)

