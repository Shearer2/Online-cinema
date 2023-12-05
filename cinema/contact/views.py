from django.shortcuts import render
from django.views.generic import CreateView
from contact.models import Contact
from contact.forms import ContactForm


# Create your views here.
class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    # Перенаправляем пользователя на главную страницу после успешной отправки формы.
    success_url = '/'
