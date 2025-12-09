from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, dashboard_view, home_view, device_data_json
from . import views

urlpatterns = [
    path('', home_view, name='base'),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path("device/<str:device_id>/data/", views.device_data_page, name="device_data_page"),
    path('device/<str:device_id>/data-json/', views.device_data_json, name="device_data_json"),
    path("api/push/", views.push_single, name="api-push-single"),
    path("api/push/batch/", views.push_batch, name="api-push-batch"),
]
