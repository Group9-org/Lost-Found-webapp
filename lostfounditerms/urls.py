
from django.urls import path
from . import views

urlpatterns = [
    path('lost/', views.get_all_items),
    path('lost/add/', views.add_item),

   # path('found/', views.get_found_items),

    path('register/', views.register_user),
    path('login/', views.login_user),
    path('lost/update/<int:item_id>/', views.update_item),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('simple-reset/', views.simple_password_reset, name='simple_password_reset'),
    path('all-items/', views.get_all_items, name='get_all_items'),
    path('delete-item/<int:item_id>/', views.delete_lost_item, name='delete_item'),
    path('all-users/', views.get_all_users, name='get_all_users'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('update-status/<int:item_id>/', views.update_item_status, name='update_status'),
    path('update-user-role/<int:user_id>/', views.update_user_role, name='update_user_role'),
]

