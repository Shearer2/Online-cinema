from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from movies.models import Movie, Category, Actor, Genre, Rating, Year
from movies.forms import ReviewForm, RatingForm, ContactForm
# Импортируем модуль для фильтрации по жанрам и годам.
from django.core.paginator import Paginator
from users.models import User
# Подключаем модель для проверки какой пользователь авторизован.
from django.contrib.auth import get_user


# Create your views here.
# Контроллер для показа главной страницы.
def movies_view(request, page_number=1):
    movies = filter_movies(request)
    # Делаем вывод всех категорий.
    category = Category.objects.all()
    # Выводим определённое количество фильмов, которые не являются черновиками.
    last_movies = Movie.objects.filter(draft=False).order_by('id')[:5]
    genres = Genre.objects.all()
    year, genres = genre_year()
    if request.GET.get('q') or request.GET.get('genres') or request.GET.get('year'):
        per_page = len(movies)
    else:
        per_page = 1
    paginator = Paginator(movies, per_page)
    movies_paginator = paginator.page(page_number)
    context = {
        'movie_list': movies_paginator,
        'category_list': category,
        'last_movies': last_movies,
        'genres': genres,
        'year': year,
        'movies': Movie.objects.filter(draft=False).values('year'),
        'form': contact(request)
    }
    return render(request, 'movies/movies_list.html', context)


def genre_year():
    year, genres = [], []
    # Получаю все года и проверяю есть ли фильмы к этим годам, если есть, то добавляю их в список.
    for movie_year in Year.objects.all():
        if len(Movie.objects.filter(draft=False).filter(year__name__in=[movie_year]).order_by('id')):
            year.append(movie_year)
    # Получаю все жанры и проверяю есть ли фильмы по этим жанрам, если есть, то добавляю их в список.
    for genre in Genre.objects.all():
        if len(Movie.objects.filter(draft=False).filter(genres__url__in=[genre.url]).order_by('id')):
            genres.append(genre)
    return year, genres


# Контроллер для вывода описания к фильму.
def movie_detail(request, slug):
    # Получаем номер фильма и по нему из базы данных берём информацию.
    movie = Movie.objects.get(url=slug)
    category = Category.objects.all()
    last_movies = Movie.objects.filter(draft=False).order_by('id')[:5]
    year, genres = genre_year()
    movies = Movie.objects.filter(draft=False)
    context = {
        'movie': movie,
        'category_list': category,
        'last_movies': last_movies,
        'genres': genres,
        'year': year,
        'movies': movies.values('year'),
        'star_form': RatingForm(),
        'form': contact(request)
    }
    return render(request, 'movies/movie_detail.html', context)


# Контроллер для отправки отзывов.
def add_review(request, pk):
    form = ReviewForm(request.POST)
    movie = Movie.objects.get(id=pk)
    # Если пользователь авторизован, то забираю его имя пользователя.
    nickname = get_user(request)
    if form.is_valid():
        # Вызывая метод save и передавая аргумент commit=False мы указываем, что хотим приостановить сохранение нашей
        # формы.
        form = form.save(commit=False)
        # Ищем в POST запросе ключ parent, который является именем определённого поля, если оно будет, то выполняется
        # данное условие, иначе выполняется None.
        if request.POST.get('parent', None):
            # Достаём значение ключа parent, чтобы прикрепить к отзыву родителя.
            form.parent_id = int(request.POST.get('parent'))
        # Если пользователь не является не авторизованным, то получаю всю информацию о нём и забираю аватарку.
        if str(nickname) != 'AnonymousUser':
            user = User.objects.get(username=nickname)
            if user.image:
                form.link_image = '/media/' + str(user.image)
            else:
                form.link_image = '/media/users_image/avatar.jpg'
        else:
            form.link_image = '/media/users_image/avatar.jpg'
        # В данном поле необходимо указать фильм, к которому мы хотим привязаться.
        form.movie = movie
        form.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Контроллер для вывода информации об актёрах и режиссёрах.
def actor_views(request, slug):
    slug_field = Actor.objects.get(name=slug)
    year, genres = genre_year()
    movies = Movie.objects.filter(draft=False)
    # Выводим определённое количество фильмов, которые не являются черновиками.
    last_movies = Movie.objects.filter(draft=False).order_by('id')[:5]
    context = {
        'actor': slug_field,
        'genres': genres,
        'year': year,
        'movies': movies.values('year'),
        'form': contact(request),
        'last_movies': last_movies
    }
    return render(request, 'movies/actor.html', context)


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
    if request.GET.get('rating'):
        # Генерируем форму передавая ей post запрос.
        form = RatingForm(request.POST)
        # Так как один и тот же пользователь не может устанавливать разные рейтинги к одному фильму, то есть если уже
        # был добавлен его рейтинг, то нужно его перезаписать, делаем это после проверки валидности формы.
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
    form = RatingForm(request.POST)
    if form.is_valid():
        print(get_client_ip(request))
        print(int(request.POST.get('movie')))
        print(int(request.POST.get('star')))
        form.ip = get_client_ip(request)
        form.movie = int(request.POST.get('movie'))
        form.star = int(request.POST.get('star'))
        form.save()
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=400)
'''

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


def filter_movies(request):
    # Устанавливаем работу фильтра если был выбран только год.
    if request.GET.get('year') and not request.GET.get('genres'):
        # Делаем вывод фильмов данного года, которые не являются черновиками.
        movies = Movie.objects.filter(draft=False).filter(year__name__in=request.GET.getlist('year')).order_by('id')
    # Устанавливаем работу фильтра если был выбран только жанр.
    elif request.GET.get('genres') and not request.GET.get('year'):
        # Делаем вывод фильмов данного жанра, которые не являются черновиками.
        movies = Movie.objects.filter(draft=False).filter(genres__url__in=request.GET.getlist('genres')).order_by('id')
    # Устанавливаем работу фильтра при выборе года и жанра.
    elif request.GET.get('year') and request.GET.get('genres'):
        # Делаем вывод фильмов по данному жанру и году.
        movies = Movie.objects.filter(draft=False).filter(
            year__name__in=request.GET.getlist('year'), genres__url__in=request.GET.getlist('genres')
        ).order_by('id')
    elif request.GET.get('q'):
        # Фильтруем фильмы по названию без учёта регистра и сравниваем с тем, что пришло в get запросе q.
        movies = Movie.objects.filter(draft=False).filter(title__iregex=request.GET.get('q')).order_by('id')
    else:
        # Делаем вывод только тех фильмов, которые не являются черновиками.
        movies = Movie.objects.filter(draft=False).order_by('id')
    return movies


def contact(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContactForm()
    return form
