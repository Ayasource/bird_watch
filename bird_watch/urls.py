from . import views
from django.urls import path

urlpatterns = [
    path("", views.BirdEntry.as_view(), name='home'),
    path('<slug:slug>/', views.bird_entry, name='bird_entry'),
]
