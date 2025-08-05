from django.urls import path
from . import views

urlpatterns = [
    # Core auth URLs
    path("", views.login, name='login'),
    path("signup/", views.signup, name='signup'),
    path("logout/", views.logout, name='logout'),
    path("dashboard/", views.dashboard, name='dashboard'),

    # Sidebar Page URLs
    path("profile/", views.profile, name='profile'),
    path("reports/", views.reports, name='reports'),
    path("settings/", views.settings, name='settings'), 

    # Transaction URLs
    path("transactions/", views.transactions, name='transactions'), 
    path("transactions/add/", views.add_transaction, name='add_transaction'),
    
    # Admin URLs
    path("admin/upload-transactions/", views.admin_upload_transactions, name='upload_transactions'),
]