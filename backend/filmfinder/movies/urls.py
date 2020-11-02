from django.urls import path

from . import views
app_name = 'movies'
urlpatterns = [
    ## e.g.: /movies/
    path('', views.movie_list_view, name='movie_list_view'),
    
    # e.g.: /movies/detail/
    path('detail/', views.detail_view, name='detail_view'),
]