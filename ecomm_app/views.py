from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def render_login(request):
    return render(request, 'login.html')

def render_register(request):
    return render(request, 'register.html')

def process_reg(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        this_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash)
        request.session['first_name'] = this_user.first_name
        request.session['id'] = this_user.id
        return redirect('/')

def process_login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login')
        one_user = User.objects.filter(email = request.POST['email'])
        request.session['id'] = one_user[0].id
        request.session['first_name'] = one_user[0].first_name
        return redirect('/')
    return redirect('/')

def logout(request):
    Cart.objects.all().delete()
    request.session.flush()
    print('COOOOOOOOOOWWWW', Cart.objects.count())
    return redirect('/')


def index(request): 
    if len(request.session.keys()) < 1:
        context = {
            'users': User.objects.all(),
            'items': Item.objects.all(),
            'cats': Cat.objects.all(),
            'carts': Cart.objects.all()
        }
        return render(request, 'index.html', context)
    else:
        context = {
            'user': User.objects.get(id=request.session['id']),
            'items': Item.objects.all(),
            'cats': Cat.objects.all(),
            'carts': Cart.objects.all(),
        }
        return render(request, 'index.html', context)

def show_empty_cart(request):
    return render(request, 'empty_cart.html')

def render_admin(request):
    context = {
        'items': Item.objects.all(),
        'cats': Cat.objects.all()
        }
    return render(request, 'admin_create.html', context)
#     return render(request, 'admin_create.html')

# def admin_create_item(request):
#     context = {
#         'items': Item.objects.all(),
#         'cats': Cat.objects.all()
#         }
#     return render(request, 'admin_create.html', context)

def create_item(request):
    print(request.POST)
    this_cat = Cat.objects.get(id=int(request.POST['cat_id']))
    this_item=Item.objects.create(
        item_name = request.POST['item_name'],
        desc = request.POST['desc'],
        price = request.POST['price'],
        cat = this_cat,
        image = request.FILES['image']
    )
    return redirect('/3227751215')

def display_product(request, item_id):
    context = {
        'item': Item.objects.get(id=item_id)
    }
    return render(request, 'display_product.html', context)

def add_to_cart(request, item_id):
    this_item= Item.objects.get(id=item_id)
    if Cart.objects.count() > 0:
        print(Cart.objects.count())
        this_cart = Cart.objects.get(id=request.session['cart_id'])
        this_cart.items.add(this_item)
        context = {
            'cart': Cart.objects.get(id=request.session['cart_id'])
        }
        return render(request, 'cart.html', context)
    else:
        this_cart = Cart.objects.create(
            user = User.objects.get(id=request.session['id']),
        )
        this_cart.items.add(this_item)
        context = {
            'cart': Cart.objects.get(id=this_cart.id)
        }
        request.session['cart_id'] = this_cart.id
        return render(request, 'cart.html', context)

def render_update_page(request, item_id):
    context = {
        'item': Item.objects.get(id=item_id),
        'cats': Cat.objects.all()
    }
    return render(request, 'admin_update.html', context)

def update_item(request, item_id):
    this_cat = Cat.objects.get(id=int(request.POST['cat_id']))
    item = Item.objects.get(id=item_id)
    item.item_name = request.POST['item_name']
    item.price = request.POST['price']
    item.desc = request.POST['desc']
    item.cat = this_cat
    item.save()
    return redirect('/3227751215')

def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect('/3227751215')

def render_cat_page(request):
    return render(request, 'add_cat.html')

def create_cat(request):
    Cat.objects.create(
        cat_name = request.POST['cat_name']
    )
    return redirect('/3227751215')

def single_product(request, item_id):

    context = {
        'item': Item.objects.get(id=item_id),
        'reviews': Review.objects.all()
        }
    return render(request, 'single_product.html', context)

def display_cat(request, cat_id):
    context = {
        'cat': Cat.objects.get(id=cat_id),
        'items': Item.objects.all()
    }
    return render(request, 'display_cat.html', context)

def display_cart(request):
        context = {
            'cart': Cart.objects.get(id=request.session['cart_id'])
        }
        return render(request, 'cart.html', context)

def display_empty_cart(request):
    return render(request, 'empty_cart.html')

def remove_from_cart(request, item_id):
    this_cart = Cart.objects.get(id=request.session['cart_id'])
    this_item = Item.objects.get(id=item_id)
    this_cart.items.remove(this_item)
    return redirect('/display_cart')

def display_checkout(request):
    if Cart.objects.count() > 0:
        subtotal = 0
        this_cart = Cart.objects.get(id=request.session['cart_id'])
        for product in this_cart.items.all():
            subtotal += product.price
        shipping = 299.99
        total = shipping + subtotal
        request.session['order_total'] = total
        


        context = {
            'cart': Cart.objects.get(id=request.session['cart_id']),
            'subtotal': subtotal,
            'shipping': shipping,
            'total': total
        }
        return render(request, 'display_checkout.html', context)
    else:
        return redirect('/')

def process_order(request):
    this_cart = Cart.objects.get(id=request.session['cart_id'])
    this_order = Order.objects.create(
        user = User.objects.get(id=request.session['id']),
        total = request.session['order_total']
    )
    for item in this_cart.items.all():
        this_order.items.add(item)
    request.session['order_id'] = this_order.id
    this_cart.delete()
    return redirect('/render_order_success')

def render_order_success(request):  
    context = {
        'order': Order.objects.get(id=request.session['order_id'])
    }
    return render(request, 'order_success.html', context)

def display_orders(request):
    context = {
        'user': User.objects.get(id=request.session['id']),
        'orders': Order.objects.all()
    }
    return render(request, 'display_orders.html', context)

def delete_order(request, order_id):
        order = Order.objects.get(id=order_id)
        order.delete()
        return redirect('/display_orders')

def add_review(request, item_id):

    this_review = Review.objects.create(
        title = request.POST['title'],
        review = request.POST['review'],
        user = User.objects.get(id=request.session['id']),
        item = Item.objects.get(id=item_id),
        stars = request.POST['stars']
    )
    return redirect(f'/single_product/{item_id}')