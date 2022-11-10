"""order_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from web.views import account
from web.views import level

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', account.login, name='login'),
    path('login/message/', account.login_message, name='login_message'),

    path('level/list/', level.level_list, name='level_list'),
    path('level/add/', level.level_add, name='level_add'),
    path('level/edit/<int:pk>/', level.level_edit, name='level_edit'),
    path('level/delete/<int:pk>/', level.level_delete, name='level_delete'),

]
