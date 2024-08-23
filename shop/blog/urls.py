from django.urls import path
from . views import (Index, Products, category_product, DetailProduct, rate, user_login, user_logout, user_register,
                     create_comment, view_comment, cart, to_cart, clear_cart, create_checkout_sessions, success_payment,
                     )

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('shop/', Products.as_view(), name='shop'),
    path('cat-pr/<int:pk>/', category_product, name='cat-pr'),
    path('detail/<int:pk>/', DetailProduct.as_view(), name='detail'),
    path('rate/<int:product_id>/<int:rating>/', rate),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('add-comment/<int:pk>/', create_comment, name='comment'),
    path('comment/<int:pk>/', view_comment, name='view_comment'),
    path('cart/', cart, name='cart'),
    path('to-cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('payment/', create_checkout_sessions, name='payment'),
    path('success/', success_payment, name='success'),
]