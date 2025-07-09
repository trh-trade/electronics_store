from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='index'),
    path('about/', views.about, name='about'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
