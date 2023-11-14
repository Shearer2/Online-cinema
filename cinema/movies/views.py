from django.shortcuts import render, HttpResponseRedirect
from movies.models import Movie, Category, Actor, Genre
from movies.forms import ReviewForm


# Create your views here.
# Контроллер для показа главной страницы.
def movies_view(request):
    # Делаем вывод только тех фильмов, которые не являются черновиками.
    movies = Movie.objects.filter(draft=False)
    # Делаем вывод всех категорий.
    category = Category.objects.all()
    # Выводим определённое количество фильмов, которые не являются черновиками.
    last_movies = Movie.objects.filter(draft=False).order_by('id')[:5]
    genres = Genre.objects.all()
    context = {
        'movie_list': movies,
        'category_list': category,
        'last_movies': last_movies,
        'genres': genres,
        'movies': movies.values('year')
    }
    return render(request, 'movies/movies_list.html', context)


# Контроллер для вывода описания к фильму.
def movie_detail(request, slug):
    # Получаем номер фильма и по нему из базы данных берём информацию.
    movie = Movie.objects.get(url=slug)
    category = Category.objects.all()
    last_movies = Movie.objects.filter(draft=False).order_by('id')[:5]
    genres = Genre.objects.all()
    movies = Movie.objects.filter(draft=False)
    context = {
        'movie': movie,
        'category_list': category,
        'last_movies': last_movies,
        'genres': genres,
        'movies': movies.values('year')
    }
    return render(request, 'movies/movie_detail.html', context)


# Контроллер для отправки отзывов.
def add_review(request, pk):
    form = ReviewForm(request.POST)
    movie = Movie.objects.get(id=pk)
    if form.is_valid():
        # Вызывая метод save и передавая аргумент commit=False мы указываем, что хотим приостановить сохранение нашей
        # формы.
        form = form.save(commit=False)
        # Ищем в POST запросе ключ parent, который является именем определённого поля, если оно будет, то выполняется
        # данное условие, иначе выполняется None.
        if request.POST.get('parent', None):
            # Достаём значение ключа parent, чтобы прикрепить к отзыву родителя.
            form.parent_id = int(request.POST.get('parent'))
        # В данном поле необходимо указать фильм, к которому мы хотим привязаться.
        # Столбец movie в базе данных обозначен как movie_id, таким образом можно передавать значение для привязки к
        # какому-либо фильму. Если мы будем использовать просто поле movie, то мы можем передавать объект самого фильма.
        #form.movie_id = pk
        # Второй вариант.
        form.movie = movie
        form.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Контроллер для вывода информации об актёрах и режиссёрах.
def actor_views(request, slug):
    slug_field = Actor.objects.get(name=slug)
    genres = Genre.objects.all()
    movies = Movie.objects.filter(draft=False)
    context = {
        'actor': slug_field,
        'genres': genres,
        'movies': movies.values('year')
    }
    return render(request, 'movies/actor.html', context)


# Контроллер для фильтрации фильмов.
def filter_movie(request):
    # Выводим года, которые входят в список всех годов.
    queryset = Movie.objects.filter(year__in=request.GET.getlist('year'))
    context = {
        'queryset': queryset
    }
    return render(request, 'movies/movies_list.html', context)
