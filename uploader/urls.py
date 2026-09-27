from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('api/upload/', views.upload_image, name='upload_image'),
    path('api/delete/<str:short_id>/', views.delete_image, name='delete_image'),
    path('img/<str:short_id>', views.serve_image, name='serve_image'),
]

