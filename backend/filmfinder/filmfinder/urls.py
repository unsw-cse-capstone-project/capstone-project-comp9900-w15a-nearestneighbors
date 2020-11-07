"""filmfinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from login.views import index_view, login_view, register_view, logout_view, browse_by_genre_view, browse_by_director_view
from movies.views import search_view
from movies.views import my_page_view, my_wishlist_view, remove_from_wishlist_view, others_wishlist_view
from movies.views import my_reviews_view, get_review_view, new_review_view, delete_review_view, edit_review_view
from movies.views import add_to_bannedlist_view, my_bannedlist_view, remove_from_bannedlist_view
from movies.views import others_page_view, others_reviews_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),

    path('index/', index_view),
    path('browse_by_genre/', browse_by_genre_view),
    path('browse_by_director/', browse_by_director_view),

    path('login/', login_view),
    path('register/', register_view),
    path('logout/', logout_view),
    path('search/', search_view),

    path('my_page/', my_page_view),
    path('my_page/my_wishlist/', my_wishlist_view),
    path('my_page/my_wishlist/remove_from_wishlist/', remove_from_wishlist_view),

    path('new_review/', new_review_view),
    path('my_page/my_reviews/',my_reviews_view),
    path('my_page/my_reviews/get_review/', get_review_view),
    path('my_page/my_reviews/get_review/delete_review/', delete_review_view),
    path('my_page/my_reviews/get_review/edit_review/', edit_review_view),
    
    path('my_page/my_bannedlist/', my_bannedlist_view),
    path('user_page/add_to_bannedlist/', add_to_bannedlist_view),
    path('my_page/my_bannedlist/remove_from_bannedlist/',remove_from_bannedlist_view),

    path('user_page/', others_page_view),
    path('user_page/user_wishlist/', others_wishlist_view),
    path('user_page/user_reviews/', others_reviews_view),
    
    #URL for showing all movies, movies detail,
    #add to wishlist, view all reviews for a specific movie,
    #create a new review for a specific movie
    path('movies/', include('movies.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  #movies poster images

urlpatterns += staticfiles_urlpatterns()