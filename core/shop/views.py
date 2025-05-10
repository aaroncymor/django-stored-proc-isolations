from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction, connection
from .models import Product, Order

# Create your views here.
def place_order_snapshot(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 0))
        except ValueError:
            messages.error(request, 'Invalid quantity.')
            return render(request, 'order_form.html', {'product': product})

        if quantity <= 0:
            messages.error(request, 'Quantity must be greater than 0.')
            return render(request, 'order_form.html', {'product': product})

        def create_order():
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # Set the isolation level to SNAPSHOT / REPEATABLE READ
                    cursor.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ')
                    
                    # Re-read the product within the transaction
                    fresh_product = Product.objects.get(pk=product_id)
                    
                    if fresh_product.stock < quantity:
                        messages.error(request, 'Not enough stock available.')
                        return False

                    Order.objects.create(product=product, quantity=quantity)
                    fresh_product.stock -= quantity
                    fresh_product.save()
                    messages.success(request, 'Order placed successfully.')
                    return True

        if create_order():
            # Pass the product_id to the success page
            return redirect('order_success', product_id=product_id)

        return render(request, 'order_form.html', {'product': product})
    
    return render(request, 'order_form.html', {'product': product})

def order_success(request, product_id=None):
    context = {}
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
        context['product'] = product
    return render(request, 'order_success.html', context)

def product_detail_read_committed(request, product_id):
    with transaction.atomic():
        with connection.cursor() as cursor:
            # Explicitly set the isolation level to READ COMMITTED (often the default)
            cursor.execute('SET TRANSACTION ISOLATION LEVEL READ COMMITTED')
            product = get_object_or_404(Product, pk=product_id)
            return render(request, 'product_detail.html', {'product': product})

def product_detail_default(request, product_id):
    # Rely on Django's default isolation level (usually READ COMMITTED) 
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

def potentially_risky_view_read_uncommitted(request, product_id):
    with transaction.atomic():
        with connection.cursor() as cursor:
            # Explicitly set the isolation level to READ UNCOMMITTED (lower isolation level)
            cursor.execute('SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED')
            product = Product.objects.get(pk=product_id)
            
            # The data from the product might be from an uncommitted transaction
            # or an uncommitted write operation
            return render(request, 'product_detail.html', {'product': product})