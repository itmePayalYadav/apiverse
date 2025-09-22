from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from .models import (
    Profile, Product, 
    Category, Coupon, Cart,
    CartItem, Address
)
from .serializers import (
    ProfileSerializer, 
    CategorySerializer, 
    ProductSerializer, 
    CartSerializer,
    CouponSerializer,
    CartItemSerializer,
    AddressSerializer
)
from core.utils import api_response

# ----------------------
# Profile Views
# ----------------------
class ProfileRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile  

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return api_response(
            success=True,
            message="Profile retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_response(
            success=True,
            message="Profile updated successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Category Views
# ----------------------
class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(
            success=True,
            message="Categories retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


class CategoryDetailView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(
            success=True,
            message="Category retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return api_response(
            success=True,
            message="Category created successfully",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )


class CategoryUpdateView(generics.UpdateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_response(
            success=True,
            message="Category updated successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


class CategoryDeleteView(generics.DestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return api_response(
            success=True,
            message="Category deleted successfully",
            data=None,
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Product Views
# ----------------------
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(
            success=True,
            message="Products retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return api_response(
            success=True,
            message="Product retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


class CategoryProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return Product.objects.filter(category_id=category_id)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(
            success=True,
            message="Products retrieved successfully for this category",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)  
        return api_response(
            success=True,
            message="Product created successfully",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )


class ProductUpdateView(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return api_response(
            success=True,
            message="Product updated successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


class ProductDeleteView(generics.DestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return api_response(
            success=True,
            message="Product deleted successfully",
            data=None,
            status_code=status.HTTP_200_OK
        )
        
# ----------------------
# Cart VIEWS
# ----------------------
class UserCartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        cart, _ = Cart.objects.get_or_create(owner=self.request.user)
        return cart
    
    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        return api_response(
            success=True,
            message="Cart retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

class AddUpdateCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return api_response(
                success=False,
                message="Product ID is required.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return api_response(
                success=False,
                message="Product not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        cart, _ = Cart.objects.get_or_create(owner=request.user)
        cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartSerializer(cart, context={'request': request})
        return api_response(
            success=True,
            message="Cart updated successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
    
class RemoveCartItemView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        if not product_id:
            return api_response(
                success=False,
                message="Product ID is required.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        cart = Cart.objects.filter(owner=request.user).first()
        if not cart:
            return api_response(
                success=False,
                message="Cart not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        try:
            item = cart.items.get(product_id=product_id)
            item.delete()
        except CartItem.DoesNotExist:
            return api_response(
                success=False,
                message="Item not in cart.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        serializer = CartSerializer(cart)
        return api_response(
            success=True,
            message="Item removed from cart.",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


class ClearCartView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        cart = Cart.objects.filter(owner=request.user).first()
        if not cart:
            return api_response(
                success=False,
                message="Cart not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        cart.items.all().delete()
        return api_response(
            success=True,
            message="Cart cleared successfully.",
            data=None,
            status_code=status.HTTP_200_OK
        )

# ----------------------
# COUPON VIEWS
# ----------------------
class CouponListView(generics.ListAPIView):
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Coupon.objects.all()
    
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(
            success=True,
            message="Coupons retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
    
class CouponCreateView(generics.CreateAPIView):
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        
        return api_response(
            success=True,
            message="Coupon created successfully",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )

class AvailableCouponListView(generics.ListAPIView):
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        now = timezone.now()
        return Coupon.objects.filter(
            start_date__lte=now,
            expiry_date__gte=now
        )
        
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(
            success=True,
            message="Available coupons retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
        
class CouponDetailView(generics.RetrieveAPIView):
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Coupon.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        coupon = self.get_object()
        serializer = self.get_serializer(coupon)
        return api_response(
            success=True,
            message="Coupon retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
        
class CouponDeleteView(generics.DestroyAPIView):
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Coupon.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        coupon = self.get_object()
        coupon.delete()
        
        return api_response(
            success=True,
            message="Coupon deleted successfully",
            data=None,
            status_code=status.HTTP_200_OK
        )
        
class CouponUpdateView(generics.UpdateAPIView):
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Coupon.objects.all()
    
    def update(self, request, *args, **kwargs):
        coupon = self.get_object()
        serializer = self.get_serializer(coupon, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_response(
            success=True,
            message="Coupon updated successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

class ApplyCouponView(generics.GenericAPIView):
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        code = request.data.get("coupon_code")
        cart = Cart.objects.filter(owner=request.user).first()
        if not cart:
            return api_response(
                success=False,
                message="Cart not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        try:
            coupon = Coupon.objects.get(coupon_code=code)
        except Coupon.DoesNotExist:
            return api_response(
                success=False,
                message="Invalid coupon code.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        now = timezone.now()
        if coupon.start_date > now or (coupon.expiry_date and coupon.expiry_date < now):
            return api_response(
                success=False,
                message="Coupon is not active.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        cart.coupon = coupon
        cart.save()
        serializer = self.get_serializer(coupon)
        
        return api_response(
            success=True, 
            message="Coupon applied successfully.", 
            data=serializer.data
        )
        
    
class RemoveCouponView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        cart = Cart.objects.filter(owner=request.user).first()
        if not cart or not cart.coupon:
            return api_response(
                False,
                "No coupon applied to remove.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        cart.coupon = None
        cart.save()
        return api_response(True, "Coupon removed successfully.")
        
class CouponStatusUpdateView(generics.UpdateAPIView):
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Coupon.objects.all()
    
    def patch(self, request, *args, **kwargs):
        coupon = self.get_object()
        is_active = request.data.get("is_active", True)
        
        if is_active:
            coupon.expiry_date = coupon.expiry_date or None
        else:
            coupon.expiry_date = timezone.now()
        
        coupon.save()

        serializer = self.get_serializer(coupon, partial=True)
        return api_response(
            True, 
            "Coupon status updated successfully.", 
            data=serializer.data
        )
        
# ----------------------
# ADDRESS VIEWS
# ----------------------
class AddressListView(generics.ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(owner=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return api_response(
            success=True,
            message="Addresses retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

class AddressCreateView(generics.CreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return api_response(
            success=True,
            message="Address created successfully",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )
    
class AddressRetrieveView(generics.RetrieveAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(
            success=True,
            message="Address retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

class AddressUpdateView(generics.UpdateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_response(
            success=True,
            message="Address updated successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

class AddressDeleteView(generics.DestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return api_response(
            success=True,
            message="Address deleted successfully",
            data=None,
            status_code=status.HTTP_200_OK
        )