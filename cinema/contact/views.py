from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView
from contact.models import Contact
from contact.forms import ContactForm

'''
# Create your views here.
class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    # Перенаправляем пользователя на главную страницу после успешной отправки формы.
    success_url = '/'
'''


def contact(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('contact'))
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'movies/footer.html', context)
