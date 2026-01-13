from django.urls import path
from .views import home_page_view
from bird_watch import views as index_views

urlpatterns = [
    path("", home_page_view),
]
