from django.contrib import admin
from .models import Customer, Product, Category, Supplier, StockMovement, Order, OrderItem, Warehouse, ProductLocation

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # ============ DISPLAY CONFIGURATION ============
    list_display = (
        'first_name', 'last_name', 'email', 'phone', 
        'customer_type', 'credit_limit', 'city', 'state', 
        'created_at'
    )

    # ============ FILTERING AND SEARCH ============
    list_filter = ('customer_type', 'state', 'created_at', 'city')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'address')

    # ============ ORDERING AND PAGINATION ============
    ordering = ['-created_at']
    list_per_page = 25

    # ============ FORM ORGANIZATION ============
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone'),
            'description': 'Basic customer contact information'
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'zipcode'),
            'description': 'Customer address details'
        }),
        ('Business Information', {
            'fields': ('customer_type', 'credit_limit', 'notes'),
            'description': 'Business relationship and credit information'
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',),
            'description': 'System-generated information'
        }),
    )

    # ============ READ-ONLY FIELDS ============
    readonly_fields = ('created_at',)

    # ============ ADMIN ACTIONS ============
    actions = ['make_business_customer', 'make_wholesale_customer', 'reset_credit_limit']

    def make_business_customer(self, request, queryset):
        """Convert selected customers to business type"""
        updated = queryset.update(customer_type='business')
        self.message_user(request, f'{updated} customers updated to business type.')
    make_business_customer.short_description = "Convert to business customers"

    def make_wholesale_customer(self, request, queryset):
        """Convert selected customers to wholesale type"""  
        updated = queryset.update(customer_type='wholesale')
        self.message_user(request, f'{updated} customers updated to wholesale type.')
    make_wholesale_customer.short_description = "Convert to wholesale customers"

    def reset_credit_limit(self, request, queryset):
        """Reset credit limit to zero"""
        updated = queryset.update(credit_limit=0)
        self.message_user(request, f'Credit limit reset for {updated} customers.')
    reset_credit_limit.short_description = "Reset credit limit to $0"


# ========================================================================
# CATEGORY ADMIN - ADD THIS NEW ADMIN
# ========================================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_product_count', 'created_at')
    search_fields = ('name', 'description')
    ordering = ['name']
    readonly_fields = ('created_at',)

    def get_product_count(self, obj):
        """Display number of products in category"""
        return obj.products.filter(is_active=True).count()
    get_product_count.short_description = 'Active Products'
    get_product_count.admin_order_field = 'products__count'


# ========================================================================
# SUPPLIER ADMIN - ADD THIS NEW ADMIN
# ========================================================================

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'contact_person', 'email', 'phone', 
        'city', 'state', 'get_product_count', 'is_active', 'created_at'
    )
    list_filter = ('is_active', 'state', 'city', 'created_at')
    search_fields = ('name', 'contact_person', 'email', 'phone', 'address')
    ordering = ['name']
    list_per_page = 25

    fieldsets = (
        ('Company Information', {
            'fields': ('name', 'contact_person', 'email', 'phone'),
            'description': 'Basic supplier company information'
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'zipcode'),
            'description': 'Supplier address details'
        }),
        ('Status', {
            'fields': ('is_active',),
            'description': 'Supplier status and availability'
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',),
            'description': 'System-generated information'
        }),
    )

    readonly_fields = ('created_at',)
    actions = ['activate_suppliers', 'deactivate_suppliers']

    def get_product_count(self, obj):
        """Display number of active products from supplier"""
        return obj.products.filter(is_active=True).count()
    get_product_count.short_description = 'Active Products'

    def activate_suppliers(self, request, queryset):
        """Activate selected suppliers"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} suppliers activated.')
    activate_suppliers.short_description = "Activate selected suppliers"

    def deactivate_suppliers(self, request, queryset):
        """Deactivate selected suppliers"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} suppliers deactivated.')
    deactivate_suppliers.short_description = "Deactivate selected suppliers"


# ========================================================================
# PRODUCT ADMIN - ADD THIS NEW ADMIN  
# ========================================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'sku', 'category', 'supplier', 
        'get_stock_status', 'quantity_in_stock', 'minimum_stock_level',
        'selling_price', 'get_profit_margin', 'is_active', 'created_at'
    )
    list_filter = ('category', 'supplier', 'is_active', 'created_at')
    search_fields = ('name', 'sku', 'description')
    ordering = ['name']
    list_per_page = 25
    readonly_fields = ('created_at', 'updated_at', 'get_profit_margin')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'sku', 'category', 'supplier'),
            'description': 'Basic product information and classification'
        }),
        ('Pricing Information', {
            'fields': ('cost_price', 'selling_price', 'get_profit_margin'),
            'description': 'Product pricing and profitability'
        }),
        ('Inventory Information', {
            'fields': ('quantity_in_stock', 'minimum_stock_level', 'maximum_stock_level'),
            'description': 'Stock levels and inventory management'
        }),
        ('Status & Timestamps', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Product status and system timestamps'
        }),
    )

    actions = ['mark_as_low_stock', 'activate_products', 'deactivate_products']

    def get_stock_status(self, obj):
        """Display stock status with color coding"""
        if obj.quantity_in_stock == 0:
            return "Out of Stock"
        elif obj.is_low_stock:
            return "Low Stock"
        else:
            return "In Stock"
    get_stock_status.short_description = 'Stock Status'

    def get_profit_margin(self, obj):
        """Display profit margin percentage"""
        margin = obj.profit_margin
        return f"{margin:.1f}%" if margin else "N/A"
    get_profit_margin.short_description = 'Profit Margin'

    def mark_as_low_stock(self, request, queryset):
        """Set minimum stock level to current stock + 5"""
        for product in queryset:
            product.minimum_stock_level = product.quantity_in_stock + 5
            product.save()
        self.message_user(request, f'Updated minimum stock levels for {queryset.count()} products.')
    mark_as_low_stock.short_description = "Mark as low stock (set min level)"

    def activate_products(self, request, queryset):
        """Activate selected products"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} products activated.')
    activate_products.short_description = "Activate selected products"

    def deactivate_products(self, request, queryset):
        """Deactivate selected products"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} products deactivated.')
    deactivate_products.short_description = "Deactivate selected products"


