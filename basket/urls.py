from . import views
from django.urls import path

app_name = "basket"

urlpatterns = [
    path('', views.basket_summary, name='basket-summary'),
    path('basket_add/', views.basket_add, name='basket_add'),
    path('basket_delete/', views.basket_delete, name='basket_delete'),
    path('basket_update/', views.basket_update, name='basket_update'),
]