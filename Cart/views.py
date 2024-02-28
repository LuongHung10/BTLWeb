from django.shortcuts import render, redirect
from home.models import Item
from django.contrib.auth.decorators import login_required
from .cart import Cart

@login_required(login_url="/signin")
def cart_add(request, id):
    cart = Cart(request)
    item = Item.objects.get(id=id)
    cart.add(item=item)
    return redirect("Cart:cart_detail")


@login_required(login_url="/signin")
def item_clear(request, id):
    cart = Cart(request)
    item = Item.objects.get(id=id)
    cart.remove(item)
    return redirect("Cart:cart_detail")


@login_required(login_url="/signin")
def item_increment(request, id):
    cart = Cart(request)
    item = Item.objects.get(id=id)
    cart.add(item=item)
    return redirect("Cart:cart_detail")


@login_required(login_url="/signin")
def item_decrement(request, id):
    cart = Cart(request)
    item = Item.objects.get(id=id)
    cart.decrement(item=item)
    return redirect("Cart:cart_detail")


@login_required(login_url="/signin")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("Cart:cart_detail")


@login_required(login_url="/signin")
def cart_detail(request):
    cart = Cart(request)
    cart_items = cart.cart.values()  # Lấy danh sách sản phẩm từ giỏ hàng
    subtotal = calculate_subtotal(cart_items)  # Tính tổng giá trị các sản phẩm
    tax_percentage = 0.05  # Thuế 5%
    shipping_percentage = 0.05  # Phí vận chuyển 5%
    tax = subtotal * tax_percentage
    shipping = subtotal * shipping_percentage
    total = subtotal + tax + shipping

    return render(request, 'home/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'total': total,
    })

def calculate_subtotal(cart_items):
    # Hàm này tính tổng giá trị các sản phẩm trong giỏ hàng
    subtotal = 0
    for item in cart_items:
        subtotal += float(item['price']) * item['quantity']
    return subtotal
