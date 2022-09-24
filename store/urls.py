from . import views
from django.urls import path

app_name = "store"

urlpatterns = [
    path('', views.home, name='home'),
    path('product-detail/<int:pk>/', views.product_detail, name='product-detail'),
    path('category/<slug:category_slug>/', views.product_category, name='category-list'),
]