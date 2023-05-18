"""twitter_import URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from scraper import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index_page'),
    path('user_list/', views.UsersListView.as_view(), name='user_list'),
    path('twitter_seach/', views.TwitterSearchView.as_view(), name='twitter_search'),
    path('user/<int:user_id>/', views.UserTwittsView.as_view(), name='get_twit_for_user'),
    path('user_delete/<int:user_twitter_id>/', views.delete_user_twitter, name='delete_user_twitter'),
    path('user_update/<int:user_twitter_id>/', views.update_user_twitter, name='update_user_twitter')
]
