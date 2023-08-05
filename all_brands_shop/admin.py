from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'mobile_number', 'date_joined', 'is_superuser')
    list_display_links = ('username', )
    list_editable = ('is_superuser', )
    search_fields = ('username', )
    prepopulated_fields = {'slug': ('username',)}

    # def get_username(self, obj):
    #     return obj.username
    #
    # def get_email(self, obj):
    #     return obj.email
    #
    # get_username.admin_order_field = 'username'  # Allows column order sorting
    # get_username.short_description = 'Имя пользователя'  # Renames column head
    # get_email.admin_order_field = 'email'
    # get_email.short_description = 'Email'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_published')
    list_display_links = ('name', )
    search_fields = ('name',)
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    # prepopulated_fields = {'slug': ('name',)}


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_published')
    list_display_links = ('name', )
    search_fields = ('name',)
    list_editable = ('is_published',)
    list_filter = ('is_published',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_published', 'price', 'cover', 'time_update', 'category', 'brand', 'gender')
    list_display_links = ('name', )
    search_fields = ('name', 'price')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_update')
    prepopulated_fields = {'slug': ('name',)}


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo', 'time_create', 'product')
    list_display_links = ('photo', )
    search_fields = ('product',)
    list_filter = ('time_create', )


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'size', 'count', 'product')
    list_display_links = ('size', )
    search_fields = ('size', 'product')
    list_filter = ('size', )


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'date_added')
    list_display_links = ('customer',)
    search_fields = ('customer', 'product')
    list_filter = ('date_added',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_ordered', 'complete', 'transaction_id')
    search_fields = ('customer', 'transaction_id')
    list_filter = ('complete', 'date_ordered')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order', 'quantity', 'date_added')
    search_fields = ('product', )
    list_filter = ('date_added',)


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'address', 'zipcode', 'date_added')
    list_display_links = ('customer', )
    search_fields = ('customer', 'zipcode')


class SlideAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'photo', 'is_published')
    list_display_links = ('name', )
    search_fields = ('name', )
    list_editable = ('is_published', )
    list_filter = ('is_published', )


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Slide, SlideAdmin)
