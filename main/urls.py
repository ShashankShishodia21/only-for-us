from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('home/', views.home),
    path('about/', views.about),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('choose-semester/', views.semesters),
    path('choose-subject/<semester>/', views.subjects),
    path('tutorials/<subject>/', views.tutorials),
    path('polls/', views.polls),
    path('my-account/', views.my_account),
    path('terms/', views.terms),
    path('poll-voting/<poll_id>/<poll_topic>/', views.poll_voting),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
