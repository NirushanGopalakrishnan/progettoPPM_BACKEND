# store/serializers.py

from rest_framework import serializers
from .models import Product, CartItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate(self, data):
        try:
            product = Product.objects.get(pk=data['product_id'])
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")
        if data['quantity'] < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        if not product.active:
            raise serializers.ValidationError("Product is not active.")
        if product.stock < data['quantity']:
            raise serializers.ValidationError("Not enough stock.")
        return data
