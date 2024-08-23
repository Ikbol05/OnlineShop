from django.shortcuts import render, redirect
from . models import Product, Category, Model, Rating, Comment
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpRequest, HttpResponse
from django import forms
from .utils import CartAuthenticatedUser
import stripe
from django.urls import reverse
from django.conf import settings

# Create your views here.


class Index(ListView):
    model = Product
    template_name = 'blog/index.html'
    context_object_name = 'products'
    extra_context = {
        'categorys': Category.objects.all(),
        'models': Model.objects.all(),
        'title': 'MULTI-SHOP'
    }


class Products(Index):
    template_name = 'blog/shoping.html'


def category_product(request, pk):
    context = {
        'categorys': Category.objects.all(),
        'products': Product.objects.filter(category_id=pk)
    }
    return render(request, 'blog/index.html', context)





class DetailProduct(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            product = self.get_object()
            rating = Rating.objects.filter(product=product, user=self.request.user).first()
            context['user_rating'] = rating.rating if rating else 0
        return context


def index(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    for product in products:
        rating = Rating.objects.filter(post=product, user=request.user).first()
        product.user_rating = rating.rating if rating else 0
    return render(request, "index.html", {"posts": product})


def rate(request: HttpRequest, product_id: int, rating: int) -> HttpResponse:
    product = Product.objects.get(pk=product_id)
    if request.user.is_authenticated:
        Rating.objects.filter(product=product, user=request.user).delete()
        product.rating_set.create(user=request.user, rating=rating)
    return redirect('detail', slug=product.slug)


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    return render(request, 'blog/user_login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'blog/register.html')




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


def create_comment(request, pk):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=pk)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = product
                comment.author = request.user
                comment.save()
                return redirect('detail', pk=pk)
        else:
            form = CommentForm()
        return redirect('detail', pk=pk)
    return redirect('login')


def view_comment(request, pk):
    comments = Comment.objects.all(product_id=pk)
    context = {
        'comments': comments
    }
    return render(request, 'blog/detail.html', context)



def cart(request):
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()
        context = {
            'order_products': cart_info['order_products'],
            'cart_total_price': cart_info['cart_total_price'],
            'cart_total_quantity': cart_info['cart_total_quantity']
        }
        return render(request, 'blog/cart.html', context)
    return redirect('register')

def to_cart(request: HttpRequest, product_id, action):
    if request.user.is_authenticated:
        CartAuthenticatedUser(request, product_id, action)
        current_page = request.META.get('HTTP_REFERER')
        return redirect(current_page)

    return redirect('register')


def clear_cart(request):
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()
        order = cart_info['order']
        order_products = order.orderproduct_set.all()
        for order_product in order_products:
            product = order_product.product
            product.quantity += order_product.quantity
            product.save()
            order_product.delete()
        return redirect('cart')
    else:
        return redirect('register')


def create_checkout_sessions(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user_cart = CartAuthenticatedUser(request)
    cart_info = user_cart.get_cart_info()
    total_price = cart_info['cart_total_price']
    total_quantity = cart_info['cart_total_quantity']
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Multi-Shop'
                },
                'unit_amount': int(total_price * 100)
            },
            'quantity': total_quantity
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('success')),
    )
    return redirect(session.url, 303)



def success_payment(request):
    return render(request, 'blog/success.html')