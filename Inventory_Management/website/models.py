from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Customer(models.Model):
    # ============ EXISTING FIELDS - KEEP EXACTLY AS IS ============
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    # ============ NEW FIELDS - ADDING ENHANCED CRM FEATURES ============
    customer_type = models.CharField(max_length=20, choices=[
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('wholesale', 'Wholesale')
    ], default='individual')
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        ordering = ['-created_at']

class Category(models.Model):
    """Product categories for organization"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']


class Supplier(models.Model):
    """Supplier/Vendor management"""
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    """Complete product management system"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')

    # Pricing information
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    # Inventory tracking
    quantity_in_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    minimum_stock_level = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    maximum_stock_level = models.IntegerField(default=1000, validators=[MinValueValidator(0)])

    # Status and timestamps
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def is_low_stock(self):
        """Check if product is below minimum stock level"""
        return self.quantity_in_stock <= self.minimum_stock_level

    @property
    def profit_margin(self):
        """Calculate profit margin percentage"""
        if self.cost_price and self.selling_price:
            return ((self.selling_price - self.cost_price) / self.selling_price) * 100
        return 0

    class Meta:
        ordering = ['name']


class StockMovement(models.Model):
    """Track all inventory movements"""
    MOVEMENT_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
        ('transfer', 'Transfer'),
        ('damaged', 'Damaged'),
        ('expired', 'Expired')
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    reference = models.CharField(max_length=100, blank=True, help_text="Reference number (PO, SO, etc.)")
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.movement_type} - {self.quantity}"

    def save(self, *args, **kwargs):
        """Automatically update product stock when saving movement"""
        super().save(*args, **kwargs)
        product = self.product

        if self.movement_type == 'in':
            product.quantity_in_stock += self.quantity
        elif self.movement_type in ['out', 'damaged', 'expired']:
            product.quantity_in_stock -= self.quantity

        product.save()

    class Meta:
        ordering = ['-created_at']


class Order(models.Model):
    """Order management for both sales and purchases"""
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned')
    ]

    ORDER_TYPES = [
        ('sale', 'Sales Order'),
        ('purchase', 'Purchase Order')
    ]

    order_number = models.CharField(max_length=50, unique=True)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_number} - {self.order_type} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Auto-generate order number
            prefix = 'SO' if self.order_type == 'sale' else 'PO'
            last_order = Order.objects.filter(order_type=self.order_type).order_by('-id').first()
            if last_order:
                last_num = int(last_order.order_number.split('-')[1])
                self.order_number = f"{prefix}-{last_num + 1:06d}"
            else:
                self.order_number = f"{prefix}-000001"
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    """Individual items within an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.order.order_number} - {self.product.name}"

    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

        # Update order total
        order_total = sum(item.total_price for item in self.order.items.all())
        self.order.total_amount = order_total
        self.order.save()

        # Create stock movement for sales orders
        if self.order.order_type == 'sale' and self.order.status in ['confirmed', 'processing', 'shipped']:
            StockMovement.objects.create(
                product=self.product,
                movement_type='out',
                quantity=self.quantity,
                reference=self.order.order_number,
                notes=f"Sales order {self.order.order_number}",
                created_by=self.order.created_by
            )

    class Meta:
        unique_together = ['order', 'product']


class Warehouse(models.Model):
    """Multi-warehouse support"""
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_warehouses')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ProductLocation(models.Model):
    """Track products in specific warehouse locations"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='locations')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='product_locations')
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    section = models.CharField(max_length=50, blank=True, help_text="Aisle, shelf, bin location")

    def __str__(self):
        return f"{self.product.name} at {self.warehouse.name}"

    class Meta:
        unique_together = ['product', 'warehouse']
