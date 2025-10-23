from rest_framework import generics, pagination, filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class SmallPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.prefetch_related('subcategories').all().order_by('name')
    serializer_class = CategorySerializer
    pagination_class = SmallPageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = SmallPageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category__name', 'subcategory__name']
    ordering_fields = ['price', 'name', 'created_at']

    def get_queryset(self):
        qs = Product.objects.select_related('category', 'subcategory').all()
        category = self.request.query_params.get('category')
        subcategory = self.request.query_params.get('subcategory')
        if category:
            qs = qs.filter(category__slug=category)
        if subcategory:
            qs = qs.filter(subcategory__slug=subcategory)
        return qs
