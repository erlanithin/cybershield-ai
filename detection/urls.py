from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('detect/', views.detection_view, name='detection'),
    path('batch-detect/', views.batch_detection_view, name='batch_detection'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('my-history/', views.user_dashboard_view, name='user_dashboard'),
    path('model-analytics/', views.model_analytics_view, name='model_analytics'),
    path('export/csv/', views.export_csv_view, name='export_csv'),
    path('analysis/<int:pk>/status/', views.update_review_status, name='update_review_status'),
    path('feedback/submit/', views.submit_feedback, name='submit_feedback'),
    # REST API
    path('api/analyze/', views.api_analyze, name='api_analyze'),
]
