from django.urls import path

from . import views

urlpatterns = [
    path('', views.getInfo),
    path('updateInfo/', views.updateInfo),
    path('changePassword/', views.changePassword),
]