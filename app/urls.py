"""safetravels URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^county/(?P<county_id>\d+)/$', views.county_information, name='county_information'),
    url(r'^review/all/(?P<county_id>\d+)/$', views.county_reviews, name='county_reviews'),
    url(r'^review/create/(?P<county_id>\d+)/$', views.review_create, name="review_create"),
    url(r'^review/edit/(?P<review_id>\d+)/$', views.review_edit, name="review_edit"),
    url(r'^review/delete/(?P<review_id>\d+)/$', views.review_delete, name="review_delete"),
]