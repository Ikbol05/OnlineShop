from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Kategoriyalar')
    photo = models.ImageField(upload_to='category/', null=True, blank=True, verbose_name='Rasmi')
    slug = models.SlugField(null=True, blank=True, verbose_name='Slug')


    def __str__(self):
        return self.name

    class Meta():
        ordering = ['-pk']



FILTER_SIZE = {
    'all': 'All Size',
    'xs': 'XS',
    's': 'S',
    'm': 'M',
    'l': 'L',
    'xl': 'XL'
}



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Kategoriya')
    name = models.CharField(max_length=255, verbose_name="Nomi")
    content = models.TextField(blank=True, null=True, verbose_name='Izohi')
    photo = models.ImageField(upload_to='product/', verbose_name='Rasmi')
    price = models.FloatField(verbose_name='Narxi')
    discount = models.FloatField(verbose_name='Chegirma')
    color = models.CharField(max_length=150, null=True, blank=True, verbose_name='Rangi')
    quantity = models.IntegerField(default=0)
    filter_size = models.CharField(max_length=3, choices=FILTER_SIZE, null=True)
    slug = models.SlugField(null=True, blank=True, verbose_name='Slug')

    def __str__(self):
        return self.name

    class Meta():
        ordering = ['-pk']


class Model(models.Model):
    name = models.CharField(max_length=150, verbose_name='Madel')
    photo = models.ImageField(upload_to='model/', verbose_name='Rasmi')

    class Meta():
        ordering = ['-pk']



class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name}: {self.rating}"


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50, null=True, default='')
    last_name = models.CharField(max_length=50, null=True, default='')


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_cart_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity




class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)

    @property
    def get_cart_price(self):
        total_price = self.quantity * self.product.price
        return total_price




class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)


class Comment(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text