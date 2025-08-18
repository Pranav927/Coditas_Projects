from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Main dashboard
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>/', views.customer_record, name='record'),  # Record
    path('delete_record/<int:pk>/', views.delete_customer, name='delete_record'),  # Delete record
    path('add_record/', views.add_customer, name='add_record'),  # Add record  
    path('update_record/<int:pk>/', views.update_customer, name='update_record'),  # Update record
    # Modern customer URLs (cleaner naming)
    path('customer/<int:pk>/', views.customer_record, name='customer_record'),
    path('customers/', views.home, name='customer_list'),  # Redirects to main dashboard
    path('customer/add/', views.add_customer, name='add_customer'),
    path('customer/<int:pk>/update/', views.update_customer, name='update_customer'),
    path('customer/<int:pk>/delete/', views.delete_customer, name='delete_customer'),

    # ========================================================================
    # PRODUCT MANAGEMENT URLS
    # ========================================================================
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:pk>/update/', views.update_product, name='update_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),

    # ========================================================================
    # CATEGORY MANAGEMENT URLS
    # ========================================================================

    path('categories/', views.category_list, name='category_list'),
    path('category/add/', views.add_category, name='add_category'),
    # Future: path('category/<int:pk>/', views.category_detail, name='category_detail'),
    # Future: path('category/<int:pk>/update/', views.update_category, name='update_category'),
    # Future: path('category/<int:pk>/delete/', views.delete_category, name='delete_category'),

    # ========================================================================
    # SUPPLIER MANAGEMENT URLS
    # ========================================================================

    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('supplier/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('supplier/add/', views.add_supplier, name='add_supplier'),
    # Future: path('supplier/<int:pk>/update/', views.update_supplier, name='update_supplier'),
    # Future: path('supplier/<int:pk>/delete/', views.delete_supplier, name='delete_supplier'),

    # ========================================================================
    # STOCK MOVEMENT URLS
    # ========================================================================

    path('stock-movements/', views.stock_movement_list, name='stock_movement_list'),
    path('stock-movement/add/', views.add_stock_movement, name='add_stock_movement'),
    # Future: path('stock-movement/<int:pk>/', views.stock_movement_detail, name='stock_movement_detail'),

    # ========================================================================
    # ORDER MANAGEMENT URLS
    # ========================================================================

    path('orders/', views.order_list, name='order_list'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('order/add/', views.add_order, name='add_order'),
    # Future: path('order/<int:pk>/update/', views.update_order, name='update_order'),
    # Future: path('order/<int:pk>/delete/', views.delete_order, name='delete_order'),

    # Order status updates (AJAX)
    path('order/<int:pk>/update-status/', views.update_order_status, name='update_order_status'),

    # ========================================================================
    # REPORTS AND ANALYTICS URLS
    # ========================================================================

    path('reports/', views.inventory_reports, name='inventory_reports'),
    path('reports/inventory/', views.inventory_reports, name='inventory_reports_detail'),
    # Future: path('reports/sales/', views.sales_reports, name='sales_reports'),
    # Future: path('reports/purchases/', views.purchase_reports, name='purchase_reports'),
    # Future: path('reports/customers/', views.customer_reports, name='customer_reports'),

    # ========================================================================
    # API ENDPOINTS (AJAX) - ADD THESE
    # ========================================================================

    path('api/product-info/', views.get_product_info, name='get_product_info'),
    # Future API endpoints:
    # path('api/customer-info/', views.get_customer_info, name='get_customer_info'),
    # path('api/stock-check/', views.check_stock, name='check_stock'),
    # path('api/price-history/', views.get_price_history, name='get_price_history'),

    # ========================================================================
    # DASHBOARD AND UTILITY URLS 
    # ========================================================================

    path('dashboard/', views.home, name='dashboard'),  # Alternative dashboard URL
    # Future: path('search/', views.global_search, name='global_search'),
    # Future: path('export/products/', views.export_products, name='export_products'),
    # Future: path('export/customers/', views.export_customers, name='export_customers'),
    # Future: path('import/products/', views.import_products, name='import_products'),

    # ========================================================================
    # WAREHOUSE MANAGEMENT URLS
    # ========================================================================
    # For future implementation:
    # path('warehouses/', views.warehouse_list, name='warehouse_list'),
    # path('warehouse/<int:pk>/', views.warehouse_detail, name='warehouse_detail'),
    # path('warehouse/add/', views.add_warehouse, name='add_warehouse'),
    # path('warehouse/<int:pk>/update/', views.update_warehouse, name='update_warehouse'),

    # ========================================================================
    # QUICK ACCESS URLS
    # ========================================================================

    # Quick add URLs for better UX
    path('quick/product/', views.add_product, name='quick_add_product'),
    path('quick/customer/', views.add_customer, name='quick_add_customer'),
    path('quick/supplier/', views.add_supplier, name='quick_add_supplier'),
    path('quick/stock-movement/', views.add_stock_movement, name='quick_add_stock_movement'),

    # Quick navigation URLs
    path('low-stock/', views.product_list, name='low_stock_products'),  # Will be filtered in view
    path('recent-orders/', views.order_list, name='recent_orders'),
    path('pending-orders/', views.order_list, name='pending_orders'),  # Will be filtered in view
]