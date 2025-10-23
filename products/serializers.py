from rest_framework import serializers
from .models import Category, SubCategory, Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    subcategory = serializers.CharField(source='subcategory.name', read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'subcategory', 'price', 'images']

    def get_images(self, obj):
        request = self.context.get('request')
        images = []
        for size in ['small', 'medium', 'large']:
            img_field = getattr(obj, f'image_{size}', None)
            if img_field:
                url = request.build_absolute_uri(img_field.url) if request else img_field.url
                images.append({'size': size, 'url': url})
        return images


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'image_small', 'image_medium', 'image_large']