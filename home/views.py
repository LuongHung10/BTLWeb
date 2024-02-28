from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from shopquanao import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from Cart.cart import Cart
from . token import generate_token

# Create your views here.
def index(request):
    items = Item.objects.all()
    dress_category = Category.objects.get(name='Váy')
    dress_items = Item.objects.filter(category=dress_category)
    shirt_category = Category.objects.get(name='Áo thun')
    shirt_items = Item.objects.filter(category=shirt_category)
    jacket_category = Category.objects.get(name='Đồ mặc ngoài')
    jacket_items = Item.objects.filter(category=jacket_category)
    jean_category = Category.objects.get(name='Quần')
    jean_items = Item.objects.filter(category=jean_category)
    return render(request,'home/index.html',{
        'items': items[:8],
        'dress_items': dress_items[:8],
        'dress_category': dress_category,
        'shirt_items': shirt_items[:8],
        'shirt_category': shirt_category,
        'jacket_items': jacket_items[:8],
        'jacket_category': jacket_category,
        'jean_category': jean_category,
        'jean_items': jean_items[:8],
    })

def signin(request):    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username = username, password = password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Account Does Not Exist')
            return redirect('/signin')
    else:
        return render(request, 'home/signin.html')
    

def signout(request):
    logout(request)
    return redirect('/')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        messages.success(request, "Your Account has been activated!")
        return redirect('/signin')
    else:
        messages.error(request, "Activation link is invalid!")
    
    return redirect('/index')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email = email).exists():
                messages.info(request, 'Email Already Used')
                return redirect('/register')
                
            elif User.objects.filter(username = username).exists():
                messages.info(request, 'Username Already Used')
                return redirect('/register')
                
            else:
                user = User.objects.create_user(username = username, email = email, password = password)
                    
                user.is_active = False
                user.save()
                    
                #Gửi tin nhắn cho email
                subject = "Welcome to my project"
                message = "Hello " + username + "! \n" + "Welcome to my project\n Thank you for joining my project to have some fun"
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    
                    
                current_site = get_current_site(request)
                email_subject = "Confirm your account @ Project - Django Signin"
                message2 = render_to_string('confirmation.html', {
                    'username': user.username,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user),
                })
                email = EmailMessage(
                    email_subject,
                    message2,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
                email.fail_silently = True
                email.send()
                return redirect('/success_register')
                
        else:
            messages.info(request, 'Password Not The Same')
            return redirect('/register')
            
    else:
        return render(request, 'home/register.html')

@login_required(login_url="/signin")
def checkout(request):
    cart = Cart(request)
    cart_items = cart.cart.values()
    total_amount = calculate_total(cart_items)
    if request.method == 'POST':
        form_data = request.POST

        # Tạo đơn hàng
        order = Order.objects.create(
            first_name=form_data['fname'],
            last_name=form_data['lname'],
            email=form_data['email'],
            phone=form_data['phone'],
            address=form_data['address'],
            total_amount=total_amount
        )

        # Lưu thông tin sản phẩm trong giỏ hàng vào đơn hàng thông qua OrderItem
        for item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product_name=item['name'],
                quantity=item['quantity'],
                price=item['price']
            )

        # Xóa dữ liệu trong giỏ hàng sau khi tạo đơn hàng
        cart.clear()

        # Chuyển hướng hoặc hiển thị thông báo đơn hàng đã được tạo thành công
        return redirect('/success_page')  # Chuyển hướng đến trang thông báo đơn hàng đã được tạo thành công
    else:
        # Nếu không phải là phương thức POST, render trang checkout với form thông tin đơn hàng
        return render(request, 'home/checkout.html', {
        'cart_items': cart_items,
        'total': total_amount,
        })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'home/detail.html',{
        'item': item,
    })

def calculate_total(cart_items):
    # Hàm này tính tổng giá trị các sản phẩm trong giỏ hàng
    subtotal = 0
    for item in cart_items:
        subtotal += float(item['price']) * item['quantity']
    tax_percentage = 0.05  # Thuế 5%
    shipping_percentage = 0.05  # Phí vận chuyển 5%
    tax = subtotal * tax_percentage
    shipping = subtotal * shipping_percentage
    total = subtotal + tax + shipping
    return total

def success_page(request):
    return render(request, 'home/success_page.html')

def success_register(request):
    return render(request, 'home/success_register.html')

def product_page(request, category_id=None):
    categories = Category.objects.all()
    if category_id is not None:
        category = Category.objects.get(id=category_id)
        items = Item.objects.filter(category=category)
    else:
        # Nếu không có danh mục được chọn, hiển thị toàn bộ sản phẩm
        items = Item.objects.all()
        category = None  # Gán category là None để sử dụng trong template

    return render(request, 'home/product.html', {'items': items, 'categories': categories})

def about_page(request):
    return render(request, 'home/about.html')