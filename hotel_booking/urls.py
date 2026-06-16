from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from hotels import views

# Swagger импорты
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Hotel Booking API",
        default_version='v1',
        description="API для сервиса бронирования отелей",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@hotelbooking.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # API
    path('api/hotels/', include('hotels.urls')),
    path('api/bookings/', include('bookings.urls')),
    
    # Accounts
    path('accounts/', include('accounts.urls')),
    path('reviews/', include('reviews.urls')),
    
    # Frontend
    path('', views.home, name='home'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)