from django.contrib import admin
from django.urls import path, include
from . import views
from django.urls import path
from .views import current_user, UserList

urlpatterns = [
    path('heroes/', views.all_heroes),
    path('heroes/<int:hero_id>/', views.view_hero),
    path('heroes/<int:hero_id>/guides/', views.all_guides),
    path('heroes/<int:hero_id>/guides/<int:guide_id>/', views.view_guide),
    path('heroes/<int:hero_id>/guides/add/', views.add_guide),
    path('heroes/<int:hero_id>/guides/<int:guide_id>/edit/', views.edit_guide),
    path('heroes/<int:hero_id>/guides/<int:guide_id>/delete/', views.delete_guide),
    path('items/', views.all_items),
    path('items/<int:item_id>', views.view_item),
    path('roles/', views.all_roles),
    path('roles/<int:role_id>', views.view_role),
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
]