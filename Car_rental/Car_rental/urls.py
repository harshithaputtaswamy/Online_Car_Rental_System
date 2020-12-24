"""Car_rental URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from webapp.views import *
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import logout
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^oauth/', include('social_django.urls', namespace='social')),
    url('^', include('django.contrib.auth.urls')),
    path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL},name='logout'),
    url(r'^$',home,name = 'home'),
    url(r'^car_list/$',car_list,name = 'car_list'),
    url(r'^car_detail/(?P<id>\d+)/$',car_detail,name = 'car_detail'),
    url(r'^book_car/$', book_car, name = 'book_car'),
    url(r'^add_address_form/$', add_address_form, name = 'add_address_form'),
    url(r'^add_address/$',add_address, name = 'add_address'),
    url(r'^booking_details/$',booking_details, name = 'booking_details'),
    url(r'^billings/$', billings, name = 'billings'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
