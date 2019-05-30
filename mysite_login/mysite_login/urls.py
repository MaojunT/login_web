"""mysite_login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# mysite_login/urls.py
 
from django.conf.urls import url
from django.contrib import admin
from login import views
 
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^login/', views.login_view),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),
    url(r'^profile/', views.profile),
    url(r'^profile_update/', views.profile_update),
    url(r'^pwd_update/', views.pwd_update),
    url(r'^index_2/', views.index_2),
    url(r'^index_3/', views.index_3),
]