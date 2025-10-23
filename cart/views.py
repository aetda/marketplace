from rest_framework import status, generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, CartAddSerializer
from django.shortcuts import get_object_or_404


class CartDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartAddSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(pk=serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']

        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()

        return Response({'status': 'added', 'item_id': item.id}, status=status.HTTP_201_CREATED)


class UpdateCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item = get_object_or_404(CartItem, pk=pk, cart=cart)
        serializer = CartItemSerializer(item, data=request.data, partial=True, context={'request': request})
        self.valid = serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'updated'})

    def delete(self, request, pk):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item = get_object_or_404(CartItem, pk=pk, cart=cart)
        item.delete()
        return Response({'status': 'deleted'}, status=status.HTTP_204_NO_CONTENT)


class ClearCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response({'status': 'cleared'})
