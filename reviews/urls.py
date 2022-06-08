from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('reviews/create/', views.ProductCreateView.as_view(), name='create'),
  
]
