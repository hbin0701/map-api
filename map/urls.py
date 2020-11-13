"""map URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from places import views
from django.urls import path, register_converter

from . import converters

register_converter(converters.FloatUrlParameterConverter, 'float')

urlpatterns = [
    path("placeinfo/", views.place_info),
    path("nearby/", views.get_nearby_places),
    path("process_reviews/<float:x>/<float:y>", views.process_reviews),
    path("process_reviews/", views.process_reviews),
    path("remove/", views.remove_reviews),
    path("edit/", views.edit_reviews),
    path("my_reviews/", views.get_my_reviews),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
]
