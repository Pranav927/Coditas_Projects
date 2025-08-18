from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Customer, Product, Category, Supplier, StockMovement, Order, OrderItem, Warehouse

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = 'Password must contain at least 8 characters and cannot be too similar to your other information.'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'

class CustomerForm(forms.ModelForm):
    # ============ EXISTING FIELDS - KEEP EXACTLY AS IS ============
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"First Name", "class":"form-control"}), label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Last Name", "class":"form-control"}), label="")
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")
    phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone", "class":"form-control"}), label="")
    address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Address", "class":"form-control"}), label="")
    city = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"City", "class":"form-control"}), label="")
    state = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"State", "class":"form-control"}), label="")
    zipcode = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Zipcode", "class":"form-control"}), label="")

    # ============ NEW ENHANCED FIELDS - ADDING THESE ============
    customer_type = forms.ChoiceField(
        choices=[('individual', 'Individual'), ('business', 'Business'), ('wholesale', 'Wholesale')], 
        widget=forms.Select(attrs={"class":"form-control"}), 
        label="Customer Type"
    )
    credit_limit = forms.DecimalField(
        required=False, 
        widget=forms.NumberInput(attrs={"placeholder":"Credit Limit", "class":"form-control", "step":"0.01"}), 
        label="Credit Limit (Optional)"
    )
    notes = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={"placeholder":"Additional Notes", "class":"form-control", "rows":"3"}), 
        label="Notes (Optional)"
    )

    class Meta:
        model = Customer  # CHANGED FROM: Record TO: Customer
        exclude = ("user",)  # Keep this exclusion


# ========================================================================
# NEW INVENTORY MANAGEMENT FORMS - ADD ALL OF THESE
# ========================================================================
# WHAT TO DO: Add these completely new forms for inventory functionality

class CategoryForm(forms.ModelForm):
    """Form for managing product categories"""
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":"Category Name", "class":"form-control"}), label="Category Name")
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={"placeholder":"Description (Optional)", "class":"form-control", "rows":"3"}), label="Description")

    class Meta:
        model = Category
        fields = ['name', 'description']


class SupplierForm(forms.ModelForm):
    """Form for managing suppliers/vendors"""
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":"Supplier Name", "class":"form-control"}), label="Supplier Name")
    contact_person = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder":"Contact Person (Optional)", "class":"form-control"}), label="Contact Person")
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder":"Email Address", "class":"form-control"}), label="Email")
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":"Phone Number", "class":"form-control"}), label="Phone")
    address = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":"Address", "class":"form-control"}), label="Address")
    city = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":"City", "class":"form-control"}), label="City")
    state = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":"State", "class":"form-control"}), label="State")
    zipcode = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":"Zipcode", "class":"form-control"}), label="Zipcode")

    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone', 'address', 'city', 'state', 'zipcode']


class ProductForm(forms.ModelForm):
    """Form for managing products"""
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":"Product Name", "class":"form-control"}), label="Product Name")
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={"placeholder":"Product Description (Optional)", "class":"form-control", "rows":"3"}), label="Description")
    sku = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder":"SKU (Stock Keeping Unit)", "class":"form-control"}), label="SKU")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={"class":"form-control"}), label="Category", empty_label="Select Category")
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.filter(is_active=True), widget=forms.Select(attrs={"class":"form-control"}), label="Supplier", empty_label="Select Supplier")
    cost_price = forms.DecimalField(required=True, widget=forms.NumberInput(attrs={"placeholder":"Cost Price", "class":"form-control", "step":"0.01"}), label="Cost Price")
    selling_price = forms.DecimalField(required=True, widget=forms.NumberInput(attrs={"placeholder":"Selling Price", "class":"form-control", "step":"0.01"}), label="Selling Price")
    quantity_in_stock = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"placeholder":"Current Stock Quantity", "class":"form-control"}), label="Stock Quantity")
    minimum_stock_level = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"placeholder":"Minimum Stock Alert Level", "class":"form-control", "value":"10"}), label="Minimum Stock Level")
    maximum_stock_level = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"placeholder":"Maximum Stock Capacity", "class":"form-control", "value":"1000"}), label="Maximum Stock Level")

    class Meta:
        model = Product
        fields = ['name', 'description', 'sku', 'category', 'supplier', 'cost_price', 'selling_price', 
                 'quantity_in_stock', 'minimum_stock_level', 'maximum_stock_level']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure only active suppliers are shown
        self.fields['supplier'].queryset = Supplier.objects.filter(is_active=True)


