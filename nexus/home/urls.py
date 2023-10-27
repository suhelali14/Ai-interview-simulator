
from django.contrib import admin
from django.urls import path
from home import views
from . import views
urlpatterns = [
    path('', views.index,name='home'),
    path('newchat', views.newchat,name='newchat'),
    path('run_prompt', views.run_prompt,name='run_prompt'),
    path('signup', views.signup,name='signup'),
    path('login', views.login,name='login'),
    path('logout', views.logout,name='logout'),
]

