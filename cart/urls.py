from django.urls import path, re_path
from .views import CartDetailView, CartAddView, CartRemoveView , CartUpdateView

app_name = "cart"

urlpatterns = [
    path("", CartDetailView.as_view(), name="cart_detail"),
    re_path(r"^add/(?P<shoe_id>\d+)/$", CartAddView.as_view(), name="cart_add"),
    re_path(r"^remove/(?P<shoe_id>\d+)/$", CartRemoveView.as_view(), name="cart_remove"),
    re_path(r"^update/(?P<shoe_id>\d+)/$", CartUpdateView.as_view(), name="cart_update"),
]
