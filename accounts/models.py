from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils.text import slugify
from products.models import Product

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    username = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    tel = models.CharField(max_length=20, unique=True, null=True, blank=True)
    fixed_address = models.TextField(null=True, blank=True)
    avatar_url = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.username:
            base_slug = slugify(self.username)
            slug = base_slug
            count = 1
            while User.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        print("checkedPassword:",make_password(raw_password))
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'product')
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"