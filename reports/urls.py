from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list_view, name='reports'),
    path('new/', views.report_create_view, name='report_create'),
    path('<int:pk>/', views.report_detail_view, name='report_detail'),
]
