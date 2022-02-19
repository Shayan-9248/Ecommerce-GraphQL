# Core django imports
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.created.strftime('%Y-%m-%d')}"


class Category(TimeStamp):
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=True, blank=True, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Product(TimeStamp):
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    slug = models.SlugField(null=True, blank=True, unique=True)
    available = models.BooleanField(default=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    amount = models.PositiveIntegerField(null=True, blank=True)
    discount = models.PositiveIntegerField(null=True, blank=True)
    total_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    image = models.ImageField(default="1.jpg")
    sell = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, blank=True, null=True
    )
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="p_like"
    )
    dislike = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="p_dislike"
    )
    favourite = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="fav"
    )

    class Meta(TimeStamp.Meta):
        ordering = ("-created",)
        indexes = [models.Index(fields=["title"])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.total_price = self.get_total_price
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("product:detail", args=[self.slug, self.id])

    @property
    def get_total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price
