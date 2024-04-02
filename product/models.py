from django.db import models
from django.utils import timezone

from authentication.models import CustomUser


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    description = models.TextField()
    colors = models.ManyToManyField(Color)  # Array of available colors
    type = models.CharField(max_length=50)  # Type of the product

    def __str__(self):
        return self.title


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    color_purchased = models.ForeignKey(Color, on_delete=models.CASCADE)
    purchased_from_vendor = models.CharField(max_length=255)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.user.first_name} {self.user.last_name} for {self.product.title}"


class ProductQuestion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    anonymous = models.BooleanField(default=False)

    def __str__(self):
        user_name = "Anonymous" if self.anonymous else f"{self.user.first_name} {self.user.last_name}"
        return f"Question by {user_name} for {self.product.title}"


class ProductAnswer(models.Model):
    question = models.ForeignKey(ProductQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    anonymous = models.BooleanField(default=False)

    def __str__(self):
        user_name = "Anonymous" if self.anonymous else f"{self.user.first_name} {self.user.last_name}"
        return f"Answer by {user_name} for {self.question.product.title}"