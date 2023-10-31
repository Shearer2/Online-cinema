from django.shortcuts import render
from movies.models import Movie


# Create your views here.
def movies_view(request):
    # Делаем вывод только тех фильмов, которые не являются черновиками.
    movies = Movie.objects.filter(draft=False)
    context = {
        'movie_list': movies
    }
    return render(request, 'movies/movies_list.html', context)


def movie_detail(request, slug):
    # Получаем номер фильма и по нему из базы данных берём информацию.
    movie = Movie.objects.get(url=slug)
    context = {
        'movie': movie
    }
    return render(request, 'movies/movie_detail.html', context)

