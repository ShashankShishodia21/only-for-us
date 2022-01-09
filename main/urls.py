from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('home/', views.home),
    path('about/', views.about),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('choose-semester/', views.semesters),
    path('my-account/', views.my_account),

]
