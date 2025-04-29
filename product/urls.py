from django.urls import path
from . import views
app_name = 'shoe_store'

urlpatterns = [
    path('shoes/', views.ShoeListView.as_view(), name='shoe_list'),
    path('shoe/<slug:slug>/', views.ShoeDetailView.as_view(), name='shoe_detail'),
    path('categories/', views.CategoryListView.as_view(), name='shoe_category_list'),  # لیست دسته‌بندی‌ها

    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='shoe_category_detail'),
]
