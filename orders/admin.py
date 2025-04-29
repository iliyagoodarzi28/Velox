from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('shoe',)
    fields = ('shoe', 'quantity', 'price', 'total_price')
    readonly_fields = ('total_price',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(order__user=request.user)

    def total_price(self, obj):
        # Safely compute total price, avoid NoneType * int errors
        if obj.price is None or obj.quantity is None:
            return 0
        return obj.get_total()
    total_price.short_description = 'Total Price'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'updated_at', 'status', 'total_amount')
    list_filter = ('status',)
    search_fields = ('user__username', 'email', 'address')
    inlines = (OrderItemInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        # Automatically assign the owner on creation
        if not change:
            obj.user = request.user
        # Ensure total_amount is never None
        obj.total_amount = obj.total_amount or 0
        super().save_model(request, obj, form, change)
