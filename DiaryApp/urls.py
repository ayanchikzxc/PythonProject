from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import DiaryEntryViewSet
from .views import mood_chart
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.index, name='index'),
    path('entry/<int:entry_id>/', views.entry_detail, name='entry_detail'),
    path('entry/create/', views.create_entry, name='create_entry'),
    path('entry/<int:entry_id>/edit/', views.edit_entry, name='edit_entry'),
    path('entry/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),
    path('login/', auth_views.LoginView.as_view(template_name='DiaryApp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('mood-chart/', views.mood_chart, name='mood_chart'),
    path('mood_chart/', mood_chart, name='mood_chart'),
]

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

router = DefaultRouter()
router.register(r'entries', DiaryEntryViewSet, basename='diaryentry')

from django.urls import include
urlpatterns += [
    path('api/', include(router.urls)),
]
