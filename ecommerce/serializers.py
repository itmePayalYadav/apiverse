from rest_framework import serializers
from .models import Product, Category, Coupon, Cart, CartItem, Order, Address, Profile

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
