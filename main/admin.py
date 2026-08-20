from django.contrib import admin
from .models import Category, Attribute, Product, ProductAttributeValue

class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1
    raw_id_fields = ('attribute',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'is_filterable')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('categories',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rating')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductAttributeValueInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'price', 'rating', 'image', 'category')
        }),
        ('Кеш атрибутов (только для чтения)', {
            'fields': ('attributes_cache',),
            'classes': ('collapse',),
        }),
    )

@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'get_value_display')
    list_filter = ('attribute',)
    search_fields = ('product__name', 'value_text')