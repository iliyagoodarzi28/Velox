from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from decimal import Decimal
from django.utils.text import slugify
from .managers import PublishManager

class BaseModel(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug', blank=True)
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
    sub_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        null=True,
        blank=True,
        verbose_name='Sub Category'
    )
    is_sub = models.BooleanField(default=False, verbose_name='Is Subcategory')

    class Meta(BaseModel.Meta):
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('shoe_store:shoe_category_detail', args=[self.slug])

class Color(BaseModel):
    name = models.CharField(max_length=50, verbose_name='Color Name')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Color Slug', blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'

    def get_absolute_url(self):
        return reverse('shoe_store:color_detail', args=[self.slug])

class Size(models.Model):
    value = models.CharField(
        max_length=10,
        unique=True,
        help_text="Enter the shoe size (e.g., 7, 8, 9, etc.).",
        verbose_name='Size Value'
    )

    class Meta:
        ordering = ('value',)
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

    def __str__(self):
        return self.value

class Shoe(BaseModel):
    categories = models.ManyToManyField(Category, related_name='shoes', verbose_name='Categories')
    description = RichTextField(verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Price')
    available = models.BooleanField(default=True, verbose_name='Available')
    publish = models.BooleanField(default=False, verbose_name='Publish', help_text='Designates whether this product should be published.')
    discount_available = models.BooleanField(default=False, verbose_name='Discount Available')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Discount Amount')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    gender = models.CharField(max_length=10, choices=[
        ('men', 'Men'),
        ('women', 'Women'),
        ('unisex', 'Unisex'),
        ('kids', 'Kids'),
    ], verbose_name='Gender')
    sizes = models.ManyToManyField(Size, related_name='shoes', blank=True, verbose_name='Sizes')
    colors = models.ManyToManyField(Color, related_name='shoes', blank=True, verbose_name='Colors')
    inventory = models.PositiveIntegerField(default=10, help_text="Available stock", verbose_name='Inventory')

    # Add the custom manager
    objects = PublishManager()

    class Meta(BaseModel.Meta):
        pass

    def get_absolute_url(self):
        return reverse('shoe_store:shoe_detail', args=[self.slug])

    def reduce_stock(self, quantity):
        if self.inventory >= quantity:
            self.inventory -= quantity
            self.save()
        else:
            raise ValueError("Not enough stock available!")

    @property
    def discount_amount(self):
        if self.discount_available and self.discount_percentage > 0:
            return self.price * (self.discount_percentage / 100)
        return Decimal('0.00')
