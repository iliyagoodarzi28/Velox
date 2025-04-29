from django.db import models

class SiteInfo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image_header = models.ImageField(upload_to='header/%Y/%m/%d', blank=True)  # Corrected field definition
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @classmethod
    def get_info(cls):
        return cls.objects.first()  