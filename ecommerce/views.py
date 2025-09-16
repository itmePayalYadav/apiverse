from rest_framework import generics, status, permissions
from .models import Profile
from .serializers import ProfileSerializer
from core.utils import api_response

# ----------------------
# Profile Retrieve
# ----------------------
class ProfileRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_class = [permissions.IsAuthenticated]
    
    def get_queryset(self):
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

# ----------------------
# Profile Update
# ----------------------
class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.profile
    
    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_response(
            success=True,
            message="Profile updated successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
        
# ----------------------
# List Products
# ----------------------
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Product.objects.all()
    
    def list(self, request, *args, **kwargs):
        products = self.get_queryset()
        serializer = self.get_serializer(products, many=True)
        return api_response(
            success=True,
            message="Products retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Create Product
# ----------------------
class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_response(
            success=True,
            message="Product created successfully",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )

# ----------------------
# Retrieve Product
# ----------------------
class ProductRetriveView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        reutrn Product.objects.all()
    
    def retrieve(self, request, *args, **kwarg)
        product = get_objects_or_404(self.get_queryset(), pk=kwargs["id"])
        return api_response(
                success=True,
                message="Product retrieved successfully",
                data=self.get_serializer(product).data,
                status_code=status.HTTP_200_OK
            )

# ----------------------
# Update Product
# ----------------------
class ProductUpdateView(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Product.objects.all()
    
    def update(self, request, *args, **kwargs):
        product = get_object_or_404(self.get_queryset(), pk=kwargs["id"])
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_response(
            success=True,
            message="Product updated successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
    
# ----------------------
# Delete Product
# ----------------------
class ProductDeleteView(generics.DestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Product.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        product = get_object_or_404(self.get_queryset(), pk=kwargs["id"])
        product.delete()
        return api_response(
            success=True,
            message="Product deleted successfully",
            status_code=status.HTTP_200_OK
        )

# ----------------------
# List Orders (User-specific)
# ----------------------
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)
    
    def list(self, request, *args, **kwargs):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return api_response(
            success=True,
            message="Orders retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

