from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('get_books/', views.get_books, name='get_books'),
    path('get_book/<str:pk>/', views.get_book, name='get_book'),
    path('search_books/', views.search_books, name='search_books'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)