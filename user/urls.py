"""core URL Configuration

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

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from user import views


app_name = 'user'
urlpatterns = [
    path('', views.UserLoginView.as_view(), name="login"),
    path("register/", views.UserProfileCreateView.as_view(), name="register"),
    path('logout/', views.LogoutTemplateView.as_view(), name='user_logout'),
    path("profile/", views.my_profile, name="profile"),
    path('update_profile/', views.UserProfileUpdateView.as_view(), name='update_profile'),
    #path("favorite/", views.favorite, name="favorite"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)