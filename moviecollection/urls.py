from django.urls import path
from .views import *

urlpatterns = [
    path("register/", register,name='register'),
    path("login/", login),
    path("users/", users),
    path("movies/", collction_movies),
    path("movies/<page>/", movie_list),
    path("collection/", collection_list),
    path("collection/<collection_id>/", collection_detail),
    path("request-count/", request_count),
    path("request-count/reset/", reset_request_count),
]
