from django.urls import path

from . import views
app_name = 'movies'
urlpatterns = [
    ## e.g.: /movies/
    path('', views.index, name='index'),
    
    # e.g.: /movies/5/
    path('<int:movie_id>/', views.detail, name='detail'),
]