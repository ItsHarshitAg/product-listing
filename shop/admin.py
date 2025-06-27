from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'stock_status')
    search_fields = ('name', 'description')
    list_filter = ('stock',)
    list_editable = ('stock',)  # Allow editing stock directly from the list view
    readonly_fields = ('stock_status',)
    
    def stock_status(self, obj):
        if obj.stock <= 0:
            return 'Out of Stock'
        elif obj.stock < 5:
            return 'Low Stock'
        else:
            return 'In Stock'
    
    stock_status.short_description = 'Inventory Status'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image')
        }),
        ('Pricing and Inventory', {
            'fields': ('price', 'stock', 'stock_status'),
            'description': 'Update product price and stock levels here. Stock status is automatically calculated.'
        }),
    )
