from django.db import models
from django.urls import reverse_lazy
from pytils.translit import slugify
from django.contrib.auth.models import User, AbstractUser


class Customer(AbstractUser):
    mobile_number = models.CharField(max_length=10, verbose_name='Номер телефона')
    slug = models.SlugField(max_length=250, db_index=True, unique=True, verbose_name="url", null=True,)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ['date_joined']

    def get_absolute_url(self):
        return reverse_lazy('profile', kwargs={'user_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)  # Call the "real" save() method.

    @property
    def customer_favorites(self):
        return self.favorites_set.all()

    @property
    def customer_orders(self):
        return self.order_set.filter(complete=True)

    @property
    def customer_shipping_addresses(self):
        return self.shippingaddress_set.all()


class Category(models.Model):
    name = models.CharField(max_length=250, blank=True, verbose_name='Название')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Brand(models.Model):
    name = models.CharField(max_length=250, blank=True, verbose_name='Название')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']


class Product(models.Model):
    GENDERS = [
        ('м', 'Мужские'),
        ('ж', 'Женские'),
        ('у', 'Унисекс')
    ]

    name = models.CharField(max_length=250, blank=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    sale = models.PositiveSmallIntegerField(default=100, verbose_name='Скидка')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    slug = models.SlugField(max_length=250, db_index=True, unique=True, verbose_name="url")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения')
    cover = models.ImageField(upload_to="files/%Y/%m/%d", verbose_name='Обложка')
    gender = models.CharField(choices=GENDERS, verbose_name='Пол', max_length=30, default='Мужские')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-time_create', ]

    def get_absolute_url(self):
        return reverse_lazy('shop_detail', kwargs={'product_slug': self.slug})

    @property
    def image_url(self):
        try:
            url = self.cover.url
        except:
            url = ''
        return url

    @property
    def sale_price(self):
        if self.sale == 100:
            sale_price = self.price
        else:
            sale_price = self.price * ((100-self.sale)/100)
        return sale_price

    @property
    def photos(self):
        return self.photo_set.all()

    @property
    def get_sizes_by_product(self):
        return self.balance_set.all().values('size')


class Photo(models.Model):
    photo = models.ImageField(upload_to="files/%Y/%m/%d", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self):
        return self.photo.url

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотки'
        ordering = ['time_create']

    @property
    def image_url(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url


class Balance(models.Model):
    SIZES = [
        ('xs', 'xs'),
        ('s', 's'),
        ('m', 'm'),
        ('l', 'l'),
        ('xl', 'xl'),
        ('xxl', 'xxl')
    ]

    size = models.CharField(choices=SIZES, verbose_name='Размер', max_length=40)
    count = models.IntegerField(verbose_name='Остаток')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self):
        return str(self.count)

    class Meta:
        verbose_name = 'Остатка'
        verbose_name_plural = 'Остатки'
        ordering = ['product']


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Покупатель')
    date_ordered = models.DateTimeField(auto_now=True, verbose_name='Время заказа')
    complete = models.BooleanField(default=False, verbose_name='Закончено')
    transaction_id = models.CharField(max_length=100, null=True, verbose_name='Номер транзакции')
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['date_ordered']

    @property
    def is_avialable_product(self):
        orderitems = self.orderitem_set.all()
        is_avialable = all(item.product.balance_set.get(size=item.size).count >= item.quantity for item in orderitems)
        return is_avialable

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_order_items(self):
        return self.orderitem_set.all()


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Товар')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Количество')
    size = models.CharField(max_length=3, null=True, verbose_name='Размер')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    @property
    def get_total(self):
        total = self.product.sale_price * self.quantity
        return total

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Еденица заказа'
        verbose_name_plural = 'Еденицы заказа'
        ordering = ['date_added']


class Favorites(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Покупатель')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Товар')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return str(self.customer) + str(self.product)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        ordering = ['customer']


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    address = models.TextField(null=False, verbose_name='Адрес покупателя')
    zipcode = models.CharField(max_length=200, null=False, verbose_name='Почтовый индекс')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')

    def __str__(self):
        return self.address

    @property
    def comment(self):
        return self.order.comment

    @comment.setter
    def comment(self, comment):
        self.order.comment = comment

    class Meta:
        verbose_name = 'Адрес Доставки'
        verbose_name_plural = 'Адреса Доставки'
        ordering = ['date_added']


class Slide(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    slogan = models.TextField(blank=True, verbose_name='Слоган')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to="files/%Y/%m/%d", verbose_name='Фото')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'
        ordering = ['id']
