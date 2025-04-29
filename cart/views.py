from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect
from product.models import Shoe
from .cart import Cart  # Adjust the import based on your project structure
from django.contrib import messages
from django.contrib.messages import get_messages

class CartDetailView(TemplateView):
    """
    Displays the current cart with all of its items.
    """
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context["cart"] = cart
        # Optionally, if you need a total number of items, total price, or total discount in the template:
        context["cart_total_items"] = len(cart)
        context["cart_total_price"] = cart.get_total_price()
        context["cart_total_discount"] = sum(item['shoe'].discount_amount * item['quantity'] for item in cart)
        

        
        return context


class CartAddView(View):
    def post(self, request, shoe_id):
        cart = Cart(request)
        shoe = get_object_or_404(Shoe, id=shoe_id)
        quantity = int(request.POST.get('quantity', 1))

        if shoe.inventory >= quantity:
            shoe.reduce_stock(quantity)  # Reduce inventory
            cart.add(shoe=shoe, quantity=quantity, update_quantity=True)
            messages.success(request, "Item added to cart successfully.")
        else:
            messages.error(request, "Not enough stock available!")
        
        # Use toaster to display messages
        storage = get_messages(request)
        for message in storage:
            # Assuming you have a function to handle toaster notifications
            self.toaster_notification(request, message)
        
        return redirect("cart:cart_detail")

    def toaster_notification(self, request, message):
        # Implement your toaster notification logic here
        pass


class CartRemoveView(View):
    """
    Removes a Shoe from the cart.
    Expects a POST request.
    """
    def post(self, request, shoe_id):
        cart = Cart(request)
        shoe = get_object_or_404(Shoe, id=shoe_id)
        cart.remove(shoe)
        messages.success(request, "Item removed from cart successfully.")
        
        # Use toaster to display messages
        storage = get_messages(request)
        for message in storage:
            self.toaster_notification(request, message)
        
        return redirect("cart:cart_detail")

    def toaster_notification(self, request, message):
        # Implement your toaster notification logic here
        pass


class CartUpdateView(View):
    def post(self, request, shoe_id):
        cart = Cart(request)
        shoe = get_object_or_404(Shoe, id=shoe_id)
        new_quantity = int(request.POST.get('quantity', 1))
        
        # Retrieve the current quantity of the shoe in the cart
        current_quantity = cart.cart.get(str(shoe_id), {}).get('quantity', 0)
        
        # Calculate the difference in quantity
        quantity_difference = new_quantity - current_quantity
        
        # Check if the new quantity is feasible with the current inventory
        if shoe.inventory >= quantity_difference:
            # Update the inventory based on the quantity difference
            shoe.reduce_stock(quantity_difference)
            # Update the cart with the new quantity
            cart.add(shoe=shoe, quantity=new_quantity, update_quantity=True)
            messages.success(request, "Cart updated successfully.")
        else:
            messages.error(request, "Not enough stock available to update the cart!")
        
        # Use toaster to display messages
        storage = get_messages(request)
        for message in storage:
            self.toaster_notification(request, message)
        
        return redirect("cart:cart_detail")

    def toaster_notification(self, request, message):
        # Implement your toaster notification logic here
        pass
