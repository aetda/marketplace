from django.urls import path
from .views import CategoryListView, ProductListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('list/', ProductListView.as_view(), name='product-list'),
]
