from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
# admin.site.register(Size)
admin.site.register(Brand)
# admin.site.register(Color)
admin.site.register(Product)

admin.site.register(Gender)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    # inlines = [ProductGalleryInline]

# class VariationAdmin(admin.ModelAdmin):
#     list_display = ('product', 'variation_category', 'variation_value', 'is_active')
#     list_editable = ('is_active',)
#     list_filter = ('product', 'variation_category', 'variation_value')
# class CategoryAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('category_name',)}
#     list_display = ('category_name', 'slug')

# admin.site.register(Category, CategoryAdmin)

# admin.site.register(Product, ProductAdmin)
# admin.site.register(Variation, VariationAdmin)
# admin.site.register(Brand)


# class VariantsAdmin(admin.ModelAdmin):
#     list_display = ['product','colors','sizes','quantinty']

# # admin.site.register(ProductAttribute,VariantsAdmin)


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

# admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