# ========================================================================
# STOCK MOVEMENT ADMIN - ADD THIS NEW ADMIN
# ========================================================================

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'movement_type', 'quantity', 'reference',
        'created_by', 'created_at'
    )
    list_filter = ('movement_type', 'created_at', 'created_by')
    search_fields = ('product__name', 'product__sku', 'reference', 'notes')
    ordering = ['-created_at']
    list_per_page = 30
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Movement Details', {
            'fields': ('product', 'movement_type', 'quantity', 'reference'),
            'description': 'Stock movement transaction details'
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_by', 'created_at'),
            'description': 'Additional notes and tracking information'
        }),
    )

    def get_queryset(self, request):
        """Optimize database queries"""
        return super().get_queryset(request).select_related('product', 'created_by')


# ========================================================================
# ORDER ITEM INLINE - ADD THIS FOR ORDER ADMIN
# ========================================================================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('total_price',)
    fields = ('product', 'quantity', 'unit_price', 'total_price')

    def get_queryset(self, request):
        """Optimize database queries"""
        return super().get_queryset(request).select_related('product')


# ========================================================================
# ORDER ADMIN - ADD THIS NEW ADMIN
# ========================================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'order_type', 'get_customer_or_supplier', 
        'status', 'total_amount', 'order_date', 'created_by'
    )
    list_filter = ('order_type', 'status', 'order_date', 'created_by')
    search_fields = (
        'order_number', 'customer__first_name', 'customer__last_name', 
        'supplier__name', 'notes'
    )
    ordering = ['-order_date']
    list_per_page = 25
    readonly_fields = ('order_number', 'total_amount', 'created_at', 'updated_at')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'order_type', 'customer', 'supplier'),
            'description': 'Basic order identification and parties involved'
        }),
        ('Order Details', {
            'fields': ('status', 'expected_delivery_date', 'total_amount'),
            'description': 'Order status and delivery information'
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_by'),
            'description': 'Additional notes and tracking'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'System timestamps'
        }),
    )

    actions = ['mark_as_confirmed', 'mark_as_processing', 'mark_as_shipped']

    def get_customer_or_supplier(self, obj):
        """Display customer for sales orders, supplier for purchase orders"""
        if obj.customer:
            return f"{obj.customer.first_name} {obj.customer.last_name}"
        elif obj.supplier:
            return obj.supplier.name
        return "N/A"
    get_customer_or_supplier.short_description = 'Customer/Supplier'

    def mark_as_confirmed(self, request, queryset):
        """Mark selected orders as confirmed"""
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} orders marked as confirmed.')
    mark_as_confirmed.short_description = "Mark as confirmed"

    def mark_as_processing(self, request, queryset):
        """Mark selected orders as processing"""
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} orders marked as processing.')
    mark_as_processing.short_description = "Mark as processing"

    def mark_as_shipped(self, request, queryset):
        """Mark selected orders as shipped"""
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} orders marked as shipped.')
    mark_as_shipped.short_description = "Mark as shipped"

    def get_queryset(self, request):
        """Optimize database queries"""
        return super().get_queryset(request).select_related('customer', 'supplier', 'created_by')


# ========================================================================
# WAREHOUSE ADMIN - ADD THIS NEW ADMIN
# ========================================================================

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'city', 'state', 'is_active', 'created_at')
    list_filter = ('is_active', 'state', 'created_at')
    search_fields = ('name', 'manager__username', 'city', 'address')
    ordering = ['name']
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Warehouse Information', {
            'fields': ('name', 'manager'),
            'description': 'Basic warehouse identification and management'
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'zipcode'),
            'description': 'Warehouse location details'
        }),
        ('Status', {
            'fields': ('is_active', 'created_at'),
            'description': 'Warehouse operational status'
        }),
    )


# ========================================================================
# PRODUCT LOCATION ADMIN - ADD THIS NEW ADMIN
# ========================================================================

@admin.register(ProductLocation)
class ProductLocationAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity', 'section')
    list_filter = ('warehouse',)
    search_fields = ('product__name', 'product__sku', 'warehouse__name', 'section')
    ordering = ['warehouse', 'product']

    def get_queryset(self, request):
        """Optimize database queries"""
        return super().get_queryset(request).select_related('product', 'warehouse')


# ========================================================================
# ADMIN SITE CUSTOMIZATION
# ========================================================================

# Customize the admin site header and title
admin.site.site_header = "Inventory Management CRM Administration"
admin.site.site_title = "Inventory CRM Admin"  
admin.site.index_title = "Welcome to Inventory Management CRM"
