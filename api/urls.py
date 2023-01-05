from django.urls import path, include, re_path

from .routers import router

urlpatterns = [
    path('', include(router.urls)),
]
