from django.contrib import admin
from .models import *
from admin_views.admin import AdminViews

# Register your models here.
admin.site.register(customer)

class carAdmin(admin.ModelAdmin):
    list_display = ("name", "availability")
    
admin.site.register(car, carAdmin)
admin.site.register(category)
admin.site.register(address)
admin.site.register(booking)
admin.site.register(billing)