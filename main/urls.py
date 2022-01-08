from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.home),
    path('about/', views.about),
    path('register/', views.register),
    path('login/', views.login),

]
