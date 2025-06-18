from django.contrib import admin

from apps.shop.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass