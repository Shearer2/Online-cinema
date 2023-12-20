from django.urls import path
from movies.views import movies_view, movie_detail, add_review, actor_views, add_rating


app_name = 'movies'

urlpatterns = [
    path('', movies_view, name='movie'),
    path('page/<int:page_number>', movies_view, name='paginator'),
    path('filter/', movies_view, name='filter'),
    path('search/', movies_view, name='search'),
    path('add-rating/', add_rating, name='add_rating'),
    path('<slug:slug>/', movie_detail, name='movie_detail'),
    path('review/<int:pk>/', add_review, name='add_review'),
    path('actor/<str:slug>/', actor_views, name='actor_views'),
]
