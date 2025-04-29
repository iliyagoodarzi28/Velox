from django.contrib import admin
from .models import Category, Shoe, Size, Color

class ShoeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'discount_available', 'discount_amount')
    search_fields = ('name',)
    list_filter = ('categories', 'discount_available')

admin.site.register(Category)
admin.site.register(Shoe, ShoeAdmin)
admin.site.register(Size)
admin.site.register(Color)
