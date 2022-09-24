from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm

app_name = "accounts"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', form_class=UserLoginForm), name='accounts-login'),
    path('register/', views.account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
    #user dashboard
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('profile/edit-details/', views.edit_details, name='edit-details'),
    path('profile/delete/', views.delete_user, name='delete-account'),
    path('profile/confirm-delete/', views.confirm_account_delete, name='delete_confirmation'),
    path('dashboard/settings/', views.settings, name='settings'),
    path('dashboard/orders/', views.orders, name='orders'),
    path('dashboard/download/', views.user_downloads, name='download'),
    #addresses
    path("addresses/", views.view_address, name="addresses"),
    path("add_address/", views.add_address, name="add_address"),
    path("addresses/edit/<slug:id>/", views.edit_address, name="edit_address"),
    path("addresses/delete/<slug:id>/", views.delete_address, name="delete_address"),
    path("addresses/set_default/<slug:id>/", views.set_default, name="set_default"),
    #wishlist
    path('wishlist/add_to_wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.users_wishlist, name='wishlist'),

]   