"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
# from django.contrib.auth import views

from events.views.home import frontpage, dashboard, list_active_events, list_expire_events
# from accounts.views import signup, register_page, login_page

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # for home.py
    path('', frontpage, name='frontpage'),
    path('dashboard/', dashboard, name='dashboard'),
    path('list/all/active/events/', list_active_events, name='list_active_events'),
    path('list/all/expire/events/', list_expire_events, name='list_expire_events'),
    
    # events App.
    path('events/', include('events.urls', namespace='events')),
    
    # authentication App.
    path('accounts/', include('allauth.urls')),
    # path('signup/', register_page, name='signup'),
    # path('login/', login_page, name='login'),
    
    # path('login/', views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # path('logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
]
