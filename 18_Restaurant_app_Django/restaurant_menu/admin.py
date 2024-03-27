from django.contrib import admin
from .models import Item

# Register your models here.

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("meal", "status", "pk")
    list_filter = ("status",)
    search_fields = ("meal", "description")
    

admin.site.register(Item, MenuItemAdmin)
