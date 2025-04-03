from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('entry/create/', views.create_entry, name='create_entry'),
    path('entry/<int:entry_id>/', views.view_entry, name='view_entry'),
    path('entry/<int:entry_id>/edit/', views.edit_entry, name='edit_entry'),
    path('entry/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),
]
