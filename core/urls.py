from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Import Views
from users.views import UserViewSet
from inventory.views import AssetViewSet, CategoryViewSet
from audit.views import AuditLogViewSet


# Create Router
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'audit', AuditLogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # JWT Authentication Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include('web_interface.urls')),

    # Add this for Password Reset:
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)