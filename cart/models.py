from django.db import models
from django.conf import settings
from product.models import Shoe  # Reference to the Shoe model from the product app

class Cart(models.Model):
    """
    Cart model: If the user is logged in, the 'user' field is used.
    Otherwise, 'session_key' can be utilized to identify the cart.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="User"
    )
    session_key = models.CharField(max_length=255, null=True, blank=True, verbose_name="Session Key")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    def __str__(self):
        return f"Cart {self.pk}"

    @property
    def total_price(self):
        """
        Calculate the total price of the cart, considering any discounts available on products.
        """
        return sum(item.total_price for item in self.items.all())

    def add_item(self, shoe, quantity=1):
        """
        Add a product (Shoe) to the cart while checking for its existence.
        If the product exists, its quantity is updated.
        """
        item, created = CartItem.objects.get_or_create(cart=self, shoe=shoe)
        if not created:
            item.quantity += quantity
            item.save()
        else:
            item.quantity = quantity
            item.save()

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ['-created_at']

class CartItem(models.Model):
    """
    Cart Item model: Each item includes a reference to a product (Shoe) and its quantity.
    """
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items', 
        verbose_name="Cart"
    )
    shoe = models.ForeignKey(
        Shoe, 
        on_delete=models.CASCADE, 
        verbose_name="Shoe"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")

    class Meta:
        unique_together = ('cart', 'shoe')
        ordering = ['shoe']
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return f"{self.quantity} of {self.shoe.name}"

    @property
    def total_price(self):
        """
        Calculate the total price for this item, accounting for any available discount.
        """
        price = self.shoe.price
        if self.shoe.discount_available and self.shoe.discount_percentage > 0:
            discount = price * (self.shoe.discount_percentage / 100)
            price = price - discount
        return price * self.quantity
