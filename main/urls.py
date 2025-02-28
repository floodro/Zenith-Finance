from django.urls import path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="QA TestLab API",
        default_version='v1',
        description="API documentation for QA TestLab",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", views.index, name='main'),
    path("login/", views.login, name='login'),
    path("signup/", views.signup, name='signup'),
    path("logout/", views.logout, name='logout'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("users/", views.get_users, name="get_users"),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('api/users/', views.get_users, name='api_get_users'),
    path('api/delete_user/<int:user_id>/', views.delete_user, name='api_delete_user'),
    path('api/update_user/<int:user_id>/', views.update_user, name='api_update_user'),
    path('api/create_admin/', views.create_admin, name='api_create_admin'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
