from django import template
from django.db.models import Count
from all_brands_shop.models import *

register = template.Library()


@register.simple_tag()
def get_slides():
    return Slide.objects.filter(is_published=True)


@register.simple_tag()
def hottest_products():
    return Product.objects.filter(is_published=True).annotate(Count('orderitem'))[:4]


@register.simple_tag()
def latest_products():
    hottest_products_id = [hottest.pk for hottest in hottest_products()]
    latest = Product.objects.filter(is_published=True).order_by('time_update')
    return latest.exclude(id__in=hottest_products_id)[:4]


@register.simple_tag()
def get_all_categories():
    return Category.objects.filter(is_published=True)


@register.simple_tag()
def get_all_brands():
    return Brand.objects.filter(is_published=True)


@register.simple_tag()
def get_all_genders():
    genders = (gender for gender in Product.GENDERS)
    return genders


@register.simple_tag()
def get_count_of_products_from_category(category_name=None):
    return Product.objects.filter(category__name=category_name).count()


@register.simple_tag()
def get_count_of_products_from_brand(brand_name=None):
    return Product.objects.filter(brand__name=brand_name).count()


@register.simple_tag()
def get_all_sizes():
    short_sizes = (size[0] for size in Balance.SIZES)
    return short_sizes


@register.simple_tag()
def get_lowest_price():
    products = Product.objects.all()
    prices = [product.sale_price for product in products]

    return int(min(prices))


@register.simple_tag()
def get_one_third_price():
    products = Product.objects.all()
    prices = [product.sale_price for product in products]
    one_third = ((max(prices)*1/3)//1000)*1000

    return int(one_third)


@register.simple_tag()
def get_two_thirds_price():
    products = Product.objects.all()
    prices = [product.sale_price for product in products]
    two_thirds = ((max(prices)*2/3)//1000)*1000

    return int(two_thirds)


@register.simple_tag()
def get_highest_price():
    products = Product.objects.all()
    prices = [product.sale_price for product in products]

    return int(max(prices))




