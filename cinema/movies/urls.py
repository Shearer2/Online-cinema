from django.urls import path
from movies.views import movies_view, movie_detail


urlpatterns = [
    path('', movies_view),
    path('<slug:slug>/', movie_detail, name='movie_detail')
]
