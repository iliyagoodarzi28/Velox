from django.views.generic import DetailView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import Order
from .forms import OrderForm
from cart.cart import Cart

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # Ensure the queryset is ordered by creation date, most recent first
        return super().get_queryset().filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'  # Specify the URL parameter for the primary key
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.get_object().order_items.all()
        return context

class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = OrderForm()
        return render(request, 'orders/order_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            # Calculate the total amount for the order
            order.calculate_total()
            
            # Clear the cart after the order is successfully created
            cart = Cart(request)
            cart.clear()
            
            return redirect('order_detail', order_id=order.id)
        return render(request, 'orders/order_form.html', {'form': form})


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        if order_id is None:
            return redirect('order_list')
        
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return redirect('order_list')
        
        return render(request, 'orders/order_pay.html', {'order': order})
