import json
from datetime import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, JsonResponse, Http404
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView, CreateView, DetailView, UpdateView

from .forms import RegisterUserForm, LoginUserForm, ShippingAddressForm, CommentForm, SearchForm
from .models import *
from .utlls import DataMixin


class ShopHome(DataMixin, ListView):
    model = Product
    template_name = 'all_brands_shop/index.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница', request=self.request)

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Product.objects.all().filter(is_published=True)


class ShopShop(DataMixin, ListView):
    model = Product
    template_name = 'all_brands_shop/shop.html'
    context_object_name = 'products'
    paginate_by = 16
    form = SearchForm

    def get_context_data(self, *, object_list=None, **kwargs):
        val_dict = dict()
        if self.request.GET.get("search_input"):
            val_dict['search_input'] = self.request.GET['search_input']
        elif self.request.GET.get("category"):
            val_dict['category'] = self.request.GET['category']
        elif self.request.GET.get("size"):
            val_dict['size'] = self.request.GET['size']
        elif self.request.GET.get("brand"):
            val_dict['brand'] = self.request.GET['brand']
        elif self.request.GET.get("gender"):
            val_dict['gender'] = self.request.GET['gender']
        elif self.request.GET.get("price1"):
            val_dict['price1'] = self.request.GET['price1']
            val_dict['price2'] = self.request.GET['price2']

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Товары', request=self.request, search_form=self.form, val_dict=val_dict)

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        search_form = self.form(self.request.GET)
        queryset = Product.objects.filter(is_published=True)
        if search_form.is_valid() and self.request.GET.get("search_input"):
            queryset = Product.objects.filter(is_published=True).filter(name__contains=self.request.GET['search_input'])
        elif self.request.GET.get("category"):
            queryset = \
                Product.objects.filter(is_published=True).filter(category__name__contains=self.request.GET['category'])
        elif self.request.GET.get("brand"):
            queryset = Product.objects.filter(is_published=True).filter(brand__name__contains=self.request.GET['brand'])
        elif self.request.GET.get("price1") and self.request.GET.get("price2"):
            queryset = Product.objects.filter(is_published=True).filter(price__range=(self.request.GET['price1'],
                                                                                      self.request.GET["price2"]))
        elif self.request.GET.get("size"):
            queryset = Product.objects.filter(is_published=True).filter(balance__size=self.request.GET['size'])
        elif self.request.GET.get("gender"):
            queryset = Product.objects.filter(is_published=True).filter(gender=self.request.GET['gender'])

        return queryset


class ShopDetail(DataMixin, DetailView):
    model = Product
    template_name = 'all_brands_shop/shop-details.html'
    context_object_name = 'some_product'
    slug_url_kwarg = 'product_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Детали товара', request=self.request)
        return dict(list(context.items()) + list(c_def.items()))


class ShopAbout(DataMixin, TemplateView):
    template_name = 'all_brands_shop/about-us.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О нас', request=self.request)

        return dict(list(context.items()) + list(c_def.items()))


class ShopUserProfile(DataMixin, DetailView, UpdateView):
    model = Customer
    template_name = 'all_brands_shop/profile.html'
    context_object_name = 'customer'
    slug_url_kwarg = 'user_slug'
    fields = ['first_name', 'last_name', 'username', 'email', 'mobile_number']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Профиль {self.get_object().username}', request=self.request)
        print(self.kwargs)

        if not self.request.user.is_authenticated or self.request.user.slug != self.kwargs['user_slug']:
            raise Http404()

        return dict(list(context.items()) + list(c_def.items()))


class ShopLogin(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'all_brands_shop/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Вход', request=self.request)

        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class ShopReg(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'all_brands_shop/registration.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация', request=self.request)

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class ShopCart(DataMixin, TemplateView):
    template_name = 'all_brands_shop/cart.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Корзина', request=self.request)

        return dict(list(context.items()) + list(c_def.items()))


class ShopFavorites(DataMixin, TemplateView):
    template_name = 'all_brands_shop/favorites.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Избранное', request=self.request)

        if not self.request.user.is_authenticated:
            raise Http404()

        return dict(list(context.items()) + list(c_def.items()))


class ShopCheckout(DataMixin, TemplateView):
    shipping_address_form = ShippingAddressForm
    comment_form = CommentForm
    guest_register_form = RegisterUserForm
    template_name = 'all_brands_shop/checkout.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        c_def = self.get_user_context(title='Счёт', request=self.request)
        if c_def['cart_items'] == 0:
            return redirect('shop')
        if not request.user.is_authenticated:
            return redirect('login')
        return self.post(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Счёт', request=self.request)

        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        post_data = request.POST or None
        guest_form = self.guest_register_form(post_data, prefix='guest_reg')

        if request.user.is_authenticated:
            order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        else:
            return redirect('login')
            # if guest_form.is_valid():
            #     user = guest_form.save()
            #     login(self.request, user)
            # order = guest_order(request, request.user)

        customer = request.user
        shipping_address, created_a = ShippingAddress.objects.get_or_create(customer=customer, order=order)
        address_form = self.shipping_address_form(post_data, prefix='address', instance=shipping_address)
        comment_form = self.comment_form(post_data, prefix='comment', instance=order)

        context = self.get_context_data(address_form=address_form,
                                        comment_form=comment_form,
                                        guest_form=guest_form)

        if address_form.is_valid() and comment_form.is_valid():
            address = address_form.save(commit=False)
            address.customer = customer
            address.order = order
            address.save()

            comment_form.save()

            process_order(request, order)

            return redirect('shop')

        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        response = super(ShopCheckout, self).render_to_response(context, **response_kwargs)
        response.set_cookie('cart', {})
        return response


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    size = data['size']

    customer = request.user
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product, size=size)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
        order_item.save()
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)
        order_item.save()
    elif action == 'delete':
        order_item.delete()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)


def update_favorites(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    customer = request.user
    product = Product.objects.get(id=product_id)

    favorite_item, created = Favorites.objects.get_or_create(customer=customer, product=product)

    if action == 'delete':
        favorite_item.delete()

    return JsonResponse('Item was added', safe=False)


def process_order(request, order):
    transaction_id = datetime.now().timestamp()

    total = request.POST['total'].replace(',', '.')

    order.transaction_id = transaction_id

    if float(total) == float(order.get_cart_total) and order.is_avialable_product:
        order.complete = True
        items = order.orderitem_set.all()

        for item in items:
            balance = Balance.objects.get(size=item.size)
            balance.count = item.product.balance_set.get(size=item.size).count - item.quantity
            balance.save()
    order.save()


def logout_user(request):
    logout(request)
    return redirect('home')


def page_not_found(request, exception):
    return HttpResponseNotFound(f"Страница не найдена!")
