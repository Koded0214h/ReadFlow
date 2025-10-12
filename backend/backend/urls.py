"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView
from documents import views as document_views
from django.contrib.auth import views as auth_views

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# Test views for API testing
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/auth/', include('users.urls')),
    path('api/', include('documents.urls')),
    
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/cleredoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    
    path('', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('register/', TemplateView.as_view(template_name='registration/register.html'), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('library/', document_views.library_view, name='library'),
    path('upload/', document_views.upload_view, name='upload_document'),
    path('read/<int:document_id>/', document_views.read_view, name='read_document'),

    # API Test URLs
    path('test/', document_views.test_dashboard, name='test_dashboard'),
    path('test/register/', document_views.test_register, name='test_register'),
    path('test/login/', document_views.test_login, name='test_login'),
    path('test/profile/', document_views.test_profile, name='test_profile'),
    path('test/documents/', document_views.test_documents, name='test_documents'),
    path('test/chunks/', document_views.test_chunks, name='test_chunks'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
