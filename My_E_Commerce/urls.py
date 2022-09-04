from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from My_E_Commerce import settings
from all_brands_shop.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('all_brands_shop.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
