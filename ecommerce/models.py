from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from core.models import BaseModel
from accounts.models import User
from core.constants import FLAT, PERCENTAGE, COUPON_TYPES, ORDER_STATUS, PENDING, PAYMENT_PROVIDERS, RAZORPAY

# ----------------------
# ADDRESS MODEL
# ----------------------
class Address(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    
# ----------------------
# CATEGORY MODEL
# ----------------------
class Category(BaseModel):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

# ----------------------
# COUPON MODEL
# ----------------------
class Coupon(BaseModel):    
    name = models.CharField(max_length=255)
    coupon_code = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=COUPON_TYPES, default=FLAT)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_cart_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

# ----------------------
# PRODUCT MODEL
# ----------------------
class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    main_image_url = models.URLField()
    sub_images = models.JSONField(default=list, blank=True)
    
# ----------------------
# CART MODEL
# ----------------------
class CartItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

class Cart(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    items = models.ManyToManyField(CartItem, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

# ----------------------
# ORDER MODEL
# ----------------------
class Order(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_order_price = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    items = models.JSONField(default=list, blank=True) 
    
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)

    status = models.CharField(max_length=20, choices=ORDER_STATUS, default=PENDING)
    payment_provider = models.CharField(max_length=20, choices=PAYMENT_PROVIDERS, default=RAZORPAY)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    is_payment_done = models.BooleanField(default=False)

# ----------------------
# PROFILE MODEL
# ----------------------
class Profile(BaseModel):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=50, default="John")
    last_name = models.CharField(max_length=50, default="Doe")
    country_code = models.CharField(max_length=10, blank=True, default="")
    phone_number = models.CharField(max_length=20, blank=True, default="")
    