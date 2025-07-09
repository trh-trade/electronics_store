from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')  # Что показывать в списке
    search_fields = ('name',)  # Поиск по названию
    list_filter = ('parent',)  # Фильтр по родительским категориям

# Регистрируем модели
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)  # Если ещё не зарегистрирована