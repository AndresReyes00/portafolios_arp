
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('my_apps.landing.urls')),
    path('accounts/', include('my_apps.accounts.urls'))
]
