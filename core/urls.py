from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, dashboard_view, home_view, device_latest_json, device_history_json, CustomLoginView
from . import views

urlpatterns = [
    path('', home_view, name='base'),
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path("device/<str:device_id>/data/", views.device_data_page, name="device_data_page"),
    # path('device/<str:device_id>/data-json/', views.device_data_json, name="device_data_json"),
    path("api/push/", views.push_single, name="api-push-single"),
    path("api/push/batch/", views.push_batch, name="api-push-batch"),
    path('device/<str:device_id>/latest/', device_latest_json, name='device_latest_json'),
    path('device/<str:device_id>/history/', device_history_json, name='device_history_json'),

]
