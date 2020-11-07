from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", include("myblogs.urls")),
]
urlpatterns += staticfiles_urlpatterns()
