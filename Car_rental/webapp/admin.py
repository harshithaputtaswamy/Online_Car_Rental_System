from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(customer)
admin.site.register(car)
admin.site.register(category)
admin.site.register(address)
admin.site.register(booking)
admin.site.register(billing)