from django.views.generic import TemplateView
from site_info.models import SiteInfo
from blog.models import Blog , Category as BlogCategory
from product.models import Category as ProductCategory , Shoe

class BaseSiteInfoView(TemplateView):
    """Base view to include site information in context."""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_info'] = SiteInfo.get_info()
        return context
    
    
class HomeView(BaseSiteInfoView):
    template_name = 'main/index.html'  # قالب صفحه خانه

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # گرفتن ۳ بلاگ آخرین، مرتب‌شده بر اساس تاریخ
        context['latest_posts'] = Blog.objects.all().order_by('-date')[:3]
        # گرفتن ۳ دسته‌بندی آخرین، مرتب‌شده بر اساس تاریخ
        context['categories_blog'] = BlogCategory.objects.all().order_by('-slug')[:5]

        context['categories_shoe'] = ProductCategory.objects.all().order_by('-slug')[:5]

        context['shoes'] = Shoe.objects.all().order_by('-slug')[:5]

        return context




class AboutView(BaseSiteInfoView):
    template_name = 'main/about.html'



