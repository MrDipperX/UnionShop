import json
from .models import *


class DataMixin:
    def get_user_context(self, request, **kwargs):
        data = cart_data(request)

        context = kwargs

        context['cart_items'] = data['cart_items']
        context['order'] = data['order']
        context['items'] = data['items']

        return context


def cookie_cart(request):
    # Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}


    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cart_items = order['get_cart_items']


    for i in cart:
        # We use try block to prevent items in cart that may have been removed from causing error
        try:
            if cart[i]['quantity'] > 0:  # items with negative quantity = lot of freebies
                cart_items += cart[i]['quantity']
                product_id = i.split('-')[0]

                product = Product.objects.get(id=product_id)
                total = (product.sale_price * cart[i]['quantity'])
                sale_price = product.sale_price

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'id': product.id,
                    'product': {'id': product.id, 'name': product.name, 'price': product.price,
                                'sale_price': sale_price, 'image_url': product.image_url},
                    'quantity': cart[i]['quantity'], 'get_total': total, 'size': cart[i]['size'],
                }
                items.append(item)

        except:
            pass

    return {'cart_items': cart_items, 'order': order, 'items': items}


def cart_data(request):
    cookie_data = cookie_cart(request)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        if cookie_data['items']:
            items = cookie_data['items']
            for item in items:
                product = Product.objects.get(id=item['id'])
                order_item, created = OrderItem.objects.get_or_create(
                    product=product,
                    order=order,
                    size=item['size']
                )

                if order_item.quantity == 0:
                    order_item.quantity = order_item.quantity + item['quantity']
                order_item.save()

        items = order.orderitem_set.all()
        cart_items = order.get_cart_items

    else:
        cart_items = cookie_data['cart_items']
        order = cookie_data['order']
        items = cookie_data['items']

    return {'cart_items': cart_items, 'order': order, 'items': items}


# def guest_order(request, customer):
#     cookie_data = cookie_cart(request)
#     items = cookie_data['items']
#
#     order = Order.objects.create(
#         customer=customer,
#         complete=False,
#     )
#
#     for item in items:
#         product = Product.objects.get(id=item['id'])
#         orderItem = OrderItem.objects.create(
#             product=product,
#             order=order,
#             quantity=(item['quantity'] if item['quantity'] > 0 else -1 * item['quantity']),
#             # negative quantity = freebies
#         )
#     return order

