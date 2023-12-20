from django.shortcuts import render, HttpResponseRedirect
# Импортируем приложение auth, чтобы узнать существует ли пользователь.
from django.contrib import auth, messages
from django.urls import reverse
# Импортируем класс, чтобы присоединить форму к приложению.
from users.forms import UserLoginForm, UserRegistrationForm


# Create your views here.
# Контроллер для авторизации.
def login(request):
    # Чтобы проверить какой запрос пришёл необходимо сделать условие, так как данная страница будет работать на два
    # запроса, предоставление информации пользователю GET и получение информации о пользователе POST.
    if request.method == 'POST':
        # Если происходит POST запрос на получение информации о клиенте сервером, то необходимо передавать данные.
        form = UserLoginForm(data=request.POST)
        # Необходимо делать проверку на валидность.
        if form.is_valid():
            # если данные проходят валидацию, то необходимо достать данные, которые пришли.
            username = request.POST['username']
            password = request.POST['password']
            # Чтобы узнать есть ли данный пользователь в базе данных передаём его имя и пароль.
            user = auth.authenticate(username=username, password=password)
            # Если пользователь есть, то мы его авторизуем, передавая запрос и пользователя.
            if user:
                auth.login(request, user)
                # Перенаправляем пользователя после авторизации на главную страницу.
                return HttpResponseRedirect(reverse('movies:movie'))
    else:
        # Если происходит GET запрос, то возвращаем нашу форму.
        form = UserLoginForm()
    # Обращаемся через ключ к нашей форме, чтобы она отображалась.
    context = {'form': form}
    return render(request, 'users/login.html', context)


# Контроллер для регистрации.
def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            # Если форма валидна, то необходимо сохранить объект в базе данных.
            form.save()
            # Выводим сообщение пользователю об успешной регистрации.
            messages.success(request, 'Поздравляем! Вы успешно зарегистрировались!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


# Контроллер для выхода из системы.
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('movies:movie'))
