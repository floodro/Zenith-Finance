from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name='login'),
    path("signup/", views.signup, name='signup'),
    path("logout/", views.logout, name='logout'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("admin/upload-transactions/", views.upload_transactions, name='upload_transactions'),
    path("admin/transactions/", views.transaction_list, name='transaction_list'),
]

