from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01, message="Price must be greater than zero")]
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return self.name
    
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock > 0
    
    def restock(self, quantity):
        """Add quantity to stock"""
        if quantity > 0:
            self.stock += quantity
            self.save()
            return True
        return False
    
    def reduce_stock(self, quantity):
        """Reduce stock by quantity"""
        if quantity <= self.stock and quantity > 0:
            self.stock -= quantity
            self.save()
            return True
        return False
    
    def to_dict(self):
        """Convert product to dictionary for JSON response"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'image': self.image.url if self.image else '',
            'stock': self.stock,
            'in_stock': self.is_in_stock()
        }
