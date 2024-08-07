"""
URL configuration for ADashbord project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# import vews
from firstpage import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data/', views.data, name='data'),
    path('admin/', admin.site.urls),
    path('login/',views.loginuser, name='loginuser'),
    path('logout/',views.logout_user, name='logout'),
    path('reset/',views.password_reset, name='password_reset'),
    path('register/',views.register, name='register'),

]
