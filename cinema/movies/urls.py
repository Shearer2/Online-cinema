from django.urls import path
from movies.views import movies_view, movie_detail, add_review


urlpatterns = [
    path('', movies_view),
    path('<slug:slug>/', movie_detail, name='movie_detail'),
    path('review/<int:pk>/', add_review, name='add_review')
]
