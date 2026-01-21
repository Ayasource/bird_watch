from . import views
from django.urls import path

urlpatterns = [
    path('', views.home_page, name='home'),
    path('birds/', views.user_bird_list, name='bird_list'), 
    path('add-bird/', views.add_bird, name='add_bird'),
    path('profile/', views.user_profile, name='profile'),
    path('<int:pk>/', views.bird_entry, name='bird_entry'),
    path('bird/<int:pk>/edit/', views.bird_edit, name='bird_edit'),
    path('bird/<int:pk>/delete/', views.bird_delete, name='bird_delete'),
]
