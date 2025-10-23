from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)
    product_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_detail', 'quantity']

    def get_product_detail(self, obj):
        request = self.context.get('request')
        images = []
        for size in ['small', 'medium', 'large']:
            img_field = getattr(obj.product, f'image_{size}', None)
            if img_field:
                url = request.build_absolute_uri(img_field.url) if request else img_field.url
                images.append({'size': size, 'url': url})
        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'slug': obj.product.slug,
            'price': obj.product.price,
            'images': images
        }


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_quantity', 'total_price']
        read_only_fields = ['user', 'total_quantity', 'total_price']

    def get_total_quantity(self, obj):
        return obj.total_quantity()

    def get_total_price(self, obj):
        return obj.total_price()

    def create(self, validated_data):
        user = self.context['request'].user
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart


class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)
