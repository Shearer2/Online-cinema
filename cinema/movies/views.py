from django.shortcuts import render, redirect
from movies.models import Movie
from movies.forms import ReviewForm


# Create your views here.
# Контроллер для показа главной страницы.
def movies_view(request):
    # Делаем вывод только тех фильмов, которые не являются черновиками.
    movies = Movie.objects.filter(draft=False)
    context = {
        'movie_list': movies
    }
    return render(request, 'movies/movies_list.html', context)


# Контроллер для вывода описания к фильму.
def movie_detail(request, slug):
    # Получаем номер фильма и по нему из базы данных берём информацию.
    movie = Movie.objects.get(url=slug)
    context = {
        'movie': movie
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
        # В данном поле необходимо указать фильм, к которому мы хотим привязаться.
        # Столбец movie в базе данных обозначен как movie_id, таким образом можно передавать значение для привязки к
        # какому-либо фильму. Если мы будем использовать просто поле movie, то мы можем передавать объект самого фильма.
        #form.movie_id = pk
        # Второй вариант.
        form.movie = movie
        form.save()
    return redirect(movie.get_absolute_url())

