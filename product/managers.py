from django.db import models
from django.utils import timezone

class PublishManager(models.Manager):
    """
    Custom manager for handling published/unpublished items.
    Provides methods to filter items based on their publication status.
    """
    def get_queryset(self):
        return super().get_queryset()

    def published(self):
        """
        Returns only published items that are available and marked as published.
        """
        return self.get_queryset().filter(
            publish=True,
            available=True,
            created__lte=timezone.now()
        )

    def unpublished(self):
        """
        Returns only unpublished items.
        """
        return self.get_queryset().filter(
            publish=False
        )

    def with_discount(self):
        """
        Returns items that have an active discount.
        """
        return self.get_queryset().filter(
            discount_available=True,
            discount_amount__gt=0
        )

    def in_stock(self):
        """
        Returns items that are in stock (inventory > 0).
        """
        return self.get_queryset().filter(
            inventory__gt=0
        )

    def out_of_stock(self):
        """
        Returns items that are out of stock (inventory = 0).
        """
        return self.get_queryset().filter(
            inventory=0
        )

    def featured(self):
        """
        Returns published items that are in stock and have discounts.
        """
        return self.published().with_discount().in_stock()

    def for_sale(self):
        """
        Returns all items that are available for sale (published and in stock).
        """
        return self.published().in_stock()

    def by_gender(self, gender):
        """
        Returns published items filtered by gender.
        """
        return self.published().filter(gender=gender)

    def by_category(self, category):
        """
        Returns published items filtered by category.
        """
        return self.published().filter(categories=category) 