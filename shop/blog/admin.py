from django.contrib import admin
from . models import Category, Product, Model
from django.utils.safestring import mark_safe
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_photo')
    list_display_links = ('name',)

    def get_photo(self, category):

        if category.photo:
            return mark_safe(f'<img src="{category.photo.url}" width="80px;">')

    get_photo.short_description = 'Rasmi'

    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'color', 'category', 'get_photo')
    list_display_links = ('name', )

    def get_photo(self, product):
        if product.photo:
            return mark_safe(f'<img src="{product.photo.url}" width="80px;">')

    get_photo.short_description ='Rasmi'

    prepopulated_fields = {'slug': ('name',)}


@admin.register(Model)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_photo')
    list_display_links = ('name', )

    def get_photo(self, model):
        if model.photo:
            return mark_safe(f'<img src="{model.photo.url}" width="80px;">')

    get_photo.short_description ='Rasmi'
