from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('product/create/', views.ProductCreateView.as_view(), name='create'),
    path('product/list/', views.ProductListView.as_view(), name='list'),
    path('product/update/<slug:slug>', views.ProductUpdateView.as_view(), name='update'),
    path('product/delete/<slug:slug>', views.ProductDeleteView.as_view(), name='delete'),
    path('product/detail/<slug:slug>', views.ProductDetailView.as_view(), name='detail'),
    path('product/review/<slug:slug>', views.ProductReview.as_view(), name='review'),

    path('add-to-cart/<slug:slug>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug:slug>', views.remove_from_cart, name='remove-from-cart'),
    path('cart/', views.OrderSummaryView.as_view(), name='cart'),
    path('checkout', views.CheckOut.as_view(), name='checkout'),
  
    
]
