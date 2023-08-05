# Generated by Django 4.0.6 on 2022-08-13 06:49

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('mobile_number', models.CharField(max_length=10, verbose_name='Номер телефона')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, verbose_name='Название')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, verbose_name='Название')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
            ],
            options={
                'verbose_name': 'Категорию',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(auto_now_add=True, verbose_name='Товар')),
                ('complete', models.BooleanField(default=False, verbose_name='Закончено')),
                ('transaction_id', models.CharField(max_length=100, null=True, verbose_name='Номер транзакции')),
                ('comment', models.TextField(blank=True, verbose_name='Комментрий')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['date_ordered'],
            },
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название')),
                ('slogan', models.TextField(blank=True, verbose_name='Слоган')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('photo', models.ImageField(upload_to='files/%Y/%m/%d', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Слайд',
                'verbose_name_plural': 'Слайды',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='all_brands_shop.order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('sale', models.PositiveSmallIntegerField(default=100, verbose_name='Скидка')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='url')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения')),
                ('cover', models.ImageField(upload_to='files/%Y/%m/%d', verbose_name='Обложка')),
                ('sex', models.CharField(choices=[('м', 'Мужские'), ('ж', 'Женские'), ('у', 'Унисекс'), ('д', 'Детские')], default='Мужские', max_length=30, verbose_name='Пол')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='all_brands_shop.brand', verbose_name='Бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='all_brands_shop.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['time_create', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='files/%Y/%m/%d', verbose_name='Фото')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='all_brands_shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Фото',
                'verbose_name_plural': 'Фотки',
                'ordering': ['time_create'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True, verbose_name='Количество')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='all_brands_shop.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='all_brands_shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Еденица заказа',
                'verbose_name_plural': 'Еденицы заказа',
                'ordering': ['date_added'],
            },
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'Extra Extra Large')], max_length=40, verbose_name='Размер')),
                ('count', models.IntegerField(verbose_name='Остаток')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='all_brands_shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Остатка',
                'verbose_name_plural': 'Остатки',
                'ordering': ['product'],
            },
        ),
    ]
