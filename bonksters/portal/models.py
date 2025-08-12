# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator
import uuid

class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    cover_image_url = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    delivery_time_minutes = models.IntegerField(blank=True, null=True)
    delivery_fee_cents = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'restaurants'
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

class MenuItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price_cents = models.IntegerField(validators=[MinValueValidator(0)])
    image_url = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

    class Meta:
        managed = False
        db_table = 'menu_items'
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'