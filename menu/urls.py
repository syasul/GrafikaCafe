from django.urls import path

from . import views


urlpatterns = [
    path('', views.menu, name='menu'),
    path('tambah-menu/', views.tambahMenu, name='tambah-menu'),
    path('update-menu/', views.updateMenu, name='update-menu'),
    path('delete-menu', views.deleteMenu, name='delete-menu')
]
