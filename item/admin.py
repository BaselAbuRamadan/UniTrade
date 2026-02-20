from django.contrib import admin
from .models import Category, Item


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "status", "seller", "created_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "description")
    autocomplete_fields = ("category", "seller")
    ordering = ("-created_at",)