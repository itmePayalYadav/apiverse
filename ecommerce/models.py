from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from core.models import BaseModel
from accounts.models import User
from core.constants import FLAT, COUPON_TYPES, ORDER_STATUS, PENDING, PAYMENT_PROVIDERS, RAZORPAY

# ----------------------
# ADDRESS MODEL
# ----------------------
class Address(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.address_line1}, {self.city}"

# ----------------------
# CATEGORY MODEL
# ----------------------
class Category(BaseModel):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

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
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.coupon_code})"

# ----------------------
# PRODUCT MODEL
# ----------------------
class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    main_image_url = models.URLField()
    sub_images = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name
    
# ----------------------
# CART MODEL
# ----------------------

class Cart(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Cart {self.id} - {self.owner}"

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

# ----------------------
# ORDER MODEL
# ----------------------
class Order(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_order_price = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

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

    def __str__(self):
        return f"Order {self.id} - {self.customer}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name if self.product else 'Deleted Product'} (x{self.quantity})"

# ----------------------
# PROFILE MODEL
# ----------------------
class Profile(BaseModel):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    country_code = models.CharField(max_length=10, blank=True, default="")
    phone_number = models.CharField(max_length=20, blank=True, default="")

    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip()