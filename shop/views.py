from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Product

def index(request):
    """Render homepage with products"""
    return render(request, 'shop/index.html')

def cart(request):
    """Render cart page"""
    return render(request, 'shop/cart.html')

def product_list(request):
    """API endpoint to get all products"""
    products = Product.objects.all()
    product_list = [product.to_dict() for product in products]
    return JsonResponse(product_list, safe=False)

@csrf_exempt
def add_to_cart(request):
    """API endpoint to add product to cart"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    data = json.loads(request.body)
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    try:
        product = Product.objects.get(id=product_id)
        
        # Check if we have enough stock
        if product.stock < quantity:
            return JsonResponse({
                'error': f'Not enough stock available. Only {product.stock} remaining.'
            }, status=400)
            
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
    # Initialize cart if not exists
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    cart = request.session['cart']
    
    # Add product to cart or update quantity
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str] = cart[product_id_str] + quantity
    else:
        cart[product_id_str] = quantity
    
    request.session.modified = True
    
    return JsonResponse({
        'success': True,
        'message': f'{product.name} added to cart',
        'cart': cart
    })

@csrf_exempt
def remove_from_cart(request):
    """API endpoint to remove product from cart"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    data = json.loads(request.body)
    product_id = data.get('product_id')
    
    if 'cart' not in request.session or not request.session['cart']:
        return JsonResponse({'error': 'Cart is empty'}, status=400)
    
    cart = request.session['cart']
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        request.session.modified = True
        return JsonResponse({
            'success': True,
            'message': 'Product removed from cart',
            'cart': cart
        })
    else:
        return JsonResponse({'error': 'Product not in cart'}, status=404)

def get_cart(request):
    """API endpoint to get cart contents"""
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    cart = request.session['cart']
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            
            # Ensure we don't have more in cart than available stock
            actual_quantity = min(quantity, product.stock)
            if actual_quantity != quantity:
                cart[product_id] = actual_quantity
                request.session.modified = True
            
            if actual_quantity <= 0:
                continue
                
            item_total = float(product.price) * actual_quantity
            total += item_total
            
            cart_items.append({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'quantity': actual_quantity,
                'item_total': item_total,
                'image': product.image.url if product.image else '',
                'stock': product.stock
            })
        except Product.DoesNotExist:
            # Remove invalid products from cart
            del cart[product_id]
            request.session.modified = True
            continue
    
    return JsonResponse({
        'items': cart_items,
        'total': total,
        'count': sum(item['quantity'] for item in cart_items)
    })

@csrf_exempt
def checkout(request):
    """API endpoint to simulate checkout (clear cart and reduce stock)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    if 'cart' not in request.session or not request.session['cart']:
        return JsonResponse({'error': 'Cart is empty'}, status=400)
    
    cart = request.session['cart']
    purchased_items = []
    
    # Process each item in the cart
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            
            # Check if enough stock is available
            if product.stock < quantity:
                return JsonResponse({
                    'error': f'Not enough stock for {product.name}. Available: {product.stock}'
                }, status=400)
            
            # Reduce stock using the model method
            if product.reduce_stock(quantity):
                # Add to purchased items
                purchased_items.append({
                    'id': product.id,
                    'name': product.name,
                    'quantity': quantity,
                    'price': float(product.price)
                })
            else:
                return JsonResponse({
                    'error': f'Failed to process {product.name}. Please try again.'
                }, status=400)
            
        except Product.DoesNotExist:
            continue
    
    # Clear the cart
    request.session['cart'] = {}
    request.session.modified = True
    
    return JsonResponse({
        'success': True,
        'message': 'Checkout successful! Your order has been placed.',
        'purchased_items': purchased_items
    })

@csrf_exempt
def update_cart_quantity(request):
    """API endpoint to update product quantity in cart"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    data = json.loads(request.body)
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    action = data.get('action', 'set')  # 'set', 'increase', or 'decrease'
    
    # Validate quantity
    if quantity <= 0 and action == 'set':
        return JsonResponse({'error': 'Quantity must be greater than 0'}, status=400)
    
    # Check if cart exists
    if 'cart' not in request.session or not request.session['cart']:
        return JsonResponse({'error': 'Cart is empty'}, status=400)
    
    cart = request.session['cart']
    product_id_str = str(product_id)
    
    # Check if product is in cart
    if product_id_str not in cart:
        return JsonResponse({'error': 'Product not in cart'}, status=404)
    
    # Get current quantity
    current_quantity = cart[product_id_str]
    
    # Update quantity based on action
    if action == 'set':
        new_quantity = quantity
    elif action == 'increase':
        new_quantity = current_quantity + quantity
    elif action == 'decrease':
        new_quantity = current_quantity - quantity
        if new_quantity <= 0:
            # If quantity is zero or negative, remove the product
            del cart[product_id_str]
            request.session.modified = True
            return JsonResponse({
                'success': True,
                'message': 'Product removed from cart',
                'cart': cart
            })
    else:
        return JsonResponse({'error': 'Invalid action'}, status=400)
    
    # Check if we have enough stock
    try:
        product = Product.objects.get(id=product_id)
        if product.stock < new_quantity:
            return JsonResponse({
                'error': f'Not enough stock available. Only {product.stock} remaining.',
                'available_stock': product.stock
            }, status=400)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
    # Update the cart
    cart[product_id_str] = new_quantity
    request.session.modified = True
    
    return JsonResponse({
        'success': True,
        'message': 'Cart updated successfully',
        'product_id': product_id,
        'quantity': new_quantity,
        'cart': cart
    })
