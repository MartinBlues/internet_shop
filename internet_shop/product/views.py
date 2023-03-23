from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CommentForm, Category, OrderItem
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from .filters import ProductFilter
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .forms import OrderForm


def product_list(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')

    categories = Category.objects.all()
    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'products': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'selected_category': int(category_id) if category_id else None,
        'search_query': search_query,
    }
    return render(request, 'product_list.html', context)


@login_required
def add_comment_to_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.author = request.user
            comment.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = CommentForm()
    return render(request, 'product/product_detail.html', {'product': product, 'form': form})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = CommentForm()
    return render(request, 'product/product_detail.html', {'product': product, 'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def add_comment_to_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.author = request.user
            comment.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = CommentForm()
        return render(request, 'product/product_detail.html', {'product': product, 'form': form})

@login_required
def order_create(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Кошик порожній')
        return redirect('product_list')

    order_form = OrderForm(request.POST or None)

    if request.method == 'POST':
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.save()
            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=quantity
                )
            del request.session['cart']
            messages.success(request, 'Замовлення успішно оформлено')
            return redirect('product_list')

    return render(request, 'order_form.html', {'order_form': order_form})
