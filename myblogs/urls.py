from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from myblogs import views

from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from myblogs import views
from django.urls import path
 
#The new django.urls.path() function allows a simpler, more readable URL routing syntax.

 
urlpatterns = [
    path("", views.home, name="home"),
    path('count_words.html', views.count_words),
]

urlpatterns += staticfiles_urlpatterns()

 