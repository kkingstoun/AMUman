from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from manager.routing import manager_router

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Dokumentacja API
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Panel administracyjny
    path("admin/", admin.site.urls),

    # Endpointy API
    path('api/', include(manager_router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Widoki frontendu Django
    path('', include('manager.urls'), name='home'),
    # path('tasks/', TaskListView.as_view(), name='task-list'),
    # path('nodes/', NodeListView.as_view(), name='node-list'),
    # path('gpus/', GpuListView.as_view(), name='gpu-list'),
    # path('manager-settings/', ManagerSettingsView.as_view(), name='manager-settings'),

    # Inne aplikacje i ich URLconf
    # path('some-app/', include('some_app.urls')),
]
