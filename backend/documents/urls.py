from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet, basename='document')
router.register(r'chunks', views.ContentChunkViewSet, basename='chunk')

urlpatterns = [
    path('', include(router.urls)),
]