from decimal import Decimal
from django.conf import settings
from product.models import Shoe

class Cart:
    """
    A session-based shopping cart.
    This class provides functionality to add, remove, update items, and calculate
    the total price of the cart.
    """
    def __init__(self, request):
        """
        Initialize the cart based on the user's request.
        If no cart exists in the session, create an empty dictionary.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, shoe, quantity=1, update_quantity=False):
        """
        Add a product (Shoe) to the cart, or update its quantity.
        Handles price and discount calculations properly.
        """
        shoe_id = str(shoe.id)
        
        # Calculate effective price and discount
        price = str(shoe.price)
        discount_amount = str(shoe.discount_amount) if shoe.discount_available else '0'

        if shoe_id not in self.cart:
            self.cart[shoe_id] = {
                'quantity': 0,
                'price': price,
                'discount_amount': discount_amount
            }
        else:
            # Update price and discount in case they changed
            self.cart[shoe_id]['price'] = price
            self.cart[shoe_id]['discount_amount'] = discount_amount
        
        if update_quantity:
            self.cart[shoe_id]['quantity'] = quantity
        else:
            self.cart[shoe_id]['quantity'] += quantity
        
        self.save()

    def save(self):
        """
        Mark the session as modified so that it gets saved.
        """
        self.session.modified = True

    def remove(self, shoe):
        """
        Remove a product from the cart.
        """
        shoe_id = str(shoe.id)
        if shoe_id in self.cart:
            del self.cart[shoe_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and calculate prices correctly.
        """
        shoe_ids = self.cart.keys()
        shoes = Shoe.objects.filter(id__in=shoe_ids)
        cart_copy = self.cart.copy()
        
        for shoe in shoes:
            cart_copy[str(shoe.id)]['shoe'] = shoe
            # Update price and discount in case they changed since adding to cart
            cart_copy[str(shoe.id)]['price'] = str(shoe.price)
            cart_copy[str(shoe.id)]['discount_amount'] = str(shoe.discount_amount)

        for item in cart_copy.values():
            item['price'] = Decimal(item['price'])
            item['discount_amount'] = Decimal(item['discount_amount'])
            # Calculate total price after discount
            effective_price = item['price'] - item['discount_amount']
            item['total_price'] = effective_price * item['quantity']
            yield item

    def __len__(self):
        """
        Calculate the total number of items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the total price of the cart, properly handling discounts.
        """
        total = Decimal('0')
        for item in self.cart.values():
            price = Decimal(item['price'])
            discount = Decimal(item.get('discount_amount', '0'))
            quantity = item['quantity']
            total += (price - discount) * quantity
        return total

    def clear(self):
        """
        Clear the cart by removing all items from the session.
        """
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()


         
