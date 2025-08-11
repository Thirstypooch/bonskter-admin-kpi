from django.contrib import admin
from .models import Restaurant, MenuItem
# Register your models here.

class MenuItemInline(admin.TabularInline):
    """Allows editing MenuItems directly within the Restaurant admin page."""
    model = MenuItem
    extra = 1  # Number of empty forms to display
    fields = ('name', 'description', 'price_cents', 'category', 'image_url')

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    """Customizes the display for the Restaurant model in the admin."""
    list_display = ('name', 'rating', 'delivery_time_minutes', 'delivery_fee_cents')
    search_fields = ('name',)
    inlines = [MenuItemInline]

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Customizes the display for the MenuItem model."""
    list_display = ('name', 'restaurant', 'price_cents', 'category')
    list_filter = ('restaurant', 'category')
    search_fields = ('name', 'restaurant__name')