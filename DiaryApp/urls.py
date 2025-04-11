from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('entry/<int:entry_id>/', views.entry_detail, name='entry_detail'),
    path('entry/create/', views.create_entry, name='create_entry'),
    path('entry/<int:entry_id>/edit/', views.edit_entry, name='edit_entry'),
    path('entry/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),
]
