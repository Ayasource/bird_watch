from . import views
from django.urls import path

urlpatterns = [
    path('', views.home_page, name='home'),
    path('birds/', views.user_bird_list, name='bird_list'), 
    path('add-bird/', views.add_bird, name='add_bird'),
    path('profile/', views.user_profile, name='profile'),
    path('<slug:slug>/', views.bird_entry, name='bird_entry'),
    path('bird/<slug:slug>/edit/', views.bird_edit, name='bird_edit'),
    path('bird/<slug:slug>/delete/', views.bird_delete, name='bird_delete'),
]
