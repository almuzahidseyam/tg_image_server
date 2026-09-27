from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/upload/', views.upload_image, name='upload_image'),
    path('img/<str:short_id>', views.serve_image, name='serve_image'),
]
