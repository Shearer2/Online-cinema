from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from contact.forms import ContactForm


# Create your views here.
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
