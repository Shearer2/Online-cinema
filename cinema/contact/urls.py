from django.urls import path
#from contact.views import ContactView
from contact.views import contact


urlpatterns = [
    #path('', ContactView.as_view(), name='contact')
    path('', contact, name='contact')
]
