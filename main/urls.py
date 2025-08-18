from django.urls import path
from . import views

urlpatterns = [
    # --- AUTHENTICATION ---
    path("", views.login_view, name='login'),
    path("signup/", views.signup_view, name='signup'),
    path("logout/", views.logout_view, name='logout'),
    
    # --- CORE APP ---
    path("dashboard/", views.dashboard_view, name='dashboard'),
    path("profile/", views.profile_view, name='profile'),
    path("transactions/", views.transactions_list_view, name='transactions'),
    path("transactions/add/", views.add_transaction_view, name='add_transaction'),
    path("transactions/upload/", views.upload_transactions_view, name="transaction_upload"),
    path("reports/", views.reports_view, name='reports'),
    path("settings/", views.settings_view, name='settings'),
]
