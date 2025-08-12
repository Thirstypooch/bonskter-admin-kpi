from django.contrib import admin
from django.utils.html import mark_safe
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
    list_display = ('name', 'image_preview', 'rating', 'delivery_time_minutes', 'formatted_delivery_fee', 'is_featured')
    list_filter = ('is_featured',)
    search_fields = ('name',)
    inlines = [MenuItemInline]
    actions = ['make_featured', 'make_unfeatured']

    fieldsets = (
        ('Restaurant Information', {
            'fields': ('name', 'cover_image_url', 'rating', 'is_featured')
        }),
        ('Delivery Details', {
            'fields': ('delivery_time_minutes', 'delivery_fee_cents')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # This makes the section collapsible
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    @admin.action(description="Mark selected restaurants as featured")
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description="Mark selected restaurants as not featured")
    def make_unfeatured(self, request, queryset):
        queryset.update(is_featured=False)

    @admin.display(description='Image')
    def image_preview(self, obj):
        if obj.cover_image_url:
            url = str(obj.cover_image_url)
            if url.startswith('http'):
                return mark_safe(f'<img src="{url}" width="100" height="50" style="object-fit: cover;" />')
            else:
                return mark_safe(
                    f'<img src="{obj.cover_image_url.url}" width="100" height="50" style="object-fit: cover;" />')
        return "No Image"

    @admin.display(description='Delivery Fee', ordering='delivery_fee_cents')
    def formatted_delivery_fee(self, obj):
        """Formats the delivery fee from cents to a PEN string or shows 'Free'."""
        if obj.delivery_fee_cents is None or obj.delivery_fee_cents == 0:
            return "Free"
        return f"S/ {obj.delivery_fee_cents / 100:.2f}"

    def get_queryset(self, request):
        """
        This is the core of our security model. It filters the restaurants
        so that non-superusers can only see their own.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Customizes the display for the MenuItem model."""
    list_display = ('name', 'restaurant_link', 'formatted_price', 'category', 'image_preview')
    list_filter = ('restaurant', 'category')
    raw_id_fields = ('restaurant' ,)
    search_fields = ('name', 'restaurant__name')

    @admin.display(description='Restaurant')
    def restaurant_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html

        link = reverse("admin:portal_restaurant_change", args=[obj.restaurant.id])
        return format_html('<a href="{}">{}</a>', link, obj.restaurant.name)

    @admin.display(description='Image')
    def image_preview(self, obj):
        if obj.image_url:
            url = str(obj.image_url)
            if url.startswith('http'):
                return mark_safe(f'<img src="{url}" width="60" height="60" style="object-fit: cover; border-radius: 4px;" />')
            else:
                return mark_safe(f'<img src="{obj.image_url.url}" width="60" height="60" style="object-fit: cover; border-radius: 4px;" />')
        return "No Image"

    @admin.display(description='Price', ordering='price_cents')
    def formatted_price(self, obj):
        """Formats the price from cents to a dollar string."""
        return f"S/ {obj.price_cents / 100:.2f}"