from django.shortcuts import render, redirect
from movies.models import Movie, MovieShots


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
    print(request.POST)
    return redirect('/')

