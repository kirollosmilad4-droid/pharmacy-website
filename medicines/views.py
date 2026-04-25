from django.shortcuts import render, redirect, get_object_or_404
from .models import Medicine, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout


# 🏠 List + Search + Filter
def medicine_list(request):
    category = request.GET.get('category')
    search = request.GET.get('search')

    medicines = Medicine.objects.all()

    if category:
        medicines = medicines.filter(category=category)

    if search:
        medicines = medicines.filter(name__icontains=search)

    fav_ids = request.session.get('fav', [])

    return render(request, 'medicines/list.html', {
        'medicines': medicines,
        'fav_ids': fav_ids
    })


# 📄 Detail
def medicine_detail(request, id):
    medicine = get_object_or_404(Medicine, id=id)

    related = Medicine.objects.filter(
        category=medicine.category
    ).exclude(id=id)[:4]

    return render(request, 'medicines/detail.html', {
        'medicine': medicine,
        'related': related
    })


# 🛒 Add to Cart
def order_medicine(request, id):
    cart = request.session.get('cart', {})

    id = str(id)

    cart[id] = cart.get(id, 0) + 1

    request.session['cart'] = cart

    return redirect('/')  # شغال مع AJAX عادي


# 🛒 Cart Page
def cart_view(request):
    cart = request.session.get('cart', {})
    medicines = Medicine.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for m in medicines:
        quantity = cart.get(str(m.id), 0)
        total += m.price * quantity

        cart_items.append({
            'medicine': m,
            'quantity': quantity
        })

    return render(request, 'medicines/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# ❌ Remove Item
def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    id = str(id)

    if id in cart:
        del cart[id]

    request.session['cart'] = cart

    return redirect('/cart/')


# 🧹 Clear Cart
def clear_cart(request):
    request.session['cart'] = {}
    return redirect('/cart/')


# 💳 Checkout
def checkout(request):
    cart = request.session.get('cart', {})
    medicines = Medicine.objects.filter(id__in=cart.keys())

    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment = request.POST.get('payment')

        if not name or not phone or not address:
            return render(request, 'medicines/checkout.html', {
                'error': 'كل البيانات مطلوبة'
            })

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=name,
            phone=phone,
            address=address,
            payment_method=payment
        )

        for m in medicines:
            OrderItem.objects.create(
                order=order,
                medicine=m,
                quantity=cart.get(str(m.id), 0)
            )

        request.session['cart'] = {}

        return render(request, 'medicines/success.html', {
            'payment': payment
        })

    return render(request, 'medicines/checkout.html')


# ❤️ Favourite
def add_to_favourite(request, id):
    fav = request.session.get('fav', [])

    if id in fav:
        fav.remove(id)
    else:
        fav.append(id)

    request.session['fav'] = fav

    # 🔥 مهم علشان AJAX يشتغل صح
    return redirect(request.META.get('HTTP_REFERER', '/'))


def favourite_view(request):
    fav_ids = request.session.get('fav', [])
    medicines = Medicine.objects.filter(id__in=fav_ids)

    return render(request, 'medicines/favourite.html', {
        'medicines': medicines
    })


# 👤 Register
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'medicines/register.html', {
                'error': 'اسم المستخدم موجود'
            })

        user = User.objects.create_user(username=username, password=password)
        login(request, user)

        return redirect('/')

    return render(request, 'medicines/register.html')


# 🔐 Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'medicines/login.html', {
                'error': 'بيانات غلط'
            })

    return render(request, 'medicines/login.html')


# 🚪 Logout
def logout_view(request):
    logout(request)
    return redirect('/')


# 📦 Orders
def orders_view(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-id')
    else:
        orders = Order.objects.all().order_by('-id')

    return render(request, 'medicines/orders.html', {
        'orders': orders
    })


# ❌ Cancel Order
def cancel_order(request, id):
    order = get_object_or_404(Order, id=id)

    if request.user == order.user and order.status == "Pending":
        order.status = "Cancelled"
        order.save()

    return redirect('/orders/')