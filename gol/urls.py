"""gol URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import path

from gol.endpoints import parse_rules, submit, step, user_create
import gol.views as views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', lambda request: redirect('/', permanent=False)),
    path('rules/parse', parse_rules),
    path('klikatko', views.simulation),
    path('task/<int:id>', views.task),
    path('task/<int:id>/submit', submit),
    path('task/<int:id>/step', step),
    path('help', views.help),
    path('usercreate', user_create),
    path('monitor', views.monitor),
]
