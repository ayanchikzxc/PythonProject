from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api_views import DiaryEntryViewSet

router = DefaultRouter()
router.register(r'api/entries', DiaryEntryViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('entry/create/', views.create_entry, name='create_entry'),
    path('entry/<int:entry_id>/', views.entry_detail, name='entry_detail'),
    path('entry/<int:entry_id>/edit/', views.edit_entry, name='edit_entry'),
    path('entry/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),
    path('', include(router.urls)),
]
