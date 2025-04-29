from django.urls import path
from . import views
urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('pay/<int:order_id>/', views.OrderPayView.as_view(), name='order_pay'),
]
