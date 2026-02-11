from django.urls import path

from .views import ProductListView, ProductDetailView, comment_create

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('comment/<int:product_id>/', comment_create, name='comment_create'),
]