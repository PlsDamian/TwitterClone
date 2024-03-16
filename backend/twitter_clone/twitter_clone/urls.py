from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tweets.urls')),  # Include app-specific URLs
    path('api-auth/', include('rest_framework.urls')),
    path('', include('tweets.urls',)),
    path('login/', LoginView.as_view(), name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
