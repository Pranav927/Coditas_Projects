from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count, F
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .forms import (
    SignUpForm, CustomerForm, CategoryForm, SupplierForm, ProductForm,
    StockMovementForm, OrderForm, OrderItemForm, 
    ProductSearchForm, CustomerSearchForm, OrderSearchForm
)
from .models import (
    Customer, Product, Category, Supplier, StockMovement, Order, 
    OrderItem, Warehouse, ProductLocation
)

def home(request):
    """Enhanced main dashboard with inventory overview and original CRM login"""
    customers = Customer.objects.all()  # CHANGED FROM: Record.objects.all()

    # Handle login form submission (keep existing login logic)
    if request.method == 'POST' and not request.user.is_authenticated:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.error(request, "There was an error please try logging in...")
            return redirect('home')

    # ============ NEW INVENTORY DASHBOARD FEATURES ============
    # If user is authenticated, show enhanced dashboard
    if request.user.is_authenticated:
        # Dashboard statistics
        total_products = Product.objects.filter(is_active=True).count()
        low_stock_products = Product.objects.filter(
            quantity_in_stock__lte=F('minimum_stock_level'), 
            is_active=True
        ).count()
        total_customers = Customer.objects.count()  # CHANGED FROM: Record
        pending_orders = Order.objects.filter(status='pending').count()

        # Recent activities for dashboard
        recent_stock_movements = StockMovement.objects.select_related('product')[:5]
        recent_orders = Order.objects.select_related('customer', 'supplier')[:5]
        low_stock_items = Product.objects.filter(
            quantity_in_stock__lte=F('minimum_stock_level'), 
            is_active=True
        ).select_related('category', 'supplier')[:10]

        context = {
            'customers': customers,  # Keep for original CRM table
            'total_products': total_products,
            'low_stock_products': low_stock_products,
            'total_customers': total_customers,
            'pending_orders': pending_orders,
            'recent_stock_movements': recent_stock_movements,
            'recent_orders': recent_orders,
            'low_stock_items': low_stock_items,
        }
        return render(request, 'inventory_dashboard.html', context)  # NEW TEMPLATE
    else:
        # ============ KEEP ORIGINAL LOGIN INTERFACE ============
        return render(request, 'home.html', {'customers': customers})  # CHANGED: customers instead of records


# ========================================================================
# EXISTING AUTHENTICATION VIEWS - MINIMAL CHANGES
# ========================================================================
# WHAT TO DO: Keep these views but update the model references

def login_view(request):
    """Keep this placeholder view as is"""
    pass

def logout_user(request):
    """Keep existing logout functionality - NO CHANGES NEEDED"""
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')

