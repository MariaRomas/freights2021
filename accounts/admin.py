from django.contrib import admin
from .models import User, Customer, Driver

admin.site.register(User)
#admin.site.register(Customer)
admin.site.register(Driver)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Грузовладелец"""
    list_display = ("user", )

