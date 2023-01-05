from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'user_profile', views.UserProfileViewSet, basename="user_profile")
