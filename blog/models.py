from django.db import models
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.text import slugify


class BaseModel(models.Model):
    """
    Base model to avoid duplicate fields.
    """
    name = models.CharField(max_length=200, verbose_name='Name')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Slug')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True, verbose_name='Image')

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Category(BaseModel):
    """
    مدل دسته‌بندی بلاگ.
    """
    class Meta(BaseModel.Meta):
        pass


class Blog(BaseModel):
    """
    مدل پست بلاگ.
    """
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='blogs',
        verbose_name='Category'
    )
    description = RichTextField(blank=True, null=True, verbose_name='Description')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    views = models.PositiveIntegerField(default=0, verbose_name='Views')

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.slug])


class Comment(models.Model):
    """
    مدل نظر برای پست‌های بلاگ.
    """
    blog = models.ForeignKey(
        Blog, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name='Blog'
    )
    name = models.CharField(max_length=100, verbose_name='Name')
    email = models.EmailField(verbose_name='Email')
    content = models.TextField(verbose_name='Content')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Created At')
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name='User'
    )

    def __str__(self):
        return f'Comment by {self.name} on {self.blog}'


class Rating(models.Model):
    """
    مدل امتیاز دهی برای پست‌های بلاگ.
    هر کاربر تنها یک بار می‌تواند به هر پست امتیاز خود را بدهد.
    """
    blog = models.ForeignKey(
        Blog, 
        on_delete=models.CASCADE, 
        related_name='ratings',
        verbose_name='Blog'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    score = models.IntegerField(verbose_name='Score')  # امتیاز؛ مثلاً از 1 تا 5

    class Meta:
        unique_together = ('blog', 'user')

    def __str__(self):
        return f'{self.user.username} rated {self.blog.name}: {self.score}'
