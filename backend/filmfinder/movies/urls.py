from django.urls import path

from . import views
app_name = 'movies'
urlpatterns = [
    ## e.g.: /movies/
    path('', views.movie_list_view, name='movie_list_view'),
    
    # e.g.: /movies/detail/
    path('detail/', views.detail_view, name='detail_view'),
    
     # e.g.: /movies/detail/all_reviews/
    path('detail/all_reviews/', views.all_reviews_view, name='all_reviews_view'),
    
    #e.g.: /movies/detail/new_review/
    path('detail/new_review/', views.new_review_view, name = 'new_review_view'),
]