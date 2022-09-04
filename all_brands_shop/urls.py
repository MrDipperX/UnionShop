from django.urls import path
from .views import *

urlpatterns = [
    path('', ShopHome.as_view(), name="home"),
    path('shop/', ShopShop.as_view(), name="shop"),
    path('shop/<slug:product_slug>', ShopDetail.as_view(), name="shop_detail"),
    path('about-us/', ShopAbout.as_view(), name="about"),
    path('cart/', ShopCart.as_view(), name="cart"),
    path('checkout/', ShopCheckout.as_view(), name="checkout"),
    path('favorites/', ShopFavorites.as_view(), name="favorites"),
    path('profile-<slug:user_slug>', ShopUserProfile.as_view(), name="profile"),
    path('update_item/', update_item, name="update_item"),
    path('update_favorites/', update_favorites, name="update_favorites"),
    path('login/', ShopLogin.as_view(), name="login"),
    path('registration/', ShopReg.as_view(), name="registration"),
    path('logout/', logout_user, name="logout")
]
