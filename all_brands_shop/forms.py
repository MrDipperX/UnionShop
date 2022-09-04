from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import Customer, Order, ShippingAddress


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'username', 'email', 'mobile_number', 'password')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Customer
        fields = ('username', 'email', 'mobile_number', 'password')


class RegisterUserForm(CustomUserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Ваша фамилия'}))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя пользователя'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ваша электронная почта'}))
    mobile_number = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повтор пароля'}))

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'username', 'email', 'mobile_number', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Ваше имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'zipcode']
        widgets = {
            'address': forms.Textarea(attrs={'placeholder': 'Адрес', 'cols': 60, 'rows': 5}),
            'zipcode': forms.NumberInput(attrs={'placeholder': 'Почтовый индекс', 'pattern': '[0-9]{6}'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['comment', ]
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Комментарий', 'cols': 60, 'rows': 5}),

        }


class SearchForm(forms.Form):
    search_input = forms.CharField(max_length=150,
                                   widget=forms.TextInput(attrs={'placeholder': 'Название товара'}))