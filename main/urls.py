from django.urls import path
from . import views

app_name = "main"   


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
    path("rating/", views.rating_request, name= "rating"),
    path("recommendation/", views.recommendation_request, name= "recommendation"),
    path('movies/<int:id>/', views.movie_detail, name='movies'),

]
