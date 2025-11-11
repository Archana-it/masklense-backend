from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    UserProfileView,
    FacialAnalysisCreateView,
    FacialAnalysisListView,
    FacialAnalysisDetailView,
    WeeklySummaryView,
    WeeklySummaryListView
)

urlpatterns = [
    # Authentication
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User Profile
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    
    # Facial Analysis
    path('analysis/', FacialAnalysisCreateView.as_view(), name='analysis_create'),
    path('analysis/list/', FacialAnalysisListView.as_view(), name='analysis_list'),
    path('analysis/<int:pk>/', FacialAnalysisDetailView.as_view(), name='analysis_detail'),
    
    # Weekly Summary
    path('summary/weekly/', WeeklySummaryView.as_view(), name='weekly_summary'),
    path('summary/history/', WeeklySummaryListView.as_view(), name='summary_history'),
]