def register_user(request):
    """Keep existing registration - MINIMAL CHANGES"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered and are now logged in!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


# ========================================================================
# CUSTOMER MANAGEMENT VIEWS - UPDATE FROM RECORD VIEWS
# ========================================================================
# WHAT TO DO: Update your existing record views to work with Customer model

@login_required
def customer_record(request, pk):
    """Enhanced customer detail view (was customer_record)"""
    # CHANGED FROM: customer_record = Record.objects.get(id=pk)
    customer = get_object_or_404(Customer, id=pk)

    # ============ NEW FEATURE: Customer order history ============
    customer_orders = Order.objects.filter(customer=customer).order_by('-created_at')

    context = {
        'customer_record': customer,  # Keep same variable name for template compatibility
        'customer_orders': customer_orders  # New feature
    }
    return render(request, 'customer_record.html', context)  # Same template name

@login_required
def delete_customer(request, pk):
    """Delete customer (was delete_record)"""
    # CHANGED FROM: delete_it = Record.objects.get(id=pk)
    customer = get_object_or_404(Customer, id=pk)
    customer.delete()
    messages.success(request, "Customer record has been deleted!")
    return redirect('home')

@login_required  
def add_customer(request):
    """Add customer (was add_record)"""
    # CHANGED FROM: form = AddRecordForm(request.POST or None)
    form = CustomerForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Customer Added Successfully!")  # Updated message
            return redirect('home')
    return render(request, 'add_customer.html', {'form': form})  # Updated template name

@login_required
def update_customer(request, pk):
    """Update customer (was update_record)"""
    # CHANGED FROM: current_record = Record.objects.get(id=pk)
    customer = get_object_or_404(Customer, id=pk)
    # CHANGED FROM: form = AddRecordForm(request.POST or None, instance=current_record)
    form = CustomerForm(request.POST or None, instance=customer)
    if form.is_valid():
        form.save()
        messages.success(request, "Customer record has been updated!")
        return redirect('home')
    return render(request, 'update_customer.html', {'form': form})


# ========================================================================
# NEW PRODUCT MANAGEMENT VIEWS - ADD ALL OF THESE
# ========================================================================
# WHAT TO DO: Add these completely new views for product management

@login_required
def product_list(request):
    """Display all products with search and filtering"""
    search_form = ProductSearchForm(request.GET or None)
    products = Product.objects.select_related('category', 'supplier').filter(is_active=True)

    # Apply search filters
    if search_form.is_valid():
        search = search_form.cleaned_data['search']
        category = search_form.cleaned_data['category']
        supplier = search_form.cleaned_data['supplier']
        stock_status = search_form.cleaned_data['stock_status']

        if search:
            products = products.filter(
                Q(name__icontains=search) | 
                Q(sku__icontains=search) | 
                Q(description__icontains=search)
            )
        if category:
            products = products.filter(category=category)
        if supplier:
            products = products.filter(supplier=supplier)
        if stock_status == 'low':
            products = products.filter(quantity_in_stock__lte=F('minimum_stock_level'))
        elif stock_status == 'out_of_stock':
            products = products.filter(quantity_in_stock=0)
        elif stock_status == 'in_stock':
            products = products.filter(quantity_in_stock__gt=0)

    # Pagination
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_form': search_form
    }
    return render(request, 'product_list.html', context)

@login_required
def product_detail(request, pk):
    """Display detailed product information"""
    product = get_object_or_404(Product, id=pk)
    stock_movements = product.stock_movements.all()[:20]
    context = {
        'product': product,
        'stock_movements': stock_movements
    }
    return render(request, 'product_detail.html', context)

@login_required
def add_product(request):
    """Add new product"""
    form = ProductForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' added successfully!")
            return redirect('product_list')
    return render(request, 'add_product.html', {'form': form})

@login_required
def update_product(request, pk):
    """Update existing product"""
    product = get_object_or_404(Product, id=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, "Product updated successfully!")
        return redirect('product_detail', pk=pk)
    return render(request, 'update_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, pk):
    """Soft delete product (deactivate)"""
    product = get_object_or_404(Product, id=pk)
    product.is_active = False
    product.save()
    messages.success(request, f"Product '{product.name}' has been deactivated!")
    return redirect('product_list')


# ========================================================================
# CATEGORY MANAGEMENT VIEWS - ADD THESE
# ========================================================================

@login_required
def category_list(request):
    """Display all categories"""
    categories = Category.objects.annotate(product_count=Count('products')).order_by('name')
    return render(request, 'category_list.html', {'categories': categories})

@login_required
def add_category(request):
    """Add new category"""
    form = CategoryForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' added successfully!")
            return redirect('category_list')
    return render(request, 'add_category.html', {'form': form})


# ========================================================================
# SUPPLIER MANAGEMENT VIEWS - ADD THESE
# ========================================================================

@login_required
def supplier_list(request):
    """Display all active suppliers"""
    suppliers = Supplier.objects.annotate(product_count=Count('products')).filter(is_active=True)
    return render(request, 'supplier_list.html', {'suppliers': suppliers})

@login_required
def supplier_detail(request, pk):
    """Display detailed supplier information"""
    supplier = get_object_or_404(Supplier, id=pk)
    supplier_products = supplier.products.filter(is_active=True)
    supplier_orders = supplier.orders.all()[:10]
    context = {
        'supplier': supplier,
        'supplier_products': supplier_products,
        'supplier_orders': supplier_orders
    }
    return render(request, 'supplier_detail.html', context)

@login_required
def add_supplier(request):
    """Add new supplier"""
    form = SupplierForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f"Supplier '{supplier.name}' added successfully!")
            return redirect('supplier_list')
    return render(request, 'add_supplier.html', {'form': form})


# ========================================================================
# STOCK MOVEMENT VIEWS - ADD THESE
# ========================================================================

@login_required
def stock_movement_list(request):
    """Display all stock movements"""
    movements = StockMovement.objects.select_related('product', 'created_by').order_by('-created_at')

    # Pagination
    paginator = Paginator(movements, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'stock_movement_list.html', {'page_obj': page_obj})

@login_required
def add_stock_movement(request):
    """Record new stock movement"""
    form = StockMovementForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            movement = form.save(commit=False)
            movement.created_by = request.user
            movement.save()
            messages.success(request, f"Stock movement recorded for '{movement.product.name}'!")
            return redirect('stock_movement_list')
    return render(request, 'add_stock_movement.html', {'form': form})


# ========================================================================
# ORDER MANAGEMENT VIEWS - ADD THESE
# ========================================================================

@login_required
def order_list(request):
    """Display all orders with search and filtering"""
    search_form = OrderSearchForm(request.GET or None)
    orders = Order.objects.select_related('customer', 'supplier', 'created_by').order_by('-created_at')

    # Apply search filters
    if search_form.is_valid():
        search = search_form.cleaned_data['search']
        order_type = search_form.cleaned_data['order_type']
        status = search_form.cleaned_data['status']
        date_from = search_form.cleaned_data['date_from']
        date_to = search_form.cleaned_data['date_to']

        if search:
            orders = orders.filter(
                Q(order_number__icontains=search) |
                Q(customer__first_name__icontains=search) |
                Q(customer__last_name__icontains=search) |
                Q(supplier__name__icontains=search)
            )
        if order_type:
            orders = orders.filter(order_type=order_type)
        if status:
            orders = orders.filter(status=status)
        if date_from:
            orders = orders.filter(order_date__gte=date_from)
        if date_to:
            orders = orders.filter(order_date__lte=date_to)

    # Pagination
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_form': search_form
    }
    return render(request, 'order_list.html', context)

@login_required
def order_detail(request, pk):
    """Display detailed order information"""
    order = get_object_or_404(Order, id=pk)
    order_items = order.items.select_related('product').all()
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'order_detail.html', context)

@login_required
def add_order(request):
    """Create new order"""
    form = OrderForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            messages.success(request, f"Order '{order.order_number}' created successfully!")
            return redirect('order_detail', pk=order.id)
    return render(request, 'add_order.html', {'form': form})


# ========================================================================
# REPORTS AND ANALYTICS VIEWS - ADD THESE
# ========================================================================

@login_required
def inventory_reports(request):
    """Comprehensive inventory reporting dashboard"""
    # Stock summary
    total_products = Product.objects.filter(is_active=True).count()
    low_stock_count = Product.objects.filter(
        quantity_in_stock__lte=F('minimum_stock_level'), 
        is_active=True
    ).count()
    out_of_stock_count = Product.objects.filter(
        quantity_in_stock=0, 
        is_active=True
    ).count()

    # Recent movements summary
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    recent_movements = StockMovement.objects.filter(
        created_at__date__gte=week_ago
    ).values('movement_type').annotate(
        count=Count('id'),
        total_quantity=Sum('quantity')
    )

    # Top products by movement activity
    top_products = Product.objects.annotate(
        movement_count=Count('stock_movements')
    ).order_by('-movement_count')[:10]

    context = {
        'total_products': total_products,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'recent_movements': recent_movements,
        'top_products': top_products
    }
    return render(request, 'inventory_reports.html', context)


# ========================================================================
# AJAX VIEWS FOR DYNAMIC FUNCTIONALITY - ADD THESE
# ========================================================================

@login_required
def get_product_info(request):
    """Get product information for AJAX requests"""
    product_id = request.GET.get('product_id')
    if product_id:
        try:
            product = Product.objects.get(id=product_id)
            data = {
                'name': product.name,
                'sku': product.sku,
                'selling_price': str(product.selling_price),
                'stock_quantity': product.quantity_in_stock,
                'is_low_stock': product.is_low_stock
            }
            return JsonResponse(data)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    return JsonResponse({'error': 'No product ID provided'}, status=400)

@login_required
def update_order_status(request, pk):
    """Update order status via AJAX"""
    if request.method == 'POST':
        order = get_object_or_404(Order, id=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Order.ORDER_STATUS):
            order.status = new_status
            order.save()
            return JsonResponse({'success': True, 'message': f'Order status updated to {new_status}'})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


# ========================================================================
# BACKWARD COMPATIBILITY VIEWS - ADD THESE
# ========================================================================
# WHAT TO DO: Add these to maintain compatibility with your existing URLs

# Legacy view names that redirect to new customer views
def customer_record_legacy(request, pk):
    """Legacy support for 'record' URLs"""
    return customer_record(request, pk)

def delete_record(request, pk):
    """Legacy support for 'delete_record' URLs"""
    return delete_customer(request, pk)

def add_record(request):
    """Legacy support for 'add_record' URLs"""
    return add_customer(request)

def update_record(request, pk):
    """Legacy support for 'update_record' URLs"""
    return update_customer(request, pk)