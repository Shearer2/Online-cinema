from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from movies.models import Movie, Category, Actor, Genre, Rating
from movies.forms import ReviewForm, RatingForm
# Импортируем модуль для фильтрации по жанрам и годам.
#from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
# Контроллер для показа главной страницы.
def movies_view(request):
    # Делаем вывод только тех фильмов, которые не являются черновиками.
    movies = Movie.objects.filter(draft=False).order_by('id')
    # Делаем вывод всех категорий.
    category = Category.objects.all()
    # Выводим определённое количество фильмов, которые не являются черновиками.
    last_movies = Movie.objects.filter(draft=False).order_by('id')[:5]
    genres = Genre.objects.all()
    #per_page = 1
    #paginator = Paginator(movies, per_page)
    #movies_paginator = paginator.page(page_number)
    # Фильтруем фильмы по названию без учёта регистра и сравниваем с тем, что пришло в get запросе q.
    #name_movies = Movie.objects.filter(title__icontains=request.GET.get('q'))
    context = {
        'movie_list': movies,
        'category_list': category,
        'last_movies': last_movies,
        'genres': genres,
        'movies': movies.values('year'),
        #'movie_pag': movies_paginator,
        #'q': request.GET.get('q')
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
        'movies': movies.values('year'),
        'star_form': RatingForm()
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
    if request.method == 'POST':
        # Делаем вывод только тех фильмов, которые не являются черновиками.
        movies = Movie.objects.filter(draft=False)
    # Устанавливаем работу фильтра если был выбран только год.
    elif request.GET.get('year') and not request.GET.get('genres'):
        # Если использовать данный способ, то при выборе жанра и года выведутся все фильмы данного жанра, вне
        # зависимости от года. Если нужно выводить что-то именно, то нужно указывать через запятую.
        #movies = Movie.objects.filter(draft=False).filter(
        #    Q(year__in=request.GET.getlist('year')) |
        #    Q(genres__in=request.GET.getlist('genres'))
        #)
        # Делаем вывод фильмов данного года, которые не являются черновиками.
        movies = Movie.objects.filter(draft=False).filter(year__in=request.GET.getlist('year'))
    # Устанавливаем работу фильтра если был выбран только жанр.
    elif request.GET.get('genres') and not request.GET.get('year'):
        # Делаем вывод фильмов данного жанра, которые не являются черновиками.
        movies = Movie.objects.filter(draft=False).filter(genres__in=request.GET.getlist('genres'))
    # Устанавливаем работу фильтра при выборе года и жанра.
    else:
        # Делаем вывод фильмов по данному жанру и году.
        movies = Movie.objects.filter(draft=False).filter(
            year__in=request.GET.getlist('year'), genres__in=request.GET.getlist('genres')
        )
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
        'movies': Movie.objects.filter(draft=False).values('year')
    }
    return render(request, 'movies/movies_list.html', context)


# Контроллер для получения ip-адреса пользователя, который отправил запрос.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Добавляем возможность устанавливать рейтинг фильма.
def add_rating(request):
    # Генерируем форму передавая ей post запрос.
    form = RatingForm(request.POST)
    # Так как один и тот же пользователь не может устанавливать разные рейтинги к одному фильму, то есть если уже был
    # добавлен его рейтинг, то нужно его перезаписать, делаем это после проверки валидности формы.
    if form.is_valid():
        # Используем update_or_create чтобы можно было либо создавать запись, либо обновлять её если она уже была
        # создана.
        Rating.objects.update_or_create(
            ip=get_client_ip(request),
            movie_id=int(request.POST.get('movie')),
            defaults={'star_id': int(request.POST.get('star'))}
        )
        form.save()
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)


'''
def add_rating(request):
    if request.method == 'POST':
        form = RatingForm(data=request.POST)
        if form.is_valid():
            rating_star = request.POST['star']
            form[rating_star].save()
    else:
        form = RatingForm()
    context = {'form': form}
    return render(request, 'movies/movie_detail.html', context)
'''