class StockMovementForm(forms.ModelForm):
    """Form for recording stock movements"""
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_active=True), 
        widget=forms.Select(attrs={"class":"form-control"}), 
        label="Product", empty_label="Select Product"
    )
    movement_type = forms.ChoiceField(
        choices=StockMovement.MOVEMENT_TYPES, 
        widget=forms.Select(attrs={"class":"form-control"}), 
        label="Movement Type"
    )
    quantity = forms.IntegerField(
        required=True, 
        widget=forms.NumberInput(attrs={"placeholder":"Quantity", "class":"form-control", "min":"1"}), 
        label="Quantity"
    )
    reference = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={"placeholder":"Reference Number (Optional)", "class":"form-control"}), 
        label="Reference"
    )
    notes = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={"placeholder":"Additional Notes (Optional)", "class":"form-control", "rows":"3"}), 
        label="Notes"
    )

    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'reference', 'notes']


class OrderForm(forms.ModelForm):
    """Form for creating orders"""
    order_type = forms.ChoiceField(
        choices=Order.ORDER_TYPES, 
        widget=forms.Select(attrs={"class":"form-control"}), 
        label="Order Type"
    )
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(), 
        widget=forms.Select(attrs={"class":"form-control"}), 
        label="Customer", empty_label="Select Customer", required=False
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.filter(is_active=True), 
        widget=forms.Select(attrs={"class":"form-control"}), 
        label="Supplier", empty_label="Select Supplier", required=False
    )
    status = forms.ChoiceField(
        choices=Order.ORDER_STATUS, 
        widget=forms.Select(attrs={"class":"form-control"}), 
        label="Status"
    )
    expected_delivery_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={"class":"form-control", "type":"date"}), 
        label="Expected Delivery Date"
    )
    notes = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={"placeholder":"Order Notes", "class":"form-control", "rows":"3"}), 
        label="Notes"
    )

    class Meta:
        model = Order
        fields = ['order_type', 'customer', 'supplier', 'status', 'expected_delivery_date', 'notes']

    def clean(self):
        """Validate that customer or supplier is selected based on order type"""
        cleaned_data = super().clean()
        order_type = cleaned_data.get('order_type')
        customer = cleaned_data.get('customer')
        supplier = cleaned_data.get('supplier')

        if order_type == 'sale' and not customer:
            raise forms.ValidationError("Customer is required for sales orders.")
        if order_type == 'purchase' and not supplier:
            raise forms.ValidationError("Supplier is required for purchase orders.")

        return cleaned_data


class OrderItemForm(forms.ModelForm):
    """Form for adding items to orders"""
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_active=True), 
        widget=forms.Select(attrs={"class":"form-control"}), 
        label="Product", empty_label="Select Product"
    )
    quantity = forms.IntegerField(
        required=True, 
        widget=forms.NumberInput(attrs={"placeholder":"Quantity", "class":"form-control", "min":"1"}), 
        label="Quantity"
    )
    unit_price = forms.DecimalField(
        required=True, 
        widget=forms.NumberInput(attrs={"placeholder":"Unit Price", "class":"form-control", "step":"0.01"}), 
        label="Unit Price"
    )

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'unit_price']


# ========================================================================
# SEARCH AND FILTER FORMS - ADD THESE FOR BETTER UX
# ========================================================================

class ProductSearchForm(forms.Form):
    """Form for searching and filtering products"""
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder":"Search products by name or SKU...", "class":"form-control"}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, widget=forms.Select(attrs={"class":"form-control"}), empty_label="All Categories")
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.filter(is_active=True), required=False, widget=forms.Select(attrs={"class":"form-control"}), empty_label="All Suppliers")
    stock_status = forms.ChoiceField(
        choices=[('', 'All Stock Levels'), ('low', 'Low Stock'), ('in_stock', 'In Stock'), ('out_of_stock', 'Out of Stock')], 
        required=False, widget=forms.Select(attrs={"class":"form-control"})
    )


class CustomerSearchForm(forms.Form):
    """Form for searching customers"""
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder":"Search customers by name or email...", "class":"form-control"}))
    customer_type = forms.ChoiceField(
        choices=[('', 'All Types'), ('individual', 'Individual'), ('business', 'Business'), ('wholesale', 'Wholesale')], 
        required=False, widget=forms.Select(attrs={"class":"form-control"})
    )


class OrderSearchForm(forms.Form):
    """Form for searching and filtering orders"""
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder":"Search orders by number or customer...", "class":"form-control"}))
    order_type = forms.ChoiceField(choices=[('', 'All Types')] + Order.ORDER_TYPES, required=False, widget=forms.Select(attrs={"class":"form-control"}))
    status = forms.ChoiceField(choices=[('', 'All Statuses')] + Order.ORDER_STATUS, required=False, widget=forms.Select(attrs={"class":"form-control"}))
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={"class":"form-control", "type":"date"}), label="From Date")
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={"class":"form-control", "type":"date"}), label="To Date")