from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# Función para conseguir el id de sesión de las cookies de la página
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    # Obtener el producto por ID
    product = get_object_or_404(Product, id=product_id)

    # Obtener o crear el carrito
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    # Verificar si el producto ya existe en el carrito
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        # Incrementar la cantidad del producto existente
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    else:
        # Crear un nuevo elemento en el carrito con cantidad 1
        CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )

    return redirect('cart')



def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:

        #cart_item = CartItem.objects.get(product=product, cart= cart, id= cart_item_id)

        cart_item = CartItem.objects.get(product=product, cart= cart, id = cart_item_id)
            
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
        
    return redirect('cart')



def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id= _cart_id(request))
    product = get_object_or_404(Product, id= product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id= cart_item_id)
    cart_item.delete()
    return redirect('cart')




def cart(request):
    total = 0
    quantity = 0
    cart_items = []
    tax= 0
    grand_total = 0

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.product.price_public * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)