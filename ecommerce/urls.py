from django.urls import path
from .views import (
    # Profile
    ProfileRetrieveView,
    ProfileUpdateView,

    # Category
    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    CategoryProductsView,

    # Product
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,

    # Cart
    UserCartView,
    AddUpdateCartItemView,
    RemoveCartItemView,
    ClearCartView,

    # Coupon
    CouponListView,
    CouponCreateView,
    AvailableCouponListView,
    CouponDetailView,
    CouponDeleteView,
    CouponUpdateView,
    ApplyCouponView,
    RemoveCouponView,
    CouponStatusUpdateView,

    # Address
    AddressListView,
    AddressCreateView,
    AddressRetrieveView,
    AddressUpdateView,
    AddressDeleteView,
)

app_name = "ecommerce"

urlpatterns = [
    # ----------------------
    # Profile
    # ----------------------
    path("profile/", ProfileRetrieveView.as_view(), name="profile-retrieve"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile-update"),

    # ----------------------
    # Category
    # ----------------------
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
    path("categories/<uuid:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("categories/<uuid:pk>/update/", CategoryUpdateView.as_view(), name="category-update"),
    path("categories/<uuid:pk>/delete/", CategoryDeleteView.as_view(), name="category-delete"),
    path("categories/<uuid:category_id>/products/", CategoryProductsView.as_view(), name="category-products"),

    # ----------------------
    # Product
    # ----------------------
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/create/", ProductCreateView.as_view(), name="product-create"),
    path("products/<uuid:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/<uuid:pk>/update/", ProductUpdateView.as_view(), name="product-update"),
    path("products/<uuid:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"),

    # ----------------------
    # Cart
    # ----------------------
    path("cart/", UserCartView.as_view(), name="user-cart"),
    path("cart/add/", AddUpdateCartItemView.as_view(), name="add-update-cart"),
    path("cart/remove/", RemoveCartItemView.as_view(), name="remove-cart-item"),
    path("cart/clear/", ClearCartView.as_view(), name="clear-cart"),

    # ----------------------
    # Coupon
    # ----------------------
    path("coupons/", CouponListView.as_view(), name="coupon-list"),
    path("coupons/create/", CouponCreateView.as_view(), name="coupon-create"),
    path("coupons/available/", AvailableCouponListView.as_view(), name="coupon-available"),
    path("coupons/<uuid:pk>/", CouponDetailView.as_view(), name="coupon-detail"),
    path("coupons/<uuid:pk>/update/", CouponUpdateView.as_view(), name="coupon-update"),
    path("coupons/<uuid:pk>/delete/", CouponDeleteView.as_view(), name="coupon-delete"),
    path("coupons/<uuid:pk>/status/", CouponStatusUpdateView.as_view(), name="coupon-status-update"),
    path("coupons/apply/", ApplyCouponView.as_view(), name="coupon-apply"),
    path("coupons/remove/", RemoveCouponView.as_view(), name="coupon-remove"),

    # ----------------------
    # Address
    # ----------------------
    path("addresses/", AddressListView.as_view(), name="address-list"),
    path("addresses/create/", AddressCreateView.as_view(), name="address-create"),
    path("addresses/<uuid:pk>/", AddressRetrieveView.as_view(), name="address-detail"),
    path("addresses/<uuid:pk>/update/", AddressUpdateView.as_view(), name="address-update"),
    path("addresses/<uuid:pk>/delete/", AddressDeleteView.as_view(), name="address-delete"),
]
