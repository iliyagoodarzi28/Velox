from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Shoe, Category, Color , Size , Category
from .forms import ShoeSelectionForm
from django.db.models import Q


class ShoeListView(ListView):
    """نمایش لیست کفش‌ها با امکان فیلتر بر اساس نام، رنگ، سایز، جنسیت و محدوده قیمت"""
    model = Shoe
    template_name = "shoe_store/shoe_list.html"
    context_object_name = "shoes"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # فیلتر جستجو بر اساس نام یا توضیحات
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        # فیلتر بر اساس رنگ (با استفاده از slug مدل Color)
        color = self.request.GET.get('color')
        if color:
            queryset = queryset.filter(colors__slug=color)
        # فیلتر بر اساس سایز (استفاده از مقدار یکتا در فیلد value برای Size)
        size = self.request.GET.get('size')
        if size:
            queryset = queryset.filter(sizes__value=size)
        # فیلتر بر اساس جنسیت
        gender = self.request.GET.get('gender')
        if gender:
            queryset = queryset.filter(gender__iexact=gender)
        # فیلتر بر اساس محدوده قیمت
        min_price = self.request.GET.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        max_price = self.request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        # فیلتر بر اساس دسته بندی
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        available = self.request.GET.get('available')
        if available:
            if available.lower() == 'true':
                queryset = queryset.filter(available=True, inventory__gt=0)
            elif available.lower() == 'false':
                queryset = queryset.filter(Q(available=False) | Q(inventory=0))
            elif available.lower() == 'discount':
                queryset = queryset.filter(discount_available=True, inventory=0)


        return queryset.distinct()  # حذف تکراری‌ها در نتیجه به علت روابط چند به چند

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ارسال لیست رنگ‌ها و سایز‌ها به قالب جهت نمایش انتخاب‌ها در فرم فیلتر
        context['color_list'] = Color.objects.all()
        context['size_list'] = Size.objects.all()
        return context


class ShoeDetailView(DetailView):
    model = Shoe
    template_name = "shoe_store/shoe_detail.html"
    context_object_name = "shoe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selection_form'] = ShoeSelectionForm(shoe=self.object)
        return context


class CategoryDetailView(ListView):
    """نمایش لیست کفش‌ها بر اساس یک دسته‌بندی انتخاب شده"""
    model = Shoe
    template_name = "shoe_store/category_detail.html"
    context_object_name = "shoes"

    def get_queryset(self):
        # جستجوی دسته‌بندی بر اساس slug و فیلتر کردن کفش‌ها مربوط به آن
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        queryset = Shoe.objects.filter(categories=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        # افزودن اطلاعات دسته‌بندی به context جهت استفاده در قالب
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context



class CategoryListView(ListView):
    model = Category
    template_name = 'shoe_store/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        # نمایش تمام دسته‌بندی‌ها، چه دسته‌بندی اصلی و چه زیر دسته‌ها
        return Category.objects.all()

