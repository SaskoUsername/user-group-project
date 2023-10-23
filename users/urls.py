from django.urls import path

from . import views

urlpatterns = [
    path('', views.groups_list, name='list_of_groups'),
    path('sign_up/', views.sign_up_view, name='sign_up'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('group-<int:index>/users/', views.get_users_of_group, name='list_of_users'),
    path('delete_object-<int:object_id>/', views.delete_object_view, name='delete_object'),
    path('create_group/', views.create_group_view, name='create_group'),
    path('create_user-<group_id>/', views.create_user_view, name='create_user'),
    path('update_group-<group_id>/', views.update_group_view, name='update_group'),
    path('update_user-<user_id>/', views.update_user_view, name='update_user'),
]
